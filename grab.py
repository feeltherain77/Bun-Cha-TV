import requests
import re
import os

def run():
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Referer': 'https://bunchatv4.net/'
    }
    
    # 1. Bóc link từ Bún Chả
    list_buncha = ""
    try:
        home = requests.get('https://bunchatv4.net/', headers=header, timeout=15).text
        links = re.findall(r'href="([^"]*binh-luan-vien/[^"]*)"', home)
        links = list(set([l for l in links if "nha-dai" not in l.lower()]))
        
        for l in links:
            url = 'https://bunchatv4.net' + l if l.startswith('/') else l
            name = l.split('/')[-1].replace('-', ' ').title()
            detail = requests.get(url, headers=header, timeout=10).text
            streams = re.findall(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', detail)
            if streams:
                clean_link = streams[0].replace("\\", "")
                list_buncha += f'#EXTINF:-1, [Bún Chả] {name}\n{clean_link}\n'
    except:
        pass

    # 2. Đọc nội dung file cũ nếu có
    old_content = ""
    if os.path.exists('live.m3u'):
        with open('live.m3u', 'r', encoding='utf-8') as f:
            old_content = f.read()
    
    if not old_content.strip():
        old_content = "#EXTM3U\n"

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
