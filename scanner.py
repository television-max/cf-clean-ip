import asyncio
import aiohttp
from aiohttp import ClientTimeout, ClientConnectorError

# محدوده‌های کلیدی Cloudflare (تنها پرکاربردترین‌ها برای سرعت بیشتر)
IP_RANGES = [
    "104.16.{}.{}",
    "104.17.{}.{}",
    "104.18.{}.{}",
    "104.19.{}.{}",
    "104.20.{}.{}",
    "104.21.{}.{}",
    "104.22.{}.{}",
    "104.23.{}.{}",
    "104.24.{}.{}",
    "104.25.{}.{}",
    "104.26.{}.{}",
    "104.27.{}.{}",
    "172.64.{}.{}",
    "172.65.{}.{}",
    "172.66.{}.{}",
    "172.67.{}.{}",
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
                for j in range(1, 256):
                    ip = base.format(i, j)
                    tasks.append(check_ip(session, ip))
        results = await asyncio.gather(*tasks)
    
    clean = [ip for ip in results if ip]
    with open("clean_ips.txt", "w") as f:
        for ip in clean:
            f.write(ip + "\n")
    print(f"\n✅ تعداد آیپی‌های تمیز: {len(clean)}")

if __name__ == "__main__":
    asyncio.run(scan())
