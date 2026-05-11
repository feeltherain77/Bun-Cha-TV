name: Update M3U 23m
on:
  schedule:
    - cron: '*/23 * * * *' # Chạy tự động mỗi 23 phút
  workflow_dispatch:      # Nút bấm tay cho Mạnh khi MU đá

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: pip install requests

      - name: Run grabber
        run: python grab.py

      - name: Commit and Push
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add live.m3u
          git commit -m "Update playlist - 23m cycle" || exit 0
          git push

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
  
