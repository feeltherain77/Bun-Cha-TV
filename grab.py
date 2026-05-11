import requests
import re
import time
import random
from urllib.parse import quote

# Cấu hình giả lập và lách luật
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
REF = 'https://bunchatv4.net/'

def run_grab():
    # Ngủ ngẫu nhiên từ 1-30s để web không quét ra bot
    time.sleep(random.randint(1, 30))
    
    m3u_text = '#EXTM3U\n'
    h = {'User-Agent': UA, 'Referer': REF}
    
    try:
        # 1. Quét trang chủ lấy danh sách trận
        r = requests.get(REF, headers=h, timeout=15).text
        links = set(re.findall(r'href="([^"]*truc-tiep/[^"]*)"', r))
        
        print(f"Đang quét {len(links)} trận đấu...")

        for m_url in links:
            full_u = REF + m_url if m_url.startswith('/') else m_url
            try:
                # 2. Vào từng trận bóc link m3u8 và BLV
                d = requests.get(full_u, headers=h, timeout=10).text
                stream_links = re.findall(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', d)
                
                if stream_links:
                    # Bóc tên trận từ thẻ h1, lọc rác
                    t = re.search(r'<h1.*?>(.*?)</h1>', d, re.S)
                    match_name = re.sub('<[^<]+?>', '', t.group(1)).strip().split('|')[0].replace('Trực tiếp', '').strip() if t else "Bóng đá"

                    # Bóc tên BLV/Server từ nội dung trang
                    blv_list = re.findall(r'(?:BLV|Kênh|Server|S)[:\s]+([^<"\']+)', d)
                    
                    for i, link in enumerate(stream_links):
                        raw_link = link.replace("\\", "")
                        blv_tag = blv_list[i].strip() if i < len(blv_list) else f"Server {i+1}"
                        
                        # Tên hiển thị cuối cùng
                        display_name = f"{match_name} ({blv_tag})"
                        
                        # Gắn Header "chống 403" cho OTT Navigator
                        final_link = f"{raw_link}|User-Agent={quote(UA)}&Referer={quote(REF)}&Origin={quote(REF)}"
                        
                        m3u_text += f'#EXTINF:-1 tvg-name="{display_name}" group-title="Bún Chả TV", {display_name}\n{final_link}\n'
            except: continue
    except Exception as e:
        print(f"Lỗi hệ thống: {e}")

    # 3. Xuất file
    with open('live.m3u', 'w', encoding='utf-8') as f:
        f.write(m3u_text)
    print("Đã cập nhật file live.m3u thành công!")

if __name__ == "__main__":
    run_grab()
                        
                        m3u_text += f'#EXTINF:-1 tvg-name="{display_name}" group-title="Bún Chả TV", {display_name}\n{final_link}\n'
                        print(f"Đã húp: {display_name}")
            except: continue
    except: pass

    with open('live.m3u', 'w', encoding='utf-8') as f:
        f.write(m3u_text)

if __name__ == "__main__":
    run_grab()
  
