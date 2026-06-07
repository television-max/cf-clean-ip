import requests
import concurrent.futures
import time
from datetime import datetime

def check_ip(ip):
    try:
        url = f"http://{ip}/cdn-cgi/trace"
        response = requests.get(url, timeout=3)
        if response.status_code == 200 and "cf-ray" in response.text:
            return ip
    except:
        pass
    return None

def scan_ips():
    base_ips = [f"104.16.0.{i}" for i in range(1, 255)]
    base_ips += [f"104.17.{i}.{j}" for i in range(1, 255) for j in range(1, 255)]
    # می‌تونی آیپی‌های بیشتری اضافه کنی
    
    clean_ips = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(check_ip, base_ips)
        for ip in results:
            if ip:
                clean_ips.append(ip)
                print(f"✅ پیدا شد: {ip}")
    
    # ذخیره در فایل
    with open("clean_ips.txt", "w") as f:
        for ip in clean_ips:
            f.write(ip + "\n")
    
    print(f"\n🎯 تعداد آیپی‌های تمیز: {len(clean_ips)}")
    return clean_ips

if __name__ == "__main__":
    scan_ips()
