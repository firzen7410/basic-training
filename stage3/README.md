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
    - 內建 max_runtime 機制，可設定爬蟲自動停止，避免瀏覽器殘留。
3. PttParse
    - 負責使用beautifulsoup解析網頁內容
    - 貼文解析回傳一個 dict，留言解析回傳多則 dict 包成 list。
    - 支援解析文章標題、作者、內容、日期及留言狀態。
4. DataBaseHandler
    - 處理資料庫連線與資料插入。
    - 接收 Scraper 或 PttParser 傳來的資料後插入資料庫表格（posts、comments、logs 等）。
    - 提供 log 插入功能，支援 task_name、狀態、訊息、時間等欄位。

