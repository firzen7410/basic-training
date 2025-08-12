import os

print(os.getenv("KEY"))
print(os.getenv("MODE"))

from dotenv import load_dotenv

load_dotenv()  # 預設會讀取當前資料夾的 .env
api_key = os.getenv("API_KEY")
debug_mode = os.getenv("DEBUG")

print(api_key, debug_mode)
