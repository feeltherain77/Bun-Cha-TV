import requests
import re
import time
import random
from urllib.parse import quote

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
REF = 'https://bunchatv4.net/'

def run_grab():
    time.sleep(random.randint(1, 10))
    m3u_text = '#EXTM3U\n'
    h = {'User-Agent': UA, 'Referer': REF}
    
    try:
        r = requests.get(REF, headers=h, timeout=15).text
        links = set(re.findall(r'href="([^"]*truc-tiep/[^"]*)"', r))
        
        for m_url in links:
            full_u = REF + m_url if m_url.startswith('/') else m_url
            try:
                d = requests.get(full_u, headers=h, timeout=10).text
                stream_links = re.findall(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', d)
                
                if stream_links:
                    # CÁCH BÓC TÊN MỚI: Lấy từ thẻ <title> nếu h1 bị rác
                    title_search = re.search(r'<title>(.*?)</title>', d, re.S)
                    if title_search:
                        name = title_search.group(1).split('|')[0].replace('Trực tiếp', '').replace('Link xem', '').strip()
                    else:
                        name = "Bóng đá Live"

                    # Bóc BLV từ các thẻ server
                    blv_list = re.findall(r'class="name-player">([^<]+)', d)
                    
                    for i, link in enumerate(stream_links):
                        raw_link = link.replace("\\", "")
                        blv_tag = blv_list[i].strip() if i < len(blv_list) else f"Server {i+1}"
                        
                        display_name = f"{name} ({blv_tag})"
                        final_link = f"{raw_link}|User-Agent={quote(UA)}&Referer={quote(REF)}&Origin={quote(REF)}"
                        
                        m3u_text += f'#EXTINF:-1 tvg-name="{display_name}" group-title="Bún Chả TV", {display_name}\n{final_link}\n'
            except: continue
    except: pass

    with open('live.m3u', 'w', encoding='utf-8') as f:
        f.write(m3u_text)

if __name__ == "__main__":
    run_grab()
  
