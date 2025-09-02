import os
import pymysql
from datetime import datetime
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 這個 .py 檔所在目錄
dotenv_path = os.path.join(BASE_DIR, "config.env")
load_dotenv(dotenv_path)


class DatabaseHandler:
    def __init__(self, scraper_log):
        self.scraper_log = scraper_log
        self.conn = pymysql.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('PORT')),
            user=os.getenv('USER'),
            password=os.getenv('PASSWORD'),
            database=os.getenv('DATABASE')
        )

    def _log(self, task_name, status, message, level="INFO"):
        log_data = {
            "task_name": task_name,
            "status": status,
            "message": message,
            "level": level,
            "execute_at": datetime.now()
        }
        self.insert_log(log_data)

        # 同步寫進 scraper_log
        getattr(self.scraper_log, level.lower())(message)

    def insert_post(self, post_data: dict):
        try:
            cursor = self.conn.cursor()
            sql = """
                  INSERT INTO posts(board, author, author_ip, title, content, location, url, created_date, created_time,
                                    crawled_at)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                  """
            cursor.execute(sql, (
                post_data["board"],
                post_data["author"],
                post_data["author_ip"],
                post_data["title"],
                post_data["content"],
                post_data["location"],
                post_data["url"],
                post_data["created_date"],
                post_data["created_time"],
                post_data["crawled_at"]
            ))
            self.conn.commit()
            self._log("insert_post", "success", "插入posts成功")
        except Exception as e:
            self._log("insert_post", "failed", f"插入posts失敗:{e}", "ERROR")
            self.conn.rollback()

    def insert_comment(self, comment_data: list):
        try:
            cursor = self.conn.cursor()
            sql = """
                  insert into comments(content, author, author_ip, created_date, created_time, is_push, is_boo, url)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                  """
            for comment in comment_data:
                cursor.execute(sql,
                               (comment["content"], comment["author"], comment["author_ip"], comment["created_date"],
                                comment["created_time"], comment["is_push"], comment["is_boo"], comment["url"]))
                self.conn.commit()
            self._log("insert_comment", "success", "插入comments成功")
        except Exception as e:
            self._log("insert_comment", "failed", f"插入comments失敗:{e}", "ERROR")
            self.conn.rollback()

    def insert_log(self, log_data: dict):
        try:
            cursor = self.conn.cursor()
            sql = """
                  insert into logs(task_name, status, message, level, execute_at)
                  VALUES (%s, %s, %s, %s, %s) \
                  """
            cursor.execute(sql,
                           (log_data["task_name"], log_data["status"], log_data["message"], log_data["level"],
                            log_data["execute_at"]))
            self.conn.commit()
        except Exception as e:
            self.scraper_log.info(f"插入log失敗:{e}")
