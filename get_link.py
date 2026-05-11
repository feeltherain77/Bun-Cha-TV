import requests, re, time, random
from urllib.parse import quote

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
REF = 'https://bunchatv4.net/'

def run_grab():
    t_hash = str(int(time.time()))
    m3u_text = f'#EXTM3U\n'
    h = {'User-Agent': UA, 'Referer': REF}
    
    try:
        # 1. QUÉT TRANG CHỦ ĐỂ LẤY THUMBNAIL VÀ LINK TRẬN
        r = requests.get(REF, headers=h, timeout=15).text
        # Tìm các khối chứa: link trận + ảnh thumbnail
        match_blocks = re.findall(r'<a[^>]*href="([^"]*truc-tiep/[^"]*)"[^>]*>.*?src="([^"]+)"', r, re.S)
        
        # Nếu trang chủ không có ảnh, lấy tạm link trận lẻ
        if not match_blocks:
            links = re.findall(r'href="([^"]*truc-tiep/[^"]*)"', r)
            match_blocks = [(l, "") for l in links]

        for m_url, m_img in match_blocks:
            full_u = REF + m_url if m_url.startswith('/') else m_url
            try:
                # Làm sạch link ảnh
                img = m_img if m_img.startswith('http') else REF + m_img
                
                d = requests.get(full_u, headers=h, timeout=10).text
                # 2. BỐC TÊN TRẬN (Dọn rác triệt để)
                title_m = re.search(r'<title>(.*?)</title>', d, re.S)
                name = title_m.group(1).split('|')[0].replace('Trực tiếp', '').strip() if title_m else "Bóng đá"
                name = re.sub(r'\d{2}[nh]\d{2}(/\d{2})?', '', name).strip()

                # 3. BỐC BLV & LINK STREAM (Bắt cặp để không lệch)
                # Tìm các cụm có chứa tên (thường trong class name-player) và link m3u8
                items = re.findall(r'class="name-player">([^<]+).*?(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', d, re.S)
                
                if not items:
                    # Cách dự phòng nếu bắt cặp xịt
                    streams = re.findall(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', d)
                    labels = re.findall(r'>(?:Link|Server|BLV|Kênh)\s*([^<]+)<', d, re.I)
                    items = [(labels[i].strip() if i < len(labels) else f"S{i+1}", s) for i, s in enumerate(streams)]

                for tag, link in items:
                    tag = tag.replace('Link', '').replace('Server', '').strip()
                    if tag.isdigit(): tag = f"S{tag}"
                    
                    display_name = f"[{tag}] {name}"
                    final_img = f"{img}?t={t_hash}" if img else ""
                    # Header lách luật full
                    final_link = f"{link.replace('\\', '')}|User-Agent={quote(UA)}&Referer={quote(REF)}&Origin={quote(REF)}"
                    
                    m3u_text += f'#EXTINF:-1 tvg-name="{display_name}" tvg-logo="{final_img}" group-title="Bún Chả TV", {display_name}\n{final_link}\n'
            except: continue
    except: pass

    with open('live.m3u', 'w', encoding='utf-8') as f:
        f.write(m3u_text)

if __name__ == "__main__":
    run_grab()
