import requests
import re
from urllib.parse import quote, urljoin

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
BASE_URL = 'https://bunchatv4.net/'

def get_m3u():
    m3u_lines = []
    h = {'User-Agent': UA, 'Referer': BASE_URL}
    processed = set()
    
    try:
        # 1. LẤY LOGO CHÍNH CHỦ TỪ WEB
        r_home = requests.get(BASE_URL, headers=h, timeout=15).text
        logo_match = re.search(r'src="([^"]*logo[^"]*\.png[^"]*)"', r_home, re.I)
        web_logo = urljoin(BASE_URL, logo_match.group(1)) if logo_match else "https://bunchatv4.net/wp-content/uploads/2024/03/logo-buncha.png"

        # 2. QUÉT TRẬN ĐẤU
        matches = re.findall(r'href="([^"]*(?:truc-tiep|match)/[^"]+)"', r_home)
        
        for m_url in list(dict.fromkeys(matches))[::-1]: 
            full_u = urljoin(BASE_URL, m_url)
            if full_u in processed: continue
            try:
                d = requests.get(full_u, headers=h, timeout=10).text
                streams = re.findall(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', d)
                
                if streams:
                    t_match = re.search(r'<title>(.*?)</title>', d)
                    raw_title = t_match.group(1) if t_match else ""
                    
                    # LỌC TÊN TRẬN (Sút văng đống rác CACHEPBONGDA)
                    clean_name = raw_title.split('|')[0].replace('Trực tiếp', '').split('-')[0].strip()
                    clean_name = re.sub(r'(CACHEPBONGDA|BUNCHATV|LIVE|VIP|WEB|COM)', '', clean_name, flags=re.I).strip()

                    # BẮT BLV (Ưu tiên tên người thực sự)
                    blv_tag = ""
                    potential = re.findall(r'BLV\s+([\w\sàáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệđìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ]+)', d, re.I)
                    for p in potential:
                        p_up = p.strip().upper()
                        if not any(x in p_up for x in ["CACHEP", "BONGDA", "BUNCHA", "LIVE", "WEB"]):
                            if 1 < len(p_up) < 15:
                                blv_tag = f"[{p_up}] "
                                break

                    for i, s in enumerate(streams):
                        s_link = s.replace('\\', '')
                        # ĐỊNH DẠNG: [BLV] Tên trận - L1
                        display_name = f"{blv_tag}{clean_name} - L{i+1}"
                        
                        # GROUP TITLE MỚI: Bún Chả TV
                        line = f'#EXTINF:-1 tvg-logo="{web_logo}" group-title="Bún Chả TV", {display_name}\n'
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
    
