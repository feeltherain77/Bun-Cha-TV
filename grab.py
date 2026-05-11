import requests
import re

def run():
    # Giả lập trình duyệt để không bị web chặn
    h = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    m3u = '#EXTM3U\n'
    
    try:
        # 1. Lấy danh sách BLV từ trang chủ
        r = requests.get('https://bunchatv4.net/', headers=h, timeout=15).text
        links = re.findall(r'href="([^"]*binh-luan-vien/[^"]*)"', r)
        
        # 2. Quét từng ông BLV (loại bỏ nhà đài)
        for l in set(links):
            if "nha-dai" in l.lower(): continue
            u = 'https://bunchatv4.net' + l if l.startswith('/') else l
            name = l.split('/')[-1].replace('-', ' ').title()
            
            try:
                # 3. Bóc link m3u8 trong trang chi tiết
                d = requests.get(u, headers=h, timeout=10).text
                s = re.findall(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', d)
                if s:
                    link = s[0].replace("\\", "")
                    m3u += f'#EXTINF:-1, [Bún Chả] {name}\n{link}\n'
            except:
                continue
    except:
        pass

    # 4. Ghi đè file mới hoàn toàn
    with open('live.m3u', 'w', encoding='utf-8') as f:
        f.write(m3u.strip() + '\n')

if __name__ == "__main__":
    run()
    run()

    # 3. Lọc bỏ các dòng Bún Chả cũ để không bị trùng link mỗi lần chạy
    lines = old_content.split('\n')
    new_lines = []
    skip = False
    for line in lines:
        if "#EXTINF" in line and "[Bún Chả]" in line:
            skip = True
            continue
        if skip and ("http" in line or ".m3u8" in line):
            skip = False
            continue
        if not skip:
            new_lines.append(line)

    # 4. Ghép nối và lưu lại
    final_m3u = "\n".join(new_lines).strip() + "\n"
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
