import requests
import re
from urllib.parse import quote

# Giả lập User-Agent xịn để né chặn
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
REF = 'https://bunchatv4.net/'

def run_grab():
    m3u_text = '#EXTM3U\n'
    h = {'User-Agent': UA, 'Referer': REF}
    
    try:
        # Lấy trang chủ
        r = requests.get(REF, headers=h, timeout=15).text
        links = set(re.findall(r'href="([^"]*truc-tiep/[^"]*)"', r))
        
        for m_url in links:
            full_u = REF + m_url if m_url.startswith('/') else m_url
            try:
                # Vào trang trận đấu bóc link m3u8
                d = requests.get(full_u, headers=h, timeout=10).text
                stream_links = re.findall(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', d)
                
                if stream_links:
                    raw_link = stream_links[0].replace("\\", "")
                    # Bóc tên trận
                    t = re.search(r'<h1.*?>(.*?)</h1>', d, re.S)
                    name = re.sub('<[^<]+?>', '', t.group(1)).strip().split('|')[0] if t else "Bóng đá"
                    
                    # FIX FULL LỖI 403: Gắn khóa vào đuôi link
                    # Dùng cho IPTV Pro, OTT Navigator, VLC...
                    final_link = f"{raw_link}|User-Agent={quote(UA)}&Referer={quote(REF)}&Origin={quote(REF)}"
                    
                    m3u_text += f'#EXTINF:-1 group-title="Bún Chả TV", {name}\n{final_link}\n'
            except: continue
    except: pass

    with open('live.m3u', 'w', encoding='utf-8') as f:
        f.write(m3u_text)

if __name__ == "__main__":
    run_grab()
  
