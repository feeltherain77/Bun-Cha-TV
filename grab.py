import requests
import re
import time
import random
from urllib.parse import quote

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
REF = 'https://bunchatv4.net/'
PAGES = [REF, f'{REF}truc-tiep/', f'{REF}lich-thi-dau/']

def run_grab():
    time.sleep(random.randint(1, 5))
    m3u_text = '#EXTM3U\n'
    h = {'User-Agent': UA, 'Referer': REF}
    all_match_links = set()
    
    try:
        for page in PAGES:
            try:
                r = requests.get(page, headers=h, timeout=15).text
                found = re.findall(r'href="([^"]*truc-tiep/[^"]*)"', r)
                for l in found:
                    full_u = REF + l if l.startswith('/') else l
                    all_match_links.add(full_u)
            except: continue
        
        for full_u in all_match_links:
            try:
                d = requests.get(full_u, headers=h, timeout=10).text
                stream_links = re.findall(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', d)
                
                if stream_links:
                    # 1. Bóc Thumbnail (Ảnh bìa trận đấu)
                    thumb_match = re.search(r'property="og:image" content="(.*?)"', d)
                    thumb_url = thumb_match.group(1) if thumb_match else ""

                    # 2. Bóc Tên trận (lấy từ Title cho sạch)
                    title_match = re.search(r'<title>(.*?)</title>', d, re.S)
                    name = title_match.group(1).split('|')[0].replace('Trực tiếp', '').replace('Link xem', '').strip() if title_match else "Bóng đá"

                    # 3. Bóc BLV
                    blv_labels = re.findall(r'class="name-player">([^<]+)', d)
                    
                    for i, link in enumerate(stream_links):
                        raw_link = link.replace("\\", "")
                        blv_tag = blv_labels[i].strip() if i < len(blv_labels) else f"S{i+1}"
                        
                        # Đưa BLV lên đầu để không bị cắt tên
                        display_name = f"[{blv_tag}] {name}"
                        
                        final_link = f"{raw_link}|User-Agent={quote(UA)}&Referer={quote(REF)}&Origin={quote(REF)}"
                        # Thêm tvg-logo để hiện ảnh
                        m3u_text += f'#EXTINF:-1 tvg-name="{display_name}" tvg-logo="{thumb_url}" group-title="Bún Chả TV", {display_name}\n{final_link}\n'
            except: continue
    except: pass

    with open('live.m3u', 'w', encoding='utf-8') as f:
        f.write(m3u_text)

if __name__ == "__main__":
    run_grab()
  
