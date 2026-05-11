import requests
import re
from urllib.parse import quote, urljoin

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
BASE_URL = 'https://bunchatv4.net/'

# Cấu hình Logo theo sở thích Mạnh DZ
SPORTS_CONFIG = {
    "Bóng đá": {"logo": "https://nha-cai.com/wp-content/uploads/2023/11/qua-bong-da.jpg", "keywords": ["bóng", "league", "cup", "vs", "united", "fc", "vđqg", "manchester", "chelsea", "arsenal", "liverpool", "real", "barca"]},
    "Tennis": {"logo": "https://i.pinimg.com/originals/94/3a/0d/943a0d4948e42658f8608e906c27e02e.png", "keywords": ["tennis", "quần vợt", "atp", "wta", "open"]},
}

def get_m3u():
    m3u_lines = []
    h = {'User-Agent': UA, 'Referer': BASE_URL}
    processed = set()
    
    try:
        r = requests.get(BASE_URL, headers=h, timeout=15).text
        matches = re.findall(r'href="([^"]*(?:truc-tiep|match)/[^"]+)"', r)
        
        # [::-1] để trận mới nhất nhảy lên đầu danh sách
        for m_url in list(dict.fromkeys(matches))[::-1]: 
            full_u = urljoin(BASE_URL, m_url)
            if full_u in processed: continue
            try:
                d = requests.get(full_u, headers=h, timeout=10).text
                streams = re.findall(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', d)
                
                if streams:
                    # Lấy Title làm gốc để bốc BLV
                    t_match = re.search(r'<title>(.*?)</title>', d)
                    raw_title = t_match.group(1) if t_match else "Live"
                    
                    # 1. XỬ LÝ Tên trận (Bỏ chữ Trực tiếp cho gọn)
                    clean_name = raw_title.split('|')[0].replace('Trực tiếp', '').strip()
                    
                    # 2. XỬ LÝ BLV (ÉP LÊN ĐẦU)
                    blv_tag = ""
                    # Tìm từ khóa BLV trong toàn bộ title (không phân biệt hoa thường)
                    blv_find = re.search(r'BLV\s+([\w\s]+)', raw_title, re.IGNORECASE)
                    if blv_find:
                        # Nếu thấy "BLV Giàng A Phò" -> biến thành [BLV GIÀNG A PHÒ]
                        blv_tag = f"[{blv_find.group(0).upper()}] "
                    elif '|' in raw_title:
                        # Nếu không có chữ BLV nhưng có dấu | thì lấy phần sau dấu |
                        blv_tag = f"[{raw_title.split('|')[-1].strip()}] "

                    # 3. PHÂN LOẠI LOGO & GROUP
                    logo = "https://nha-cai.com/wp-content/uploads/2023/11/qua-bong-da.jpg"
                    group = "Bóng Đá"
                    for k, v in SPORTS_CONFIG.items():
                        if any(kw in raw_title.lower() for kw in v["keywords"]):
                            logo, group = v["logo"], k
                            break

                    for i, s in enumerate(streams):
                        # Làm sạch link (xóa dấu \)
                        s_link = s.replace('\\', '')
                        
                        # ĐỊNH DẠNG TÊN: [BLV] Tên Trận - Link i
                        display_name = f"{blv_tag}{clean_name} - Link {i+1}"
                        
                        # Xây dựng nội dung dòng m3u theo chuẩn Đa Nền Tảng
                        line = f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}", {display_name}\n'
                        line += f'#EXTVLCOPT:http-user-agent={UA}\n'
                        line += f'#EXTVLCOPT:http-referrer={full_u}\n'
                        line += f'{s_link}'
                        m3u_lines.append(line)
            except: continue
            processed.add(full_u)
    except: pass

    # Ghi file
    with open("list.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n" + "\n".join(m3u_lines))

if __name__ == "__main__":
    get_m3u()
    
