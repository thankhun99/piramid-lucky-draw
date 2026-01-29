# คำสั่ง Git สำหรับ Deploy

## 1. ตั้งค่า Git (รันครั้งเดียว)
```powershell
git config --global user.name "ชื่อของคุณ"
git config --global user.email "email@example.com"
```

## 2. Commit ไฟล์
```powershell
git add .
git commit -m "Initial commit - Piramid Lucky Draw 2026"
```

## 3. Push ขึ้น GitHub
```powershell
git push -u origin main
```

## หมายเหตุ
- ถ้า GitHub ขอ username/password ให้ใช้ Personal Access Token แทนรหัสผ่าน
- สร้าง Token ได้ที่: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
