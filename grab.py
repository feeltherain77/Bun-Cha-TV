import requests, re, time, random
from urllib.parse import quote

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
REF = 'https://bunchatv4.net/'

def run_grab():
    # 1. Tạo mã phá cache (hash) và thời gian cập nhật
    t_hash = str(int(time.time()))
    current_time = time.strftime("%H:%M") 
    # Tên nhóm sẽ kèm giờ để App TV biết có dữ liệu mới
    group_name = f"Bún Chả TV (Cập nhật: {current_time})"
    
    m3u_text = f'#EXTM3U\n'
    h = {'User-Agent': UA, 'Referer': REF}
    
    try:
        # Quét trang chủ
        r = requests.get(REF, headers=h, timeout=15).text
        links = set(re.findall(r'href="([^"]*truc-tiep/[^"]*)"', r))
        
        for m_url in links:
            full_u = REF + m_url if m_url.startswith('/') else m_url
            try:
                d = requests.get(full_u, headers=h, timeout=10).text
                streams = re.findall(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', d)
                
                if streams:
                    # BỐC ẢNH + PHÁ CACHE
                    thumb = re.search(r'property="og:image" content="(.*?)"', d)
                    img = f"{thumb.group(1)}?t={t_hash}" if thumb else ""

                    # BỐC TÊN + XÓA RÁC (19h30, 20n05...)
                    title_m = re.search(r'<title>(.*?)</title>', d, re.S)
                    name = title_m.group(1).split('|')[0].replace('Trực tiếp', '').strip() if title_m else "Bóng đá"
                    name = re.sub(r'\d{2}[nh]\d{2}(/\d{2})?', '', name).strip()
                    
                    # BỐC BLV
                    blvs = re.findall(r'class="name-player">([^<]+)', d)
                    
                    for i, link in enumerate(streams):
                        tag = blvs[i].strip() if i < len(blvs) else f"S{i+1}"
                        if tag.isdigit(): tag = f"S{tag}"
                        
                        display_name = f"[{tag}] {name}"
                        # Header lách luật full cho TV
                        final_link = f"{link.replace('\\', '')}|User-Agent={quote(UA)}&Referer={quote(REF)}&Origin={quote(REF)}"
                        
                        m3u_text += f'#EXTINF:-1 tvg-name="{display_name}" tvg-logo="{img}" group-title="{group_name}", {display_name}\n{final_link}\n'
            except: continue
    except: pass

    with open('live.m3u', 'w', encoding='utf-8') as f:
        f.write(m3u_text)

if __name__ == "__main__":
    run_grab()
