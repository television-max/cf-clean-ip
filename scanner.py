import asyncio
import aiohttp
from aiohttp import ClientTimeout

# آخرین محدوده‌های رسمی IPv4 کلودفلیر (منبع: 5)
# (IPv4 - 103.21.244.0/22 , IPv4 - 103.22.200.0/22, ...)
IP_RANGES = [
    "103.21.244.{}",
    "103.22.200.{}",
    "103.31.4.{}",
    "104.16.{}",
    "104.17.{}",
    "104.18.{}",
    "104.19.{}",
    "104.20.{}",
    "104.21.{}",
    "104.22.{}",
    "104.23.{}",
    "104.24.{}",
    "104.25.{}",
    "104.26.{}",
    "104.27.{}",
    "108.162.192.{}",
    "108.162.193.{}",
    "108.162.194.{}",
    "108.162.195.{}",
    "108.162.196.{}",
    "108.162.197.{}",
    "108.162.198.{}",
    "108.162.199.{}",
    "131.0.72.{}",
    "141.101.64.{}",
    "141.101.65.{}",
    "141.101.66.{}",
    "141.101.67.{}",
    "162.158.0.{}",
    "172.64.{}",
    "172.65.{}",
    "172.66.{}",
    "172.67.{}",
    "173.245.48.{}",
    "173.245.49.{}",
    "173.245.50.{}",
    "173.245.51.{}",
    "173.245.52.{}",
    "173.245.53.{}",
    "173.245.54.{}",
    "173.245.55.{}",
    "188.114.96.{}",
    "188.114.97.{}",
    "188.114.98.{}",
    "188.114.99.{}",
    "190.93.240.{}",
    "190.93.241.{}",
    "190.93.242.{}",
    "190.93.243.{}",
    "197.234.240.{}",
    "197.234.241.{}",
    "197.234.242.{}",
    "197.234.243.{}",
    "198.41.128.{}",
    "198.41.129.{}",
    "198.41.130.{}",
    "198.41.131.{}",
    "198.41.132.{}",
    "198.41.133.{}",
    "198.41.134.{}",
    "198.41.135.{}",
]

async def check_ip(session, ip):
    try:
        url = f"http://{ip}/cdn-cgi/trace"
        async with session.get(url, timeout=ClientTimeout(total=1)) as resp:
            if resp.status == 200:
                text = await resp.text()
                if "cf-ray" in text:
                    return ip
    except:
        pass
    return None

async def scan():
    connector = aiohttp.TCPConnector(limit=0, limit_per_host=100, ttl_dns_cache=300)
    timeout = ClientTimeout(total=1)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = []
        for base in IP_RANGES:
            for i in range(1, 256):
                ip = base.format(i)
                tasks.append(check_ip(session, ip))
        results = await asyncio.gather(*tasks)
    
    clean = [ip for ip in results if ip]
    with open("clean_ips.txt", "w") as f:
        for ip in clean:
            f.write(ip + "\n")
    print(f"\n✅ تعداد آیپی‌های تمیز: {len(clean)}")

if __name__ == "__main__":
    asyncio.run(scan())
