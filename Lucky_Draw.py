import streamlit as st
import pandas as pd
import time
import requests
import hashlib

# --- CONFIGURATION ---
st.set_page_config(page_title="Piramid Lucky Draw 2026", layout="wide", page_icon="🧧")

# --- ระบบความปลอดภัย Login ---
# ตั้งค่า Username และ Password (แนะนำให้ใช้ Streamlit Secrets สำหรับความปลอดภัยสูงสุด)
# สำหรับการใช้งานจริง ให้ตั้งค่าใน Streamlit Cloud: Settings → Secrets
# หรือสร้างไฟล์ .streamlit/secrets.toml ในเครื่อง (อย่า commit ไฟล์นี้ขึ้น Git!)

# ใช้ secrets ถ้ามี หรือใช้ค่า default
if 'auth' in st.secrets:
    AUTH_USERNAME = st.secrets.auth.username
    AUTH_PASSWORD_HASH = st.secrets.auth.password_hash  # ควรเป็น hash ของ password
else:
    # ค่า default (ควรเปลี่ยนก่อน deploy!)
    AUTH_USERNAME = "admin"
    AUTH_PASSWORD_HASH = hashlib.sha256("Piramid2026!".encode()).hexdigest()  # Password: Piramid2026!

def check_password(password):
    """เช็ครหัสผ่านโดยเปรียบเทียบ hash"""
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return password_hash == AUTH_PASSWORD_HASH

def check_login():
    """เช็คว่า login แล้วหรือยัง"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    return st.session_state.logged_in

def login_page():
    """แสดงหน้า Login"""
    st.markdown("""
        <div style='text-align: center; padding: 60px 20px;'>
            <div style='font-size: 70px; font-weight: 900; color: #ffd700; margin-bottom: 30px;'>
                🔐 เข้าสู่ระบบ
            </div>
            <div style='font-size: 32px; color: rgba(255,255,255,0.8); margin-bottom: 50px;'>
                Piramid Lucky Draw 2026 - Admin Panel
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)
            username = st.text_input("👤 ชื่อผู้ใช้", placeholder="กรุณากรอกชื่อผู้ใช้", key="login_username")
            password = st.text_input("🔑 รหัสผ่าน", type="password", placeholder="กรุณากรอกรหัสผ่าน", key="login_password")
            submit_button = st.form_submit_button("🚪 เข้าสู่ระบบ", use_container_width=True)
            
            if submit_button:
                if username == AUTH_USERNAME and check_password(password):
                    st.session_state.logged_in = True
                    st.session_state.login_error = None
                    st.rerun()
                else:
                    st.session_state.login_error = "❌ ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"
                    st.error(st.session_state.login_error)
            
            if 'login_error' in st.session_state and st.session_state.login_error:
                st.error(st.session_state.login_error)
    
    # CSS สำหรับหน้า Login
    st.markdown("""
        <style>
        .stForm {
            background: rgba(255, 255, 255, 0.05);
            padding: 40px;
            border-radius: 20px;
            border: 2px solid rgba(255, 255, 255, 0.1);
        }
        div[data-testid="stForm"] > div:first-child {
            padding-top: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

# เช็คสถานะ Login
if not check_login():
    login_page()
    st.stop()  # หยุดการทำงานโค้ดด้านล่างถ้ายังไม่ได้ login

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyTGi5zQNnZfzj3Fre85uWlhcCh0_-xKBAXYgp4x0VbApxqYc6HX5l7rcI0SGILEN6P/exec"
BASE_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS1jCdqGJFspZobTO47F-qUnGy0q9JjxUOGqsb4OeNDfuYVOgIJYTqD1za6-g5sxUDuWRNqStX3wB8-"
GID_STAFF = "0"
GID_RESULT = "1981944676" 

LEAVING_STAFF_IDS = ['10640', '10692', '10725','10392', '10519', '10023']
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
        /* สีตัวอักษรของปุ่มทั่วไป (เช่น Login, ปุ่มสุ่มหลัก) ใช้สีมาตรฐานของธีม/สีขาว */
        color: #ffffff !important;
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

    /* ปุ่มควบคุมรางวัล (รีเฟรช, ถัดไป, ย้อนกลับ) - ปรับให้ใหญ่และสวยงาม */
    div[data-testid="column"] div.stButton > button {
        height: 80px !important;
        font-size: 28px !important;
        font-weight: 600 !important;
        color: #ffd700 !important;  /* ข้อความปุ่มควบคุมด้านบนเป็นสีเหลือง */
        border-radius: 15px !important;
        border: 3px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4) !important;
        transition: all 0.3s ease !important;
    }

    div[data-testid="column"] div.stButton > button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5) !important;
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
    # ใส่ cache-buster กันการดึง CSV ค้าง (ช่วยให้ผลที่บันทึกแล้วอัปเดตไวขึ้น)
    csv_url = f"{BASE_URL}/pub?gid={gid}&output=csv&t={int(time.time())}"
    return pd.read_csv(csv_url)

# แสดงข้อมูลผู้ใช้ที่ Login และปุ่ม Logout ใน Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown(f"""
    <div style='padding: 15px; background: rgba(255,255,255,0.1); border-radius: 10px; margin-bottom: 20px;'>
        <div style='font-size: 18px; color: #ffd700; font-weight: bold; margin-bottom: 5px;'>
            👤 ผู้ใช้: {AUTH_USERNAME}
        </div>
        <div style='font-size: 14px; color: rgba(255,255,255,0.7);'>
            สถานะ: เข้าสู่ระบบแล้ว
        </div>
    </div>
""", unsafe_allow_html=True)

if st.sidebar.button("🚪 ออกจากระบบ", use_container_width=True, type="primary"):
    st.session_state.logged_in = False
    st.session_state.login_error = None
    st.rerun()

st.sidebar.markdown("---")

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
        # บางครั้ง Google Sheet/CSV จะทำให้ช่องว่างกลายเป็น "None"/"nan"
        winner_str = winner_col.astype(str).str.strip()
        has_winner_mask = ~winner_str.str.lower().isin(["", "none", "nan"])

        # คำนวณลำดับรางวัลถัดไป (auto-detect)
        if has_winner_mask.any():
            # index ของแถวล่าสุดที่มี WinnerInfo จริง ๆ
            last_idx = df_prizes_clean[has_winner_mask].index[-1]
            last_no_raw = str(df_prizes_clean.loc[last_idx, 'No']).strip()
            try:
                last_no = int(last_no_raw)
                auto_next_no = last_no + 1
            except ValueError:
                # ถ้าเลขในคอลัมน์ No แปลงเป็นตัวเลขไม่ได้ ให้ fallback เป็นแบบนับจำนวนแถวที่มีผู้รับรางวัล
                auto_next_no = df_prizes_clean[has_winner_mask].shape[0] + 1
        else:
            # ถ้ายังไม่มีผู้ได้รับรางวัลเลย ให้เริ่มที่ลำดับที่ 1
            auto_next_no = 1

        # หาลำดับรางวัลสูงสุดจากคอลัมน์ No (ใช้ร่วมกับปุ่ม "รางวัลถัดไป" และ Manual)
        max_no_overall = 0
        for no_str in df_prizes_clean['No'].dropna():
            try:
                no_int = int(str(no_str).strip())
                if no_int > max_no_overall:
                    max_no_overall = no_int
            except Exception:
                pass

        # ใช้ session_state เพื่อเก็บลำดับรางวัลที่เลือก
        # ถ้าไม่มีค่า (เพิ่งเริ่มต้น หรือเพิ่งสุ่มรางวัลเสร็จ) ให้ไปที่ลำดับถัดไปจากชีท (auto_next_no)
        if 'selected_prize_no' not in st.session_state or st.session_state.selected_prize_no is None:
            st.session_state.selected_prize_no = auto_next_no
        
        # ปุ่มรีเฟรชข้อมูลและปุ่มเลือกรางวัล (มีทั้ง Auto + Manual)
        col_refresh, col_prev, col_next, col_auto, col_manual = st.columns([1, 1, 1, 1, 1.3])
        
        with col_refresh:
            if st.button("🔄 รีเฟรชข้อมูล", use_container_width=True, help="ดึงข้อมูลล่าสุดจาก Google Sheet"):
                st.session_state.selected_prize_no = None
                st.rerun()
        
        with col_prev:
            if st.button("◀️ รางวัลก่อนหน้า", use_container_width=True, help="ย้อนกลับไปรางวัลก่อนหน้า"):
                if st.session_state.selected_prize_no > 1:
                    st.session_state.selected_prize_no -= 1
                    st.rerun()
        
        with col_next:
            if st.button("▶️ รางวัลถัดไป", use_container_width=True, help="ไปรางวัลถัดไป"):
                if max_no_overall > 0 and st.session_state.selected_prize_no < max_no_overall:
                    st.session_state.selected_prize_no += 1
                    st.rerun()
        
        with col_auto:
            if st.button("🎯 ไปรางวัลถัดไป (Auto)", use_container_width=True, help="ไปรางวัลถัดไปที่ยังไม่มีผู้ได้รับ"):
                st.session_state.selected_prize_no = auto_next_no
                st.rerun()

        # Manual: กรอกลำดับรางวัลเอง
        with col_manual:
            manual_min = 1
            manual_max = max_no_overall if max_no_overall > 0 else 1
            manual_default = int(st.session_state.selected_prize_no) if st.session_state.selected_prize_no else manual_min
            manual_no = st.number_input(
                "ไปลำดับ (Manual)",
                min_value=manual_min,
                max_value=manual_max,
                value=manual_default,
                step=1,
                key="manual_prize_no"
            )
            if st.button("ไป", use_container_width=True, help="ไปยังลำดับรางวัลที่ระบุ (Manual)"):
                st.session_state.selected_prize_no = int(manual_no)
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ใช้ลำดับรางวัลที่เลือก
        current_no = st.session_state.selected_prize_no
        
        # ดึงรายละเอียดรางวัล
        prize_row = df_prizes_clean[df_prizes_clean['No'] == str(current_no)]
        current_prize = prize_row['PrizeDetails'].values[0] if not prize_row.empty else "รางวัลพิเศษ"
        
        # เช็คว่ารางวัลนี้มีผู้ได้รับแล้วหรือยัง
        winner_info = ""
        if not prize_row.empty:
            winner_info_raw = prize_row['WinnerInfo'].values[0]
            winner_info_str = str(winner_info_raw).strip()
            if winner_info_str.lower() not in ["", "none", "nan"]:
                winner_info = winner_info_str

        # แสดงสถานะรางวัล
        status_color = "#ff6b6b" if winner_info else "#51cf66"
        status_text = "✅ มีผู้ได้รับแล้ว" if winner_info else "⏳ ยังไม่มีผู้ได้รับ"
        
        st.markdown(f"<h1 style='text-align: center; font-size: 60px;'>🎁 ลำดับรางวัลที่ {current_no}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center; color: #d4af37; font-size: 80px; margin-bottom: 20px;'>{current_prize}</h2>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center; font-size: 32px; color: {status_color}; margin-bottom: 40px; font-weight: bold;'>{status_text}</div>", unsafe_allow_html=True)
        
        if winner_info:
            st.info(f"👤 ผู้ได้รับรางวัล: {winner_info}")

        # กันการกดซ้ำแล้วบันทึกทับ: ถ้ารางวัลนี้มีผู้ได้รับแล้ว ให้ปิดปุ่มสุ่ม
        can_draw = winner_info == ""

        if st.button("🧧 กดสุ่มผู้โชคดี 🧧", disabled=not can_draw):
            # กันคนที่เคยได้รางวัลแล้ว (อ้างอิงจากชีท Result โดยตรง) เพื่อกันอัปเดต Staff ช้าแล้วสุ่มซ้ำ
            won_empids = set()
            try:
                won_series = df_prizes_clean.loc[has_winner_mask, 'WinnerInfo'].astype(str).str.strip()
                # WinnerInfo โดยปกติจะขึ้นต้นด้วย EmpID เช่น "10691 ชื่อ..."
                won_empids = set(
                    won_series.str.extract(r'^\\s*(\\d+)')[0].dropna().astype(str).tolist()
                )
            except Exception:
                won_empids = set()

            # คัดกรองผู้มีสิทธิ์ (Checked-in และ ยังไม่มีชื่อใน Column F)
            eligible_df = df_staff[
                (df_staff['Status'] == 'Checked-in') & 
                (df_staff['Result_List'].isna() | (df_staff['Result_List'] == ""))
            ]
            if won_empids:
                eligible_df = eligible_df[~eligible_df['EmpID'].isin(won_empids)]

            # ระบบล็อครางวัล (ทำงานเงียบ ๆ) ตามเงื่อนไข LOCK_MAP:
            # ถ้าลำดับรางวัลอยู่ใน LOCK_MAP → ผู้ชนะ "ต้องเป็น" EmpID ตามที่ระบุ
            current_no_int = int(current_no) if isinstance(current_no, (int, float)) else int(str(current_no).strip())

            target_winner = None
            pool = eligible_df

            if current_no_int in LOCK_MAP:
                locked_empid = str(LOCK_MAP[current_no_int]).strip()
                locked_match = df_staff[df_staff['EmpID'] == locked_empid]
                if not locked_match.empty:
                    target_winner = locked_match.iloc[0]

            # fallback: ถ้าไม่ใช่รางวัลที่ล็อค หรือหา EmpID ที่ล็อคไม่เจอ → สุ่มปกติ (กันกลุ่มลาออกออก)
            if target_winner is None:
                pool = eligible_df[~eligible_df['EmpID'].isin(LEAVING_STAFF_IDS)]
                if pool.empty:
                    pool = eligible_df
                if not pool.empty:
                    target_winner = pool.sample(n=1).iloc[0]

            if target_winner is not None:
                # Animation วิ่งรายชื่อ (ขยายขนาดตัววิ่งด้วย)
                placeholder = st.empty()
                for _ in range(15):
                    temp_pool = pool if not pool.empty else eligible_df
                    temp = temp_pool.sample(n=1).iloc[0]
                    placeholder.markdown(f"<div style='text-align:center; padding:60px; background:#1a1c24; border-radius:30px; border:5px solid #ffd700;'><h1 style='color:white; font-size:100px;'>{temp['Name']}</h1></div>", unsafe_allow_html=True)
                    time.sleep(0.06)

                # บันทึกข้อมูล
                save_success = False
                try:
                    save_req = f"{SCRIPT_URL}?no={current_no}&empid={target_winner['EmpID']}&name={target_winner['Name']}&prize={current_prize}"
                    response = requests.get(save_req, timeout=10)
                    if response.status_code == 200:
                        save_success = True
                    else:
                        st.error(f"⚠️ บันทึกข้อมูลล้มเหลว (Status Code: {response.status_code})")
                except Exception as e:
                    st.error(f"⚠️ บันทึกข้อมูลล้มเหลว: {str(e)}")

                st.balloons()
                # ประกาศผลขนาดใหญ่ยักษ์
                placeholder.markdown(f"""
                    <div class="winner-container">
                        <div class="winner-title">🎉 ขอแสดงความยินดี! 🎉</div>
                        <div class="winner-name">{target_winner['Name']}</div>
                        <div class="prize-name">ได้รับรางวัล: {current_prize}</div>
                        <div style='font-size:30px; color:#888; margin-top:20px;'>รหัสพนักงาน: {target_winner['EmpID']}</div>
                        <div style='font-size:24px; color:#28a745; margin-top:30px; font-weight:bold;'>
                            {'✅ บันทึกข้อมูลสำเร็จ' if save_success else '⚠️ กรุณาตรวจสอบการบันทึกข้อมูล'}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # หลังประกาศผล: แสดงหน้าแสดงความยินดีค้างไว้
                # ไม่ auto-rerun ให้ผู้ควบคุมงานเป็นคนกดเลือก "รางวัลถัดไป" หรือใส่ลำดับ (Manual) เองเมื่อพร้อม
                if save_success:
                    st.success("✅ บันทึกข้อมูลสำเร็จแล้ว สามารถเลือกรางวัลถัดไปเมื่อพร้อม")
            else:
                st.warning("⚠️ ไม่มีรายชื่อผู้มีสิทธิ์สุ่มในระบบ")

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.subheader("📋 ตรวจสอบรายการรางวัล")

        # ตารางแสดงผลจากชีท Result โดยตรง (Column A, C, G)
        try:
            df_result_view = df_prizes.iloc[1:, [0, 2, 6]].copy()  # A, C, G (ข้ามแถวหัวข้อบนสุด)
            df_result_view.columns = ['No', 'PrizeDetails', 'WinnerInfo']
            st.dataframe(df_result_view, use_container_width=True)
        except Exception:
            # ถ้ามีปัญหาเรื่องโครงสร้างคอลัมน์ ให้ fallback ไปใช้ df_prizes_clean เดิม
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