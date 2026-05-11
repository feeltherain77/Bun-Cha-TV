import requests, re
from urllib.parse import quote

# 1. Khai báo các loại khóa để lách 403
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
REFERER = 'https://bunchatv4.net/'
ORIGIN = 'https://bunchatv4.net'

m3u_content = '#EXTM3U\n'

try:
    headers = {'User-Agent': UA, 'Referer': REFERER}
    # Quét trang chủ lấy trận
    response = requests.get(REFERER, headers=headers, timeout=15)
    response.encoding = 'utf-8'
    r = response.text
    
    matches = set(re.findall(r'href="([^"]*truc-tiep/[^"]*)"', r))
    
    for m_url in matches:
        u = REFERER + m_url if m_url.startswith('/') else m_url
        try:
            # Vào trang trận đấu bóc m3u8
            detail = requests.get(u, headers=headers, timeout=10).text
            
            # Bóc tên trận đấu từ thẻ h1 hoặc title
            t_match = re.search(r'<h1.*?>(.*?)</h1>', detail, re.S)
            if t_match:
                name = re.sub('<[^<]+?>', '', t_match.group(1)).strip() # Xóa tag html nếu có
                name = name.split('|')[0].replace('Trực tiếp', '').strip()
            else:
                name = "Bóng đá Live"

            # Tìm link m3u8 (Fix lỗi ký tự lạ)
            links = re.findall(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', detail)
            if links:
                raw_link = links[0].replace("\\", "")
                
                # 2. TUYỆT CHIÊU CUỐI: Ép Header vào link
                # Thêm Origin và Referer trực tiếp vào sau dấu |
                # Đây là định dạng chuẩn để các app như IPTV Pro, OTT Navigator mở được link 403
                headers_inject = f"|User-Agent={quote(UA)}&Referer={quote(REFERER)}&Origin={quote(ORIGIN)}"
                final_link = raw_link + headers_inject
                
                m3u_content += f'#EXTINF:-1 group-title="Bún Chả TV", {name}\n{final_link}\n'
        except:
            continue
except Exception as e:
    print(f"Lỗi rồi Mạnh ơi: {e}")

# 3. Ghi file cực chuẩn
with open('live.m3u', 'w', encoding='utf-8') as f:
    f.write(m3u_content)
print("Đã nổ hũ file live.m3u thành công!")
with open('live.m3u', 'w', encoding='utf-8') as f:
    f.write(m)
  
