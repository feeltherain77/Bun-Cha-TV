import requests, re, os

def run():
    h = {'User-Agent': 'Mozilla/5.0'}
    b_list = ""
    # Bước 1: Quét link Bún Chả
    try:
        r = requests.get('https://bunchatv4.net/', headers=h, timeout=15).text
        links = list(set(re.findall(r'href="([^"]*binh-luan-vien/[^"]*)"', r)))
        for l in links:
            if "nha-dai" in l.lower(): continue
            u = 'https://bunchatv4.net' + l if l.startswith('/') else l
            name = l.split('/')[-1].replace('-', ' ').title()
            d = requests.get(u, headers=h, timeout=10).text
            s = re.findall(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', d)
            if s: b_list += f'#EXTINF:-1, [Bún Chả] {name}\n{s[0].replace("\\", "")}\n'
    except: pass

    # Bước 2: Đọc list cũ (VTV, K+...)
    old = ""
    if os.path.exists('live.m3u'):
        with open('live.m3u', 'r', encoding='utf-8') as f: old = f.read()
    
    # Bước 3: Lọc bỏ Bún Chả cũ để không bị trùng
    lines = old.split('\n')
    new = [line for line in lines if "[Bún Chả]" not in line and not line.startswith('http')]
    
    # Bước 4: Gộp lại
    final = "#EXTM3U\n" + "\n".join([l for l in new if "#EXTM3U" not in l]).strip() + "\n" + b_list.strip()
    with open('live.m3u', 'w', encoding='utf-8') as f:
        f.write(final.strip() + "\n")

if __name__ == "__main__":
    run()

if __name__ == "__main__":
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
