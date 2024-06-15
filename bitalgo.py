!pip install pycryptodome

import hashlib
from Crypto.Cipher import AES

# تابع جایگشت بایت‌ها به صورت تصادفی
def byte_permutation(data):
    return data[::-1]

# تابع تولید زیر کلید با استفاده از SHA-256
def generate_subkey(key, round_num):
    hashed_key = hashlib.sha256(key).digest()
    subkey = hashed_key[round_num*2:(round_num+1)*2]  # استفاده از 2 بایت
    return subkey

# عملیات XOR بر روی دو بایت‌های ورودی
def xor_bytes(byte1, byte2):
    return bytes(x ^ y for x, y in zip(byte1, byte2))

# الگوریتم فیستل-بیت برای یک بلوک 64 بیتی
def feistel_bit_algorithm(data_block):
    # کلید ثابت (مثلاً)
    key = b'secret_key'

    left_block = data_block[:4]
    right_block = data_block[4:]

    # اجرای 16 دور از الگوریتم فیستل-بیت
    for round_num in range(16):
        # استفاده از زیر کلید از کلید ثابت
        subkey = generate_subkey(key, round_num)

        # اعمال XOR بر روی بخش راست با زیر کلید
        xor_result = xor_bytes(right_block, subkey)

        # جایگشت بایت‌ها به صورت تصادفی
        permuted_right = byte_permutation(xor_result)

        # ترکیب بخش چپ با نتیجه جایگشت بایت‌ها با استفاده از XOR
        new_left_block = right_block
        new_right_block = xor_bytes(left_block, permuted_right)

        # به‌روزرسانی بلوک برای دور بعدی
        left_block = new_left_block
        right_block = new_right_block

    # ترکیب بلوک‌های نهایی بعد از تمام دورها
    final_block = left_block + right_block
    return final_block

# مثال استفاده از الگوریتم با ورودی از کاربر
if __name__ == "__main__":
    # ورودی از کاربر برای داده
    data_input = input("Enter data (64-bit in hex, 16 characters): ")
    
    # تبدیل ورودی به بایت
    data_bytes = bytes.fromhex(data_input)
    
    # بررسی طول ورودی
    if len(data_bytes) != 8:
        raise ValueError("Input data must be exactly 64 bits (8 bytes).")
    
    # اجرای الگوریتم فیستل-بیت برای داده ورودی
    encrypted_data = feistel_bit_algorithm(data_bytes)
    print("Encrypted Data:", encrypted_data.hex())
