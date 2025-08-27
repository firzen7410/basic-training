import os
import pymysql


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

    def insert_post(self, post_data: dict):
        try:
            print(post_data)
            cursor = self.conn.cursor()
            sql = """
                  INSERT INTO posts (board, author, author_ip, title, content, location, url, created_date,
                                     created_time)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                post_data["created_time"]
            ))
            self.conn.commit()
            self.scraper_log.info(f"成功插入資料: {post_data['title']}")
        except Exception as e:
            self.scraper_log.error(f"插入資料失敗: {e}")
            self.conn.rollback()
