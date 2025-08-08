# <name>-basic-training

## 一、PyCharm 基礎操作

### 1. 這是什麼

>功能強大的Python 整合式開發環境（IDE）

### 2. 怎麼使用它

* 新增專案  
  * 左上角File > New Project > 選擇開啟哪一種專案 > create

* 新增檔案
  * 右上角New File or Directory > 選擇甚麼類型的檔案(副檔名) > python
  * 選項有三種：python file、python unit test、python stub，通常選python file就好

* 執行程式
  * 程式頁面右鍵 > 點選RUN'檔名'，或者切換右上角程式然後ctrl+shift+f10

* debugger
  * 點擊行號設置breakpoint後，到程式頁面右鍵 > 點選debugger'檔名'，或者切換右上角程式然後shift+f9，進入debugger模式之後按f8逐行執行並觀察變數值

* 設定執行參數
  * 左上角選單 > RUN>Edit Configuration > 選擇程式 > 在script parameters填入參數，這樣下次執行程式就會帶入這些參數了

* 快速尋找方法或參數
  * 游標停在function或class上 > ctrl+B可以找到它的定義方式
  * 相反也可以找誰使用這個function或class，在該method上右鍵 > find usage (alt+f7)

* 快速縮排
  * ctrl+alt+L

* 配置虛擬環境
  * 點右下角管理interpreter和新增interpreter這個頁面可以查看當前的虛擬環境為何，新增虛擬環境或選擇現有的虛擬環境、管理環境內的套件
* poetry建立流程
  1. 修改config，讓虛擬環境可以建在專案裡  
  `poetry config --list`查看設定，`virtualenvs.in-project`是我們要修改的目標，輸入`poetry config virtualenvs.in-project = true`
  2. 到專案目錄建一個poetry_env/，從terminal進到目錄裡輸入`poetry init`，會產生pyproject.toml檔案，tomel檔會記錄安裝的套件，假設安裝flask，這裡就只會顯示`flask (>=3.1.1,<4.0.0)`，poetry的好處就在他會區分哪些是我們主動安裝的套件，以及那些是基於此套件安裝的相依套件
  3. 輸入`poetry env use python`建立虛擬環境(出現.env)，輸入`protry shell`進入虛擬環境，但是終端機跟上方程式是分開的，要點右下角`add new interpreter` > `add local interpreter` > `select existing`，`path to poetry`是poetry下載後的原始路徑可以用poetry ，`poetry env use`是剛剛創的poetry_env/.venv/script/python，這樣pycharm就可以讀到這個虛擬環境了
* requirement.txt的匯出與匯入:
  * poetry 
    * 匯出  
`poetry export -f requirements.txt --output requirements.txt --without-hashes`  
 以上指令會把 pyproject.toml 內的 dependencies 匯出成 pip 用的格式
    * 匯入(poetry 基本不使用requirement.txt，用pyproject.toml)  
    `git clone https://github.com/someone/awesome-project.git`  
    `cd awesome-project`  
    `poetry install`
  * pip
    * 匯出  
      `pip freeze > requirements.txt`
    * 匯入  
      `pip install -r requirements.txt`
### 3. 為什麼需要它

...

## 二、Python 程式基礎

### 1. 資料結構（List / Dict / Set / Tuple）
#### set的特性：
#### 唯一性:set中的元素不能重複，重複的元素會被刪除
#### 只要是不可變的、可hash的都可以放進set，像list、dict、set就不能放進set
#### 相關函式：len(s), s.add(), s.remove(), s.discard(), s.clear(), s.union(), s.intersection(), s.difference()
#### discard和remove的差別:如果該元素不存在，discard不會報錯

#### List的特性：有序性
#### 建立陣列的方式：1.放入中括號並以逗點隔開:2.使用List()將iterable(for i in ...)的物件轉成List，像字串、tuple、dict； 3.split()可以將一個字串根據特定的分割符號，拆分成list
...

### 2. 函式與引數

...

### 3. 模組與封裝

...

## 三、Git 基本操作

### 1. Git 是什麼

...

### 2. 如何使用

...

### 3. 常見操作說明

...

## 四、附錄：程式碼範例

- `bmi.py`：BMI 計算器，支援命令列參數
- `log_example.py`：日誌記錄與輸出
- `env_example.py`：如何使用 `.env` 管理環境變數

