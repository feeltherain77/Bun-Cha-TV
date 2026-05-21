import requests
import re
from urllib.parse import urljoin

# Cấu hình thông tin cấu trúc
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
BASE_URL = 'https://sv2.thiendinh3.live/'
TRANG_CHU = urljoin(BASE_URL, 'trang-chu')

def get_m3u():
    m3u_lines = ["#EXTM3U"]
    headers = {
        'User-Agent': UA,
        'Referer': BASE_URL
    }
    processed_urls = set()

    try:
        # 1. LẤY LOGO CHÍNH CHỦ TỪ WEB THIÊN ĐÌNH
        response = requests.get(TRANG_CHU, headers=headers, timeout=10)
        html = response.text
        
        logo_match = re.search(r'src="([^"]*logo[^"]*)"', html, re.IGNORECASE)
        web_logo = urljoin(BASE_URL, logo_match.group(1)) if logo_match else urljoin(BASE_URL, 'assets/images/logo.png')

        # 2. QUÉT TRẬN ĐẤU TRÊN TRANG CHỦ
        # Tìm các thẻ <a> chứa liên kết trận đấu và nội dung bên trong
        matches = re.findall(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', html, re.IGNORECASE | re.DOTALL)

        for href, content in matches:
            match_url = href.strip()
            
            # Chỉ lấy các link dẫn vào phòng xem trận đấu
            if not any(k in match_url for k in ['/match/', '/live/', '/truc-tiep/', '/xem']):
                continue
                
            match_url = urljoin(BASE_URL, match_url)
            
            # Tránh trùng lặp trận
            if match_url in processed_urls:
                continue
            processed_urls.add(match_url)

            # Làm sạch mã HTML trong nội dung thẻ <a> để lấy chữ công khai
            clean_content = re.sub(r'<[^>]+>', ' ', content)
            clean_content = re.sub(r'\s+', ' ', clean_content).strip()
            
            if len(clean_content) < 5:
                continue

            # ⏳ Bóc tách giờ đá (Định dạng xx:xx)
            time_match = re.search(r'(\d{2}:\d{2})', clean_content)
            match_time = time_match.group(1) if time_match else "LIVE"

            # 🎙️ Bóc tách tên bình luận viên
            blv_match = re.search(r'(BLV\s+[^\s|]+)', clean_content, re.IGNORECASE)
            blv_name = blv_match.group(1).strip() if blv_match else "Mỳ Tôm"

            # 🖼️ Bóc tách ảnh thumbnail/logo của trận đấu đó
            thumb_match = re.search(r'(?:src|data-src)="([^"]+)"', content)
            match_thumb = urljoin(BASE_URL, thumb_match.group(1)) if thumb_match else web_logo

            # ⚽ Lọc ra tên sạch của trận đấu (Tên đội 1 vs Tên đội 2)
            match_name = clean_content.replace(match_time, "").replace(blv_name, "").strip()
            match_name = " ".join(match_name.split()).strip('- ')
            if not match_name or len(match_name) < 3:
                match_name = "Trận Đấu Đang Diễn Ra"

            # Định dạng tên hiển thị lên list IPTV
            display_name = f"⚽ {match_name} [{match_time}] - BLV {blv_name}"

            # 👑 ĐÚC FILE THEO ĐỊNH DẠNG IPTV (.M3U) CHUẨN ĐÉT CHO MONPLAYER
            m3u_lines.append(f'#EXTINF:-1 tvg-logo="{match_thumb}" group-title="🔴 Live Bóng Đá Today", {display_name}')
            m3u_lines.append(match_url)

    except Exception as e:
        print(f"Lỗi rồi ông giáo ơi: {e}")

    # Nếu không quét được trận nào thì tạo 1 kênh cứu cánh dẫn về trang chủ
    if len(m3u_lines) == 1:
        m3u_lines.append(f'#EXTINF:-1 tvg-logo="https://sv2.thiendinh3.live/assets/images/logo.png" group-title="Thiên Đình TV", [LIVE] Vào trang chủ Thiên Đình TV')
        m3u_lines.append(TRANG_CHU)

    # Ghi toàn bộ dữ liệu ra file list.m3u
    with open("list.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(m3u_lines))

if __name__ == "__main__":
    get_m3u()
    
