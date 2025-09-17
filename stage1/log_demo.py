import logging

# 預設使用root的logger
# 預設只輸出 warning 及比 warning 更嚴重的訊息
# CRITICAL（50）
# ERROR（40）
# WARNING（30）
# INFO（20）
# DEBUG（10）
# NOTSET（0）
# logging有四個核心組件:logger, handler, formatter, level

# 自行建立logger，命名dev
dev_logger = logging.getLogger('dev')
# 設置logger等級
dev_logger.setLevel(logging.DEBUG)

# Handler: 輸出到 console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Header:輸出到檔案
file_handler = logging.FileHandler('log_demo.log')
file_handler.setLevel(logging.DEBUG)

# 設置formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
# 綁定handler
dev_logger.addHandler(file_handler)
dev_logger.addHandler(console_handler)
try:
    a = {[1024]: "jack"}
except Exception as e:
    dev_logger.exception("發生錯誤")
