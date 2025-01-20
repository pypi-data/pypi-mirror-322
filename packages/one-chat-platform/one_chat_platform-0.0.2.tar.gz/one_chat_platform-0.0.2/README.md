
## อัปเดตเวอร์ชันในไฟล์ setup.py
### เปิดไฟล์ setup.py และอัปเดตตัวแปร version เป็นเวอร์ชันใหม่
```python
setup(
    name='your_package',
    version='1.1.0',  # อัปเดตเวอร์ชันที่นี่
    ...
)
```

## สร้างแพ็กเกจใหม่
### ใช้คำสั่งเพื่อสร้างไฟล์สำหรับอัปโหลด
```bash
python setup.py sdist bdist_wheel
```

## อัปโหลดไปยัง PyPI
### ใช้ twine เพื่ออัปโหลดแพ็กเกจ
```bash
twine upload dist/*
```

## API Token
```bash
pypi-AgEIcHlwaS5vcmcCJDQ4NTgyMzFiLTdiMDgtNDMxYy05NTNmLTUyOWFlNjAzMjQ1MQACGVsxLFsib25lLWNoYXQtcGxhdGZvcm0iXV0AAixbMixbIjhmMWNlMDMzLTRhNGMtNDdmMi1hMTQzLTE0MjRhNTgxNzRmMSJdXQAABiAcIu0yQGcvlEVXIUYfYb2XhEPP2-NwNlSrV-5pzRGeVw
```