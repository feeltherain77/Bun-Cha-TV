import requests, re
from urllib.parse import quote

# 1. Khai báo "giấy thông hành"
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
h = {'User-Agent': ua, 'Referer': 'https://bunchatv4.net/'}

m = '#EXTM3U\n'

try:
    r = requests.get('https://bunchatv4.net/', headers=h, timeout=10).text
    matches = set(re.findall(r'href="([^"]*truc-tiep/[^"]*)"', r))
    
    for m_url in matches:
        u = 'https://bunchatv4.net' + m_url if m_url.startswith('/') else m_url
        try:
            d = requests.get(u, headers=h, timeout=7).text
            # Bắt tên trận
            t = re.search(r'<h1.*?>(.*?)</h1>', d, re.S) or re.search(r'<title>(.*?)</title>', d)
            name = t.group(1).split('|')[0].replace('Trực tiếp', '').strip() if t else "Trận đấu"
            
            # Bắt link m3u8
            s = re.findall(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', d)
            if s:
                link = s[0].replace("\\", "")
                
                # 2. ĐÂY LÀ ĐOẠN QUAN TRỌNG NHẤT:
                # Gắn thẳng "giấy thông hành" vào đuôi link để App IPTV tự mở được
                # Dấu | thần thánh giúp App hiểu phải dùng UA và Referer nào
                final_link = f"{link}|User-Agent={quote(ua)}&Referer={quote('https://bunchatv4.net/')}"
                
                m += f'#EXTINF:-1 group-title="Bún Chả TV", [Live] {name}\n{final_link}\n'
        except: continue
except: pass

# 3. Ghi vào file live.m3u
with open('live.m3u', 'w', encoding='utf-8') as f:
    f.write(m)
  
