import requests
import re
from urllib.parse import quote

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
REF = 'https://bunchatv4.net/'

def run_grab():
    m3u_text = '#EXTM3U\n'
    h = {'User-Agent': UA, 'Referer': REF}
    
    try:
        r = requests.get(REF, headers=h, timeout=15).text
        links = set(re.findall(r'href="([^"]*truc-tiep/[^"]*)"', r))
        
        for m_url in links:
            full_u = REF + m_url if m_url.startswith('/') else m_url
            try:
                d = requests.get(full_u, headers=h, timeout=10).text
                # Tìm tất cả link m3u8 trong trang (vì một trận có thể có nhiều server/BLV)
                stream_links = re.findall(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', d)
                
                if stream_links:
                    # 1. Bóc tên trận cơ bản
                    t = re.search(r'<h1.*?>(.*?)</h1>', d, re.S)
                    match_name = re.sub('<[^<]+?>', '', t.group(1)).strip().split('|')[0].replace('Trực tiếp', '').strip() if t else "Bóng đá"

                    # 2. Bóc tên BLV (Thường nằm trong thẻ span hoặc class bình luận viên)
                    # Web này hay để kiểu: "Server BLV Batman" hoặc "K+ Sport (BLV Anh Quân)"
                    blv_list = re.findall(r'(?:BLV|Kênh|Server)[:\s]+([^<"\']+)', d)
                    
                    for i, link in enumerate(stream_links):
                        raw_link = link.replace("\\", "")
                        
                        # Thử gán tên BLV cho từng link nếu tìm thấy
                        blv_name = blv_list[i].strip() if i < len(blv_list) else f"Link {i+1}"
                        
                        # Tên hiển thị cuối cùng: Tên Trận - BLV
                        display_name = f"{match_name} ({blv_name})"
                        
                        final_link = f"{raw_link}|User-Agent={quote(UA)}&Referer={quote(REF)}&Origin={quote(REF)}"
                        
                        m3u_text += f'#EXTINF:-1 tvg-name="{display_name}" group-title="Bún Chả TV", {display_name}\n{final_link}\n'
                        print(f"Đã húp: {display_name}")
            except: continue
    except: pass

    with open('live.m3u', 'w', encoding='utf-8') as f:
        f.write(m3u_text)

if __name__ == "__main__":
    run_grab()
  
