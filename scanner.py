import requests
import concurrent.futures

# محدوده‌های معروف Cloudflare (IPv4)
ip_ranges = [
    "104.16.0.{}",
    "104.17.0.{}",
    "104.18.0.{}",
    "104.19.0.{}",
    "104.20.0.{}",
    "104.21.0.{}",
    "104.22.0.{}",
    "104.23.0.{}",
    "104.24.0.{}",
    "104.25.0.{}",
    "104.26.0.{}",
    "104.27.0.{}",
    "172.64.0.{}",
    "172.65.0.{}",
    "172.66.0.{}",
    "172.67.0.{}",
]

def check_ip(ip):
    try:
        url = f"http://{ip}/cdn-cgi/trace"
        r = requests.get(url, timeout=2)
        if r.status_code == 200 and "cf-ray" in r.text:
            return ip
    except:
        pass
    return None

def scan():
    clean = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as ex:
        futures = []
        for base in ip_ranges:
            for i in range(1, 256):
                ip = base.format(i)
                futures.append(ex.submit(check_ip, ip))
        for f in concurrent.futures.as_completed(futures):
            result = f.result()
            if result:
                clean.append(result)
                print(f"✅ {result}")
    
    with open("clean_ips.txt", "w") as f:
        for ip in clean:
            f.write(ip + "\n")
    
    print(f"\n🎯 تعداد کل آیپی‌های تمیز: {len(clean)}")

if __name__ == "__main__":
    scan()
