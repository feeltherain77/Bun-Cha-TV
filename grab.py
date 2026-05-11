import requests, re

def run():
    h = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    m = '#EXTM3U\n'
    try:
        # 1. Lấy danh sách trận đấu đang live
        r = requests.get('https://bunchatv4.net/', headers=h, timeout=15).text
        # Tìm tất cả link trực tiếp trận đấu
        matches = re.findall(r'href="([^"]*truc-tiep/[^"]*)"', r)
        
        for m_url in set(matches):
            u = 'https://bunchatv4.net' + m_url if m_url.startswith('/') else m_url
            try:
                # 2. Vào trang trận đấu, soi cái Iframe chứa video
                d = requests.get(u, headers=h, timeout=10).text
                # Tìm link cdn-hls hoặc các link m3u8 ẩn
                s = re.findall(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', d)
                
                # Nếu không thấy, soi tiếp trong các thẻ iframe ẩn
                if not s:
                    frame = re.findall(r'iframe.*?src="([^"]+)"', d)
                    for f_url in frame:
                        f_content = requests.get(f_url, headers=h, timeout=5).text
                        s += re.findall(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', f_content)
                
                if s:
                    # Lấy tên trận đấu từ URL cho gọn
                    name = m_url.split('/')[-1].replace('-', ' ').title()[:30]
                    link = s[0].replace("\\", "")
                    m += f'#EXTINF:-1, [Live] {name}\n{link}\n'
            except: continue
    except: pass
    
    with open('live.m3u', 'w', encoding='utf-8') as f:
        f.write(m.strip() + '\n')

if __name__ == "__main__": run()
