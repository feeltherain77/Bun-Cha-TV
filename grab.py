import requests
import re

def run():
    header = {'User-Agent': 'Mozilla/5.0'}
    m3u = '#EXTM3U\n'
    try:
        # Lấy danh sách BLV từ trang chủ
        content = requests.get('https://bunchatv4.net/', headers=header).text
        # Tìm các link BLV và lọc bỏ "nhà đài"
        links = re.findall(r'href="([^"]*binh-luan-vien/[^"]*)"', content)
        links = list(set([l for l in links if "nha-dai" not in l.lower()]))
        
        for l in links:
            url = 'https://bunchatv4.net' + l if l.startswith('/') else l
            name = l.split('/')[-1].replace('-', ' ').title()
            # Bóc link m3u8 trong trang chi tiết
            detail = requests.get(url, headers=header).text
            stream = re.findall(r'(https?://[\w\.-]+[:\d]*/[\w\.-/]+\.m3u8[^\s"\'<>]*)', detail)
            if stream:
                m3u += f'#EXTINF:-1, [Royx] {name}\n{stream[0].replace("\\", "")}\n'
    except:
        pass
    
    # Luôn ghi file để tránh lỗi "did not match any files"
    with open('live.m3u', 'w', encoding='utf-8') as f:
        f.write(m3u)

if __name__ == "__main__":
    run()
  
