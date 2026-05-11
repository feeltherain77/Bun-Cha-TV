import requests, re

def run():
    # Chứng minh thư để web không chặn
    h = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    # Chuỗi User-Agent để app IPTV vượt rào
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    
    m = '#EXTM3U\n'
    try:
        # 1. Lấy danh sách trận
        r = requests.get('https://bunchatv4.net/', headers=h, timeout=15).text
        matches = set(re.findall(r'href="([^"]*truc-tiep/[^"]*)"', r))
        
        for m_url in matches:
            u = 'https://bunchatv4.net' + m_url if m_url.startswith('/') else m_url
            try:
                d = requests.get(u, headers=h, timeout=10).text
                
                # 2. Bắt tên trận đấu (Lấy trong thẻ H1 hoặc Title)
                name_match = re.search(r'<h1.*?>(.*?)</h1>', d, re.S)
                if not name_match:
                    name_match = re.search(r'<title>(.*?)</title>', d)
                
                if name_match:
                    name = name_match.group(1).split('|')[0].replace('Trực tiếp', '').strip()
                else:
                    name = m_url.split('/')[-1]

                # 3. Húp link m3u8
                s = re.findall(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', d)
                if s:
                    link = s[0].replace("\\", "")
                    # Cấu trúc FIX LỖI PHÁT KÊNH: Thêm trực tiếp User-Agent vào dòng INF
                    m += f'#EXTINF:-1 group-title="Bún Chả TV" http-user-agent="{ua}", [Live] {name}\n{link}\n'
            except: continue
    except: pass

    with open('live.m3u', 'w', encoding='utf-8') as f:
        f.write(m.strip() + '\n')

if __name__ == "__main__":
    run()
