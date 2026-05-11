import requests, re

def run():
    h = {'User-Agent': 'Mozilla/5.0'}
    m = '#EXTM3U\n'
    # 1. Lấy danh sách link BLV
    r = requests.get('https://bunchatv4.net/', headers=h).text
    links = list(set(re.findall(r'href="([^"]*binh-luan-vien/[^"]*)"', r)))
    
    for l in links:
        if "nha-dai" in l: continue
        u = 'https://bunchatv4.net' + l if l.startswith('/') else l
        name = l.split('/')[-1].replace('-', ' ').title()
        # 2. Vào từng link lấy m3u8
        d = requests.get(u, headers=h).text
        s = re.findall(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', d)
        if s:
            link = s[0].replace("\\", "")
            m += f'#EXTINF:-1, [Bún Chả] {name}\n{link}\n'
            
    # 3. Ghi file (Ghi đè hoàn toàn)
    with open('live.m3u', 'w', encoding='utf-8') as f:
        f.write(m.strip() + '\n')

if __name__ == "__main__":
    run()
  
