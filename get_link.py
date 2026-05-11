import requests
import re
from urllib.parse import quote, urljoin

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
BASE_URL = 'https://bunchatv4.net/'

# Cấu hình Logo và Nhóm tự động
SPORTS_CONFIG = {
    "Bóng đá": {
        "logo": "https://nha-cai.com/wp-content/uploads/2023/11/qua-bong-da.jpg",
        "keywords": ["bóng đá", "vđqg", "cup", "league", "united", "fc", "vs", "u23", "u19"]
    },
    "Tennis": {
        "logo": "https://i.pinimg.com/originals/94/3a/0d/943a0d4948e42658f8608e906c27e02e.png",
        "keywords": ["tennis", "quần vợt", "atp", "wta", "grand slam", "open"]
    },
    "Bóng rổ": {
        "logo": "https://i.pinimg.com/originals/7b/72/70/7b7270b216f496f86c2d829983995815.png",
        "keywords": ["bóng rổ", "nba", "basketball"]
    }
}
DEFAULT_LOGO = "https://nha-cai.com/wp-content/uploads/2023/11/qua-bong-da.jpg"

def get_sport_info(title):
    title_lower = title.lower()
    for sport, config in SPORTS_CONFIG.items():
        if any(kw in title_lower for kw in config["keywords"]):
            return sport, config["logo"]
    return "Thể Thao", DEFAULT_LOGO

def get_m3u():
    m3u = "#EXTM3U\n"
    h = {'User-Agent': UA, 'Referer': BASE_URL}
    processed = set()
    
    try:
        r = requests.get(BASE_URL, headers=h, timeout=15).text
        matches = re.findall(r'href="([^"]*(?:truc-tiep|match)/[^"]+)"', r)
        
        for m_url in list(set(matches)):
            full_u = urljoin(BASE_URL, m_url)
            if full_u in processed: continue
            
            try:
                d = requests.get(full_u, headers=h, timeout=10).text
                streams = re.findall(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', d)
                
                if streams:
                    t_match = re.search(r'<title>(.*?)</title>', d)
                    raw_title = t_match.group(1) if t_match else "Trực tiếp Thể Thao"
                    
                    # Phân loại Logo theo môn
                    sport_group, sport_logo = get_sport_info(raw_title)
                    
                    # Tách tên Trận và tên BLV
                    parts = raw_title.split('|')
                    clean_name = parts[0].replace('Trực tiếp', '').strip()
                    blv_tag = ""
                    if len(parts) > 1:
                        blv_part = parts[-1].strip()
                        if "BLV" in blv_part:
                            blv_tag = f"[{blv_part}] "
                    
                    # Định dạng: [BLV Giàng A Phò] MU vs Arsenal
                    display_name = f"{blv_tag}{clean_name}"
                    
                    for i, s in enumerate(streams):
                        # Fix lỗi syntax bằng cách xử lý biến trước f-string
                        s_clean = s.replace('\\', '')
                        q_ua = quote(UA)
                        q_ref = quote(full_u)
                        
                        final_link = f"{s_clean}|User-Agent={q_ua}&Referer={q_ref}"
                        m3u += f'#EXTINF:-1 tvg-logo="{sport_logo}" group-title="{sport_group}", {display_name} - S{i+1}\n{final_link}\n'
            except: continue
            processed.add(full_u)
            
    except Exception as e:
        print(f"Lỗi: {e}")
    
    with open("list.m3u", "w", encoding="utf-8") as f:
        f.write(m3u)

if __name__ == "__main__":
    get_m3u()
    
