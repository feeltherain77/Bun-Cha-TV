import requests
import re

def run():
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Referer': 'https://bunchatv4.net/'
    }
    m3u = '#EXTM3U\n'
    
    try:
        # 1. Lấy trang chủ để tìm danh sách BLV
        response = requests.get('https://bunchatv4.net/', headers=header, timeout=15)
        content = response.text
        
        # 2. Tìm các link BLV (binh-luan-vien/...)
        links = re.findall(r'href="([^"]*binh-luan-vien/[^"]*)"', content)
        # Loại bỏ trùng lặp và lọc bỏ "nhà đài"
        links = list(set([l for l in links if "nha-dai" not in l.lower()]))
        
        for l in links:
            url = 'https://bunchatv4.net' + l if l.startswith('/') else l
            # Tạo tên từ slug (ví dụ: blv-rio -> Blv Rio)
            name = l.split('/')[-1].replace('-', ' ').title()
            
            try:
                # 3. Vào trang chi tiết của từng BLV để bóc link m3u8
                detail = requests.get(url, headers=header, timeout=10).text
                # Tìm link m3u8 (loại bỏ các dấu gạch chéo ngược nếu có)
                stream = re.findall(r'(https?://[\w\.-]+[:\d]*/[\w\.-/]+\.m3u8[^\s"\'<>]*)', detail)
                
                if stream:
                    clean_link = stream[0].replace("\\", "")
                    m3u += f'#EXTINF:-1, [Royx] {name}\n{clean_link}\n'
            except:
                continue
                
    except Exception as e:
        print(f"Lỗi rồi: {e}")
    
    # 4. Ghi file với cấu trúc chuẩn để App không bị lỗi "Không có kênh"
    with open('live.m3u', 'w', encoding='utf-8') as f:
        f.write(m3u.strip() + '\n')

if __name__ == "__main__":
    run()
