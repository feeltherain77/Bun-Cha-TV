import requests, re, time, random
from urllib.parse import quote

# Giả lập trình duyệt xịn để không bị chặn
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
REF = 'https://bit.ly/bunchatv/'
# Các trang con để quét vét sạch trận đấu
PAGES = [REF, f'{REF}truc-tiep/', f'{REF}lich-thi-dau/']

def run_grab():
    # Thêm mã thời gian để ép App TV phải tải lại ảnh mới (phá cache)
    t_hash = str(int(time.time()))
    m3u_text = '#EXTM3U\n'
    h = {'User-Agent': UA, 'Referer': REF}
    all_links = set()
    
    try:
        # 1. Quét vét tất cả các link trận đấu hiện có
        for p in PAGES:
            try:
                r = requests.get(p, headers=h, timeout=15).text
                found = re.findall(r'href="([^"]*truc-tiep/[^"]*)"', r)
                for l in found:
                    full_u = REF + l if l.startswith('/') else l
                    all_links.add(full_u)
            except: continue
        
        # 2. Bóc tách chi tiết từng trận
        for match_u in all_links:
            try:
                d = requests.get(match_u, headers=h, timeout=10).text
                stream_links = re.findall(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', d)
                
                if stream_links:
                    # LẤY THUMBNAIL (ẢNH TRẬN ĐẤU)
                    thumb_match = re.search(r'property="og:image" content="(.*?)"', d)
                    img = f"{thumb_match.group(1)}?t={t_hash}" if thumb_match else ""

                    # LẤY TÊN TRẬN VÀ DỌN RÁC (Xóa sạch 00n11/05, 17h30...)
                    title_m = re.search(r'<title>(.*?)</title>', d, re.S)
                    name = title_m.group(1).split('|')[0].replace('Trực tiếp', '').strip() if title_m else "Bóng đá"
                    name = re.sub(r'\d{2}[nh]\d{2}(/\d{2})?', '', name) # Xóa sạch mã số thô

                    # LẤY TÊN BÌNH LUẬN VIÊN
                    blvs = re.findall(r'class="name-player">([^<]+)', d)
                    
                    for i, link in enumerate(stream_links):
                        raw_l = link.replace("\\", "")
                        # Lấy nhãn: BLV hoặc Server (S1, S2...)
                        tag = blvs[i].strip() if i < len(blvs) else f"S{i+1}"
                        if tag.isdigit(): tag = f"S{tag}"
                        
                        # Cấu trúc: [Tên BLV] Tên Trận
                        display_name = f"[{tag}] {name}"
                        
                        # Link kèm Header lách luật chuẩn cho OTT/Televizo
                        final_l = f"{raw_l}|User-Agent={quote(UA)}&Referer={quote(REF)}&Origin={quote(REF)}"
                        
                        # Xuất ra định dạng M3U chuẩn
                        m3u_text += f'#EXTINF:-1 tvg-name="{display_name}" tvg-logo="{img}" group-title="Bún Chả TV", {display_name}\n{final_l}\n'
            except: continue
    except: pass

    # Lưu lại file
    with open('live.m3u', 'w', encoding='utf-8') as f:
        f.write(m3u_text)

if __name__ == "__main__":
    run_grab()
  
