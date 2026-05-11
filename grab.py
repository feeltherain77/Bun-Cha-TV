import requests
import re

def run():
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Referer': 'https://bunchatv4.net/'
    }
    m3u = '#EXTM3U\n'
    
    try:
        # 1. Quét trang chủ
        content = requests.get('https://bunchatv4.net/', headers=header, timeout=15).text
        # Tìm các link có chữ "binh-luan-vien"
        links = re.findall(r'href="([^"]*binh-luan-vien/[^"]*)"', content)
        links = list(set([l for l in links if "nha-dai" not in l.lower()]))
        
        if not links:
            print("Không tìm thấy BLV nào.")
            
        for l in links:
            url = 'https://bunchatv4.net' + l if l.startswith('/') else l
            name = l.split('/')[-1].replace('-', ' ').title()
            
            try:
                # 2. Vào trang chi tiết
                detail = requests.get(url, headers=header, timeout=10).text
                # Regex mới: Soi tất cả những gì có đuôi .m3u8, chấp cả gạch chéo ngược
                streams = re.findall(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', detail)
                
                if streams:
                    # Lấy link đầu tiên tìm được, dọn dẹp sạch sẽ
                    clean_link = streams[0].replace("\\", "")
                    m3u += f'#EXTINF:-1, [Royx] {name}\n{clean_link}\n'
                    print(f"Đã húp được link của: {name}")
            except:
                continue
                
    except Exception as e:
        print(f"Lỗi: {e}")
    
    # 3. Ghi file - Đảm bảo có nội dung
    if m3u == '#EXTM3U\n':
        m3u += '#EXTINF:-1, Dang cho tran dau tiep theo...\nhttps://127.0.0.1/error.m3u8\n'
        
    with open('live.m3u', 'w', encoding='utf-8') as f:
        f.write(m3u.strip() + '\n')

if __name__ == "__main__":
    run()
                
    except Exception as e:
        print(f"Lỗi rồi: {e}")
    
    # 4. Ghi file với cấu trúc chuẩn để App không bị lỗi "Không có kênh"
    with open('live.m3u', 'w', encoding='utf-8') as f:
        f.write(m3u.strip() + '\n')

if __name__ == "__main__":
    run()
