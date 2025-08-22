# PTT爬蟲與資料展示系統

## 專案簡介

本專案實作一個 資料蒐集 > 儲存 > API > 前端展示 的完整流程。

功能包含：

- PTT 爬蟲：每小時自動爬取指定五個看板的最新文章
- 資料庫儲存：透過 MariaDB (docker-compose) 儲存爬取的文章資料
- RESTful API (FastAPI)：提供文章的查詢、新增、修改、刪除等功能
- 前端頁面 (Jinja2 Template)：透過簡單的靜態頁面展示文章與統計資訊
- 測試 (pytest)：針對爬蟲與 API 撰寫單元測試與 CRUD 測試
- 排程 (Celery + Celery Beat)：自動化定時執行爬蟲
- 容器化部屬 (docker-compose)：快速啟動所有服務

運作流程

1. Celery Beat 排程
    - 每小時觸發一次爬蟲任務
    - 爬取指定五個 PTT 看板 (過去一年內文章 + 最新文章)
    - 新文章寫入 posts 資料表，並在 logs 中記錄任務執行情況
2. FastAPI 提供 API
    - /api/posts：查詢最新文章、分頁、條件過濾 (作者、時間、看板)
    - /api/posts/{id}：查詢單篇文章
      -/api/statistics：文章統計 (時間範圍、看板、作者)
3. 前端頁面 (Jinja2)
    - /posts：最新 50 筆文章列表，可分頁/篩選
    - /posts/{id}：文章詳細頁
    - /statistics：統計頁面 (文章數量、看板分布)
4. pytest 測試
    - API CRUD 測試 (新增、修改、刪除、查詢)
    - 爬蟲模擬測試 (是否能正確解析文章)

資料表設計

post表格

| 欄位名稱       | 資料型態                      | 說明                |
|------------|---------------------------|-------------------|
| pid        | varchar(50) (primary key) | 以文章檔名作為pid(url後綴) |
| board      | varchar(50)               | 看板名稱              |
| title      | varchar(255)              | 文章標題              |
| author     | varchar(100)              | 作者帳號              |
| content    | TEXT                      | 內文                |
| created_at | DATETIME                  | 發文時間              |
| url        | varchar(255)              | 文章連結              |

logs表格

| 欄位名稱       | 資料型態              | 說明           |
|------------|-------------------|--------------|
| lid        | int (primary key) | LogID 流水號    |
| task_name  | varchar(100)      | 任務名稱         |
| status     | varchar(20)       | success/fail |
| message    | TEXT              | 錯誤訊息或摘要      |
| execute_at | DATETIME          | 執行時間         |

post_log

| 欄位名稱       | 資料型態                  | 說明                       |
|------------|-----------------------|--------------------------|
| pid        | varchar(50) (PK & FK) | references from post的pid |
| lid        | int(PK & FK)          | references from log的lid  |
| crawled_at | DATETIME              | 爬取時間                     |

開發時程規劃 (三週)

- Week 1 - 系統架構規劃與爬蟲
    - 設計資料表 (posts, logs)
    - 寫 PTT 爬蟲 (OOP 抽象化，支援多個看板)
    - 建立 Celery 排程，定時執行爬蟲
    - docker-compose 建立 MariaDB + FastAPI 開發環境
    - README.md 撰寫初版 (架構、流程、資料表設計)

- Week 2 - API 開發與測試
    - 建立 FastAPI 專案架構
    - API CRUD (GET, POST, PUT, DELETE)
    - /statistics 統計 API
    - 使用 Pydantic 進行資料驗證
    - 撰寫 pytest 測試 (API CRUD + 爬蟲單元測試)

- Week 3 - 前端與部屬
    - 撰寫 Jinja2 Template (文章列表、詳細、統計頁)
    - API 與前端整合
    - 測試 Celery 任務能穩定執行三天 (log 驗證)
    - 撰寫最終 README.md (含部署文件)
    - docker-compose 部屬 (DB + Backend + Worker)