import requests
import re
from urllib.parse import quote, urljoin

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
BASE_URL = 'https://bunchatv4.net/'

# Dùng link ảnh trực tiếp từ CDN để đảm bảo Logo luôn hiện
LOGO_BONG_DA = "https://raw.githubusercontent.com/manh-dz/logo/main/football.png" 
# Nếu không có link trên, dùng link dự phòng này:
DEFAULT_LOGO = "https://i.imgur.com/8N9E0M0.png"

def get_m3u():
    m3u_lines = []
    h = {'User-Agent': UA, 'Referer': BASE_URL}
    processed = set()
    
    try:
        r = requests.get(BASE_URL, headers=h, timeout=15).text
        matches = re.findall(r'href="([^"]*(?:truc-tiep|match)/[^"]+)"', r)
        
        for m_url in list(dict.fromkeys(matches))[::-1]: 
            full_u = urljoin(BASE_URL, m_url)
            if full_u in processed: continue
            try:
                d = requests.get(full_u, headers=h, timeout=10).text
                streams = re.findall(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', d)
                
                if streams:
                    # 1. LẤY TÊN TRẬN (Quét cực kỹ)
                    t_match = re.search(r'<title>(.*?)</title>', d)
                    raw_title = t_match.group(1) if t_match else "Trực tiếp"
                    clean_name = raw_title.split('|')[0].replace('Trực tiếp', '').strip()

                    # 2. SĂN BLV (Quét mọi ngóc ngách trong code web)
                    blv_tag = ""
                    # Tìm cụm BLV kèm tên (bao gồm cả ký tự đặc biệt tiếng Việt)
                    blv_find = re.search(r'(?:BLV|Bình luận viên)\s*:?\s*([\w\sàáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệđìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ]+)', d, re.IGNORECASE)
                    
                    if blv_find:
                        tên_blv = blv_find.group(1).strip().upper()
                        # Loại bỏ các từ thừa nếu robot bốc nhầm
                        if len(tên_blv) < 30: # Giới hạn độ dài để tránh bốc nhầm cả đoạn văn
                            blv_tag = f"[{tên_blv}] "
                    elif '|' in raw_title:
                        blv_tag = f"[{raw_title.split('|')[-1].strip().upper()}] "

                    # 3. GÁN LOGO & GROUP (Ép logo quả bóng)
                    logo = LOGO_BONG_DA
                    group = "Bóng Đá TV"
                    if "tennis" in raw_title.lower():
                        logo = "https://i.imgur.com/6S6W8aA.png"
                        group = "Tennis TV"

                    for i, s in enumerate(streams):
                        s_link = s.replace('\\', '')
                        # ĐỊNH DẠNG CHUẨN: [BLV] Tên Trận - Link i
                        display_name = f"{blv_tag}{clean_name} - L{i+1}"
                        
                        # Dùng cấu hình này để Logo hiện trên mọi App (OTT, Smarters, VLC...)
                        line = f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}", {display_name}\n'
                        line += f'#EXTVLCOPT:http-user-agent={UA}\n'
                        line += f'#EXTVLCOPT:http-referrer={full_u}\n'
                        line += f'{s_link}'
                        m3u_lines.append(line)
            except: continue
            processed.add(full_u)
    except: pass

    with open("list.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n" + "\n".join(m3u_lines))

if __name__ == "__main__":
    get_m3u()
