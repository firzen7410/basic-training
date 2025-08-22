# <name>-basic-training

## 一、PyCharm 基礎操作

### 1. 這是什麼

> 功能強大的Python 整合式開發環境（IDE）

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
* 設定執行環境變數
    * 左上角選單 > RUN>Edit Configuration > 選擇程式 > 在environment variable加入，讀取sys.argv就可以取得環境變數了
* 快速尋找方法或參數
    * 游標停在function或class上 > ctrl+B可以找到它的定義方式
    * 相反也可以找誰使用這個function或class，在該method上右鍵 > find usage (alt+f7)
* 快速縮排
    * ctrl+alt+L

* 配置虛擬環境
    * 點右下角管理interpreter和新增interpreter這個頁面可以查看當前的虛擬環境為何，新增虛擬環境或選擇現有的虛擬環境、管理環境內的套件
* poetry建立流程
    1. 修改config，讓虛擬環境可以建在專案裡  
       `poetry config --list`查看設定，`virtualenvs.in-project`是我們要修改的目標，輸入
       `poetry config virtualenvs.in-project = true`
    2. 到專案目錄建一個poetry_env/，從terminal進到目錄裡輸入`poetry init`
       ，會產生pyproject.toml檔案，tomel檔會記錄安裝的套件，假設安裝flask，這裡就只會顯示`flask (>=3.1.1,<4.0.0)`
       ，poetry的好處就在他會區分哪些是我們主動安裝的套件，以及那些是基於此套件安裝的相依套件
    3. 輸入`poetry env use python`建立虛擬環境(出現.env)，輸入`protry shell`進入虛擬環境，但是終端機跟上方程式是分開的，要點右下角
       `add new interpreter` > `add local interpreter` > `select existing`，`path to poetry`
       是poetry下載後的原始路徑可以用poetry ，`poetry env use`是剛剛創的poetry_env/.venv/script/python，這樣pycharm就可以讀到這個虛擬環境了
* requirement.txt的匯出與匯入:
    * poetry
        * 匯出  
          `poetry export -f requirements.txt --output requirements.txt --without-hashes`  
          以上指令會把 pyproject.toml 內的 dependencies 匯出成 pip 用的格式
        * 匯入(poetry 基本不使用requirement.txt，用pyproject.toml)  
          `git clone gitLink`  
          `cd project`  
          `poetry install`
    * pip
        * 匯出  
          `pip freeze > requirements.txt`
        * 匯入  
          `pip install -r requirements.txt`

### 3. 為什麼需要它

* 用於開發程式，相比vscode有不少功能已整合在一起，如虛擬環境，debugger，自動縮排

## 二、Python 程式基礎

### 1. 資料結構（List / Dict / Set / Tuple）

* set
    * 特性：
        * set中的元素不能重複，重複的元素會被刪除
        * 屬於可變，定義好之後可以增減元素
        * 沒有順序，每次印出可能不同
        * 只要是不可變的且可hash的都可以放進set，像是int, string, tuple，反之像list、dict、set就不能放進set

* List
    * 有序性
    * 可放入重複
    * 屬於可變，定義好之後可以增減元素
    * 可放入任何資料型態的元素
    * 建立陣列的方式：
        1. 放入中括號並以逗點隔開
        2. 使用List()將iterable(for i in ...)
           的物件轉成List，像字串、tuple、dict，那甚麼是iterable？就是目標物件具有__iter__()或是__getitem__()
           方法，即使是自訂的物件也可以透過list()轉成list
            * 我自訂了一個student
              class，並定義了__iter__這個method，這裡比較偷吃步，我是先把name跟age包成一個tuple再透過iter()
              呼叫tuple的__iter__()
              method，回傳一個迭代器object，關於這個迭代器，由於最底層實作方式是CPython，有點複雜，暫時先關注這個iterator能做甚麼就好，list()
              就相當於利用iterator做append的動作，使傳入的物件變成list
        3. split()可以將一個字串根據特定的分割符號，拆分成list，這算是專門為string服務的function，其他人要用就得先轉乘string
* tuple
    * 有序性
    * 可放入重複
    * 屬於不可變，但是如果放入可變的資料型態，如list，set..等，還是可以改動元素內的值
    * 可放入任何資料型態的值
* dictionary
    * 無序
    * key值必須唯一，且不可變，value可以是任意資料型態
    * dict底層使用hash table實作
    * hash table
        * 將key值經過hash function後，得到index(hash值)
          ，而我們的table就是紀錄index和key的對應關係，但是不同key值hash過可能會對應到相同index，稱為碰撞，因此hash table
          加入link list使用指標指到新加入key值

### 2. 函式與引數

* Positional Arguments
    * 呼叫的時候按照函式定義的順序傳入
* keyword arguments
    * 呼叫的時候針對要使用的引數傳入參數，可以隨意放置參數，較為靈活
* 函式可以設定預設值，當該參數未被傳入時使用預設值，當有傳入時覆蓋，未設定預設值為必要參數
    * 必要參數一定要放在有預設值參數的前面，否則會syntax error
    * 若是positional argument和keyword argument混用，則positional必須放在keyword argument前面
* unpacking
    * `*`可以用來拆解可迭代的物件，像list, tuple, set, str，或任何有__item__()的物件
    * `**`可以用來拆解有key-value這種映射關係的物件，最常見就dict或任何有.key(), .item()的物件
    * 配合positional argument或keyword argument可以用來傳遞或接收不定數量的參數

### 3. 模組與封裝

* 使用import 檔名.py，程式內使用檔名.function就可以使用
* 為什麼需要__name__='main':
    * 主要用在module的程式裡，讓使用module的其他程式部會執行到main裡面的內容，區分的作用

### 4. python延伸練習

* logging
* python命名
    * Package（套件）
        * 全小寫
        * 可用底線 `_` 分隔，單字為主
        * 名詞為主，簡短且有意義
    * Class
        * PascalCase（首字母大寫的駝峰式）
    * function
        * 全小寫
        * 單字之間用底線隔開
    * Variable
        * 全小寫
        * 單字之間用底線分隔

單字之間用底線 _ 分隔

## 三、Git 基本操作

* 在git中檔案有四種狀態，untracked, unmodified, modified, staged
    * 使用git add 將untracked檔案移到stage
    * 使用git commit -m "訊息" 可以提交版本訊息，建立新版本
    * 使用git push 將本地端commit的repo發佈到遠端
* 流程
    1. 在github創建遠端儲存庫
    2. 本地專案terminal輸入`git init`
    3. `git add .`將檔案加入追蹤
    4. `git commit -M main`將當前分支強制命名為main並提交
    5. `git remoto add <url>`:跟遠端儲存庫連接
    6. `git push -u origin main`:將本地已提交檔案上傳至遠端

### 1. Git 是什麼

* 用於版本控制的系統

### 2. 如何使用

...

### 3. 常見操作說明

...

