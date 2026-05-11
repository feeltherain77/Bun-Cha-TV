import requests, re, os

def run():
    h = {'User-Agent': 'Mozilla/5.0'}
    b_list = ""
    try:
        r = requests.get('https://bunchatv4.net/', headers=h, timeout=15).text
        links = re.findall(r'href="([^"]*binh-luan-vien/[^"]*)"', r)
        for l in set(links):
            if "nha-dai" in l.lower(): continue
            u = 'https://bunchatv4.net' + l if l.startswith('/') else l
            name = l.split('/')[-1].replace('-', ' ').title()
            try:
                d = requests.get(u, headers=h, timeout=10).text
                s = re.findall(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', d)
                if s: b_list += f'#EXTINF:-1, [Bún Chả] {name}\n{s[0].replace("\\", "")}\n'
            except: pass
    except: pass

    old = ""
    if os.path.exists('live.m3u'):
        with open('live.m3u', 'r', encoding='utf-8') as f: old = f.read()
    
    lines = old.split('\n')
    new = []
    skip = False
    for line in lines:
        if "#EXTINF" in line and "[Bún Chả]" in line: skip = True
        elif skip and ("http" in line or ".m3u8" in line): skip = False
        elif not skip: new.append(line)

    final = "\n".join(new).strip() + "\n" + b_list.strip()
    with open('live.m3u', 'w', encoding='utf-8') as f:
        txt = final.strip()
        if not txt.startswith("#EXTM3U"): txt = "#EXTM3U\n" + txt
        f.write(txt + "\n")

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
