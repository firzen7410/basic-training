## 爬蟲架構

### 主要由以下四個class所組成

1. BaseScraper
    - 提供基礎操作方法給 Scraper 使用。
    - 功能包括：等待元素載入、尋找元素、滾動到指定元素、點擊元素、抓取頁面原始碼等。
    - 負責處理 Selenium 低層細節，減少 Scraper class 的重複程式碼。
2. Scraper
    - 繼承BaseScraper。
    - 控制爬蟲流程，安排點擊元素的順序與邏輯。
    - 支援多板抓取、翻頁操作、刪文判斷、未滿 18 歲頁面處理等。
<<<<<<< HEAD
    - 內建 max_runtime 機制，可設定爬蟲自動停止，避免瀏覽器殘留。
=======
    - max_runtime 機制，可設定爬蟲自動停止，避免瀏覽器殘留。
>>>>>>> 4f4dad3 ('重置')
3. PttParse
    - 負責使用beautifulsoup解析網頁內容
    - 貼文解析回傳一個 dict，留言解析回傳多則 dict 包成 list。
    - 支援解析文章標題、作者、內容、日期及留言狀態。
4. DataBaseHandler
    - 處理資料庫連線與資料插入。
    - 接收 Scraper 或 PttParser 傳來的資料後插入資料庫表格（posts、comments、logs 等）。
    - 提供 log 插入功能，支援 task_name、狀態、訊息、時間等欄位。

<<<<<<< HEAD
=======
## API 規格

## BASE URL

http://127.0.0.1:8000/

GET /api/posts

查詢參數

| 參數             | 型別  | 必填 | 預設 | 描述                  |
|----------------|-----|----|----|---------------------|
| `limit`        | int | 否  | 50 | 每頁筆數，1–100          |
| `page`         | int | 否  | 1  | 頁碼                  |
| `author`       | str | 否  | -  | 篩選發文者 (模糊查詢)        |
| `board`        | str | 否  | -  | 篩選看板名稱              |
| `created_date` | str | 否  | -  | 篩選發文日期 (YYYY-MM-DD) |
| `created_time` | str | 否  | -  | 篩選發文時間 (HH:MM:SS)   |
| `keyword`      | str | 否  | -  | 搜尋標題或內文             |

**Response 200**

```json
{
  "page": 1,
  "limit": 50,
  "total_count": 20802,
  "total_pages": 417,
  "prev_query": {
    "page": "1"
  },
  "next_query": {
    "page": "2"
  },
  "keyword": null,
  "posts": [
    {
      "id": 20818,
      "title": "[菜單] 60k遊戲機(4k畫質)",
      "author": "idoxo (MikeLiu)",
      "board": "PC_Shopping",
      "created_date": "2025-09-17",
      "created_time": "14:21:36",
      "content": "\n已買/未買/已付訂金（元）：未買\n\n預算/用途：60k\n3A大作4k順跑，畫質希望在中高以上\n單機為主，比較喜歡動作遊戲\n\nCPU (中央處理器)：AMD【8核】Ryzen7 7700\nMB      (主機板)：【任搭CPU】華碩 TUF GAMING B650-E WIFI\nRAM     (記憶體)：十銓 TEAM T-CREATE EXPERT DDR5-6000 32G(16G*2)-黑\nVGA     (顯示卡)：華碩 PRIME-RTX5080-16G\nCooler  (散熱器)：ID-COOLING FROZN A620 PRO SE ARGB 黑\nSSD   (固態硬碟)：鎧俠 KIOXIA EXCERIA PLUS G3 2TB\nHDD       (硬碟)：\nPSU (電源供應器)：MONTECH TITAN 850W\nCHASSIS   (機殼)：darkFlash DS900 黑\nMONITOR   (螢幕)：\nMouse/KB  (鼠鍵)：\nOS    (作業系統)：\n\n其它      (自填)：\n總價 (未稅/含稅)：59,638\n\n注意1：自稱小妹或會透露自己性別的舉動要注意可能會引來不必要的紛擾，請注意。\n注意2：標題是否有寫明\"預算\"、\"用途\"? 沒有請按Ctrl+x 然後按T改標題\n注意3：請多加利用線上估價系統來進行估價以及價格查詢 (僅供參考)\n注意4：若遇新品問題請勿發除錯文，請直接回原購買處處理。\n\n   國內網路通路連結。請以文字敘述。\n\n\n   菜單文與情報文，禁止任何估價系統連結與擷圖、包含文字估價單號碼。\n   (參閱板規1-2-3、1-3-9)\n   違反者:刪文、水桶十日。\n\n注意5：為保障您的權益，購物消費請索取統一發票，並盡量以含稅價取貨\n注意6：若有任何問題請先洽詢板務。\n\n--\n"
    },
>>>>>>> 4f4dad3 ('重置')
