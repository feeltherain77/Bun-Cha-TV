import requests, re

def run():
    h = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    # Lệnh này cực quan trọng để fix lỗi "Lỗi phát kênh" trên App
    ua_fix = '#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\n'
    m = '#EXTM3U\n'
    
    # --- NGUỒN 1: BÚN CHẢ TV ---
    try:
        r1 = requests.get('https://bunchatv4.net/', headers=h, timeout=15).text
        links1 = set(re.findall(r'href="([^"]*truc-tiep/[^"]*)"', r1))
        for l in links1:
            u = 'https://bunchatv4.net' + l if l.startswith('/') else l
            try:
                d = requests.get(u, headers=h, timeout=10).text
                s = re.findall(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', d)
                if s:
                    name = l.split('/')[-1].replace('-', ' ').title()[:30]
                    link = s[0].replace("\\", "")
                    # Thêm group-title và UA Fix
                    m += f'#EXTINF:-1 group-title="Bún Chả TV", [Bún Chả] {name}\n{ua_fix}{link}\n'
            except: continue
    except: pass

    # --- NGUỒN 2: (Ông chỉ cần dán link web nguồn mới vào đây) ---
    # Tôi sẽ làm mẫu một cấu trúc tương tự nếu ông có link Xôi Lạc...

    # Ghi file
    with open('live.m3u', 'w', encoding='utf-8') as f:
        f.write(m.strip() + '\n')

if __name__ == "__main__":
    run()

if __name__ == "__main__": run()
