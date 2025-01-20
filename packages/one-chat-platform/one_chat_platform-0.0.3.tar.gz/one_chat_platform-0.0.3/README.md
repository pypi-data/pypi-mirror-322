
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
pypi-AgEIcHlwaS5vcmcCJDhhY2Q1NjE5LWQ5ZGEtNDg1My1iY2MxLWIzOGQ3YjRjZjdiMwACGVsxLFsib25lLWNoYXQtcGxhdGZvcm0iXV0AAixbMixbIjhmMWNlMDMzLTRhNGMtNDdmMi1hMTQzLTE0MjRhNTgxNzRmMSJdXQAABiCtK5OC4vD4A4QIa7ZQG7QwddAIIkUuWMxZEPdD_ZufzQ
```

## วิธีใช้

```python
from one_chat_platform import *

token = "Your Access Token"
to = "User ID or Group ID"
init(
    token,
    to,
)


def main():
    send_message(
        message="Test Successfull ✅",
    )


if __name__ == "__main__":
    main()
```