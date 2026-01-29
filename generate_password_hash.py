#!/usr/bin/env python3
"""
สคริปต์สำหรับสร้าง Password Hash สำหรับระบบ Login
"""
import hashlib
import getpass

print("=" * 60)
print("🔐 สร้าง Password Hash สำหรับ Piramid Lucky Draw")
print("=" * 60)
print()

# รับรหัสผ่าน
password = getpass.getpass("กรุณากรอกรหัสผ่านที่ต้องการใช้: ")
password_confirm = getpass.getpass("ยืนยันรหัสผ่านอีกครั้ง: ")

if password != password_confirm:
    print("\n❌ รหัสผ่านไม่ตรงกัน กรุณาลองใหม่อีกครั้ง")
    exit(1)

if len(password) < 6:
    print("\n⚠️  คำเตือน: รหัสผ่านควรมีความยาวอย่างน้อย 6 ตัวอักษร")

# สร้าง hash
password_hash = hashlib.sha256(password.encode()).hexdigest()

print("\n" + "=" * 60)
print("✅ สร้าง Password Hash สำเร็จ!")
print("=" * 60)
print()
print("คัดลอก hash ด้านล่างไปใส่ใน secrets.toml หรือ Streamlit Secrets:")
print()
print(f"password_hash = \"{password_hash}\"")
print()
print("=" * 60)
