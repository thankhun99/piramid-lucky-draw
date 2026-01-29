import streamlit as st
import pandas as pd
import time
import requests

# --- CONFIGURATION ---
st.set_page_config(page_title="Piramid Lucky Draw 2026", layout="wide", page_icon="🧧")

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyTGi5zQNnZfzj3Fre85uWlhcCh0_-xKBAXYgp4x0VbApxqYc6HX5l7rcI0SGILEN6P/exec"
BASE_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS1jCdqGJFspZobTO47F-qUnGy0q9JjxUOGqsb4OeNDfuYVOgIJYTqD1za6-g5sxUDuWRNqStX3wB8-"
GID_STAFF = "0"
GID_RESULT = "1981944676" 

LEAVING_STAFF_IDS = ['10640', '10692', '10392', '10519', '10023']
LOCK_MAP = {4: '10640', 8: '10692', 12: '10392', 15: '10519', 19: '10023'}

# --- CUSTOM CSS FOR BIG HALL ---
st.markdown("""
    <style>
    /* พื้นหลังและฟอนต์สำหรับจอโปรเจคเตอร์ใน Hall */
    html, body, [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top, #1b2735 0%, #090a0f 55%, #000000 100%) !important;
        color: #f5f5f5 !important;
        font-family: "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif !important;
        font-size: 24px !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    section[data-testid="stSidebar"] {
        background: rgba(0, 0, 0, 0.85) !important;
        backdrop-filter: blur(6px) !important;
        border-right: 2px solid rgba(255, 255, 255, 0.15) !important;
    }

    /* ตัวอักษรใน Sidebar และเมนูให้ใหญ่ขึ้น */
    section[data-testid="stSidebar"] .stRadio > label,
    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        font-size: 26px !important;
        font-weight: 600 !important;
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        font-size: 22px !important;
    }

    /* หัวข้อหลักให้เด่นและอ่านง่าย */
    h1 {
        font-size: 72px !important;
        font-weight: 900 !important;
        letter-spacing: 2px !important;
        color: #ffffff !important;
        text-shadow: 0 6px 18px rgba(0, 0, 0, 0.8) !important;
    }

    h2 {
        font-size: 48px !important;
        font-weight: 700 !important;
        color: #ffd700 !important;
        text-shadow: 0 4px 12px rgba(0, 0, 0, 0.7) !important;
    }

    h3, .stSubheader {
        font-size: 40px !important;
        font-weight: 700 !important;
    }

    /* ตัวหนังสือทั่วไปให้ใหญ่ขึ้น */
    p, span, label {
        font-size: 26px !important;
    }

    /* ปรับขนาดปุ่มสุ่มให้ใหญ่ยักษ์ */
    div.stButton > button {
        width: 100% !important;
        height: 170px !important;
        font-size: 64px !important;
        font-weight: bold !important;
        color: white !important;
        background: linear-gradient(45deg, #FF4B2B, #FF416C) !important;
        border-radius: 30px !important;
        border: 5px solid #ffffff !important;
        box-shadow: 0 14px 40px rgba(0, 0, 0, 0.7) !important;
        transition: transform 0.25s ease, box-shadow 0.25s ease, background 0.25s ease !important;
    }

    div.stButton > button:hover {
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8) !important;
        background: linear-gradient(45deg, #FF416C, #FF4B2B) !important;
    }

    /* กล่องประกาศผลผู้โชคดีขนาดใหญ่ */
    .winner-container {
        text-align: center;
        padding: 80px;
        background: radial-gradient(circle at top, #ffffff 0%, #f5f5f5 60%, #e4e4e4 100%);
        border: 20px solid #28a745;
        border-radius: 50px;
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.6);
        margin: 30px 0;
    }

    .winner-title {
        font-size: 60px !important;
        color: #28a745;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .winner-name {
        font-size: 140px !important;
        font-weight: 900;
        color: #111111;
        line-height: 1.05;
        margin: 30px 0;
    }

    .prize-name {
        font-size: 70px !important;
        color: #d4af37;
        font-weight: 800;
    }

    /* ตารางข้อมูลให้ตัวใหญ่ขึ้นสำหรับฉายบนจอ */
    .dataframe td, .dataframe th {
        font-size: 26px !important;
        padding: 14px 18px !important;
    }

    [data-testid="stDataFrame"] div[role="gridcell"],
    [data-testid="stDataFrame"] div[role="columnheader"] {
        font-size: 26px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# แบนเนอร์หัวหน้าหน้า สำหรับงานปีใหม่
st.markdown("""
    <div style='text-align: center; padding: 20px 0 10px;'>
        <div style='font-size: 90px; font-weight: 900; color: #ffd700; text-shadow: 0 8px 25px rgba(0,0,0,0.9);'>
            PIRAMID LUCKY DRAW 2026
        </div>
        <div style='font-size: 40px; color: rgba(255,255,255,0.85); margin-top: 10px;'>
            New Year Celebration Night
        </div>
    </div>
""", unsafe_allow_html=True)

def get_sheet_data(gid):
    csv_url = f"{BASE_URL}/pub?gid={gid}&output=csv"
    return pd.read_csv(csv_url)

# ใช้ Sidebar เมนู
menu = st.sidebar.radio("เมนูใช้งาน", ["🎯 เริ่มสุ่มรางวัล", "📜 สรุปผู้ได้รับรางวัล", "👥 ตรวจสอบการลงทะเบียน"])

try:
    # โหลดข้อมูล Staff 
    df_staff = get_sheet_data(GID_STAFF)
    df_staff['EmpID'] = df_staff['EmpID'].astype(str).str.strip()
    
    # โหลดข้อมูล Result ของรางวัล (เพื่อเช็คว่าสุ่มไปถึงลำดับไหนแล้ว)
    df_prizes = get_sheet_data(GID_RESULT)
    df_prizes_clean = df_prizes.iloc[1:].copy()
    df_prizes_clean.columns = ['No', 'ColB', 'PrizeDetails', 'D', 'E', 'F', 'WinnerInfo'] + list(df_prizes_clean.columns[7:])
    df_prizes_clean['No'] = df_prizes_clean['No'].astype(str).str.strip()

    if menu == "🎯 เริ่มสุ่มรางวัล":
        # --- ระบบตรวจสอบลำดับล่าสุดจากชีท Result คอลัมน์ G (ผู้ได้รับรางวัล) ---
        # ใช้ "แถวล่าสุดที่ไม่ว่างและไม่เป็น NaN" แล้วไปลุ้นรางวัลลำดับถัดไป
        winner_col = df_prizes_clean['WinnerInfo']
        not_na_mask = winner_col.notna()
        not_blank_mask = winner_col.astype(str).str.strip() != ""
        has_winner_mask = not_na_mask & not_blank_mask

        if has_winner_mask.any():
            # index ของแถวล่าสุดที่มี WinnerInfo จริง ๆ
            last_idx = df_prizes_clean[has_winner_mask].index[-1]
            last_no_raw = str(df_prizes_clean.loc[last_idx, 'No']).strip()
            try:
                last_no = int(last_no_raw)
                current_no = last_no + 1
            except ValueError:
                # ถ้าเลขในคอลัมน์ No แปลงเป็นตัวเลขไม่ได้ ให้ fallback เป็นแบบนับจำนวนแถวที่มีผู้รับรางวัล
                current_no = df_prizes_clean[has_winner_mask].shape[0] + 1
        else:
            # ถ้ายังไม่มีผู้ได้รับรางวัลเลย ให้เริ่มที่ลำดับที่ 1
            current_no = 1

        # ดึงรายละเอียดรางวัล
        prize_row = df_prizes_clean[df_prizes_clean['No'] == str(current_no)]
        current_prize = prize_row['PrizeDetails'].values[0] if not prize_row.empty else "รางวัลพิเศษ"

        st.markdown(f"<h1 style='text-align: center; font-size: 60px;'>🎁 ลำดับรางวัลที่ {current_no}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center; color: #d4af37; font-size: 80px; margin-bottom: 40px;'>{current_prize}</h2>", unsafe_allow_html=True)

        if st.button("🧧 กดสุ่มผู้โชคดี 🧧"):
            # คัดกรองผู้มีสิทธิ์ (Checked-in และ ยังไม่มีชื่อใน Column F)
            eligible_df = df_staff[
                (df_staff['Status'] == 'Checked-in') & 
                (df_staff['Result_List'].isna() | (df_staff['Result_List'] == ""))
            ]

            target_winner = None
            
            # เช็คระบบล็อค (Sequence Lock)
            if current_no in LOCK_MAP:
                t_id = LOCK_MAP[current_no]
                match = eligible_df[eligible_df['EmpID'] == t_id]
                if not match.empty:
                    target_winner = match.iloc[0]
            
            # สุ่มจากผู้มีสิทธิ์ทั่วไป
            if target_winner is None:
                pool = eligible_df[~eligible_df['EmpID'].isin(LEAVING_STAFF_IDS)]
                if not pool.empty:
                    target_winner = pool.sample(n=1).iloc[0]

            if target_winner is not None:
                # Animation วิ่งรายชื่อ (ขยายขนาดตัววิ่งด้วย)
                placeholder = st.empty()
                for _ in range(15):
                    temp = eligible_df.sample(n=1).iloc[0]
                    placeholder.markdown(f"<div style='text-align:center; padding:60px; background:#1a1c24; border-radius:30px; border:5px solid #ffd700;'><h1 style='color:white; font-size:100px;'>{temp['Name']}</h1></div>", unsafe_allow_html=True)
                    time.sleep(0.06)

                # บันทึกข้อมูล
                try:
                    save_req = f"{SCRIPT_URL}?no={current_no}&empid={target_winner['EmpID']}&name={target_winner['Name']}&prize={current_prize}"
                    requests.get(save_req, timeout=10)
                except:
                    st.error("⚠️ บันทึกข้อมูลล้มเหลว (ตรวจสอบอินเทอร์เน็ต)")

                st.balloons()
                # ประกาศผลขนาดใหญ่ยักษ์
                placeholder.markdown(f"""
                    <div class="winner-container">
                        <div class="winner-title">🎉 ขอแสดงความยินดี! 🎉</div>
                        <div class="winner-name">{target_winner['Name']}</div>
                        <div class="prize-name">ได้รับรางวัล: {current_prize}</div>
                        <div style='font-size:30px; color:#888; margin-top:20px;'>รหัสพนักงาน: {target_winner['EmpID']}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ ไม่มีรายชื่อผู้มีสิทธิ์สุ่มในระบบ")

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.subheader("📋 ตรวจสอบรายการรางวัล")
        st.dataframe(df_prizes_clean[['No', 'PrizeDetails', 'WinnerInfo']], use_container_width=True)

    elif menu == "📜 สรุปผู้ได้รับรางวัล":
        st.subheader("📜 รายชื่อผู้ได้รับรางวัลทั้งหมด")
        winners = df_staff[df_staff['Result_List'].notna() & (df_staff['Result_List'] != "")]
        st.table(winners[['EmpID', 'Name', 'Result_List']])

    elif menu == "👥 ตรวจสอบการลงทะเบียน":
        st.subheader("👥 พนักงานที่ลงทะเบียนเข้างานแล้ว")
        st.dataframe(df_staff[df_staff['Status'] == 'Checked-in'][['EmpID', 'Name', 'Result_List']])

except Exception as e:
    st.error(f"เกิดข้อผิดพลาดทางเทคนิค: {e}")