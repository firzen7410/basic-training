import os
from dotenv import load_dotenv

load_dotenv('config.env')

api_key = os.getenv('API_KEY')
debug = os.getenv('DEBUG')

mode = os.getenv("MODE")
key = os.getenv("KEY")

print(api_key, debug)
