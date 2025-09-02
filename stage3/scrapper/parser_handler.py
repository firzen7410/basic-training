from datetime import datetime
from bs4 import BeautifulSoup
from stage3.scrapper.database_handler import DatabaseHandler


class PttParser:
    def __init__(self, driver, scraper_log):
        self.driver = driver
        self.scraper_log = scraper_log
        db_handler = DatabaseHandler(self.scraper_log)
        self.db_handler = db_handler

    def _log(self, task_name, status, message, level="INFO"):
        log_data = {
            "task_name": task_name,
            "status": status,
            "message": message,
            "level": level,
            "execute_at": datetime.now()
        }
        self.db_handler.insert_log(log_data)

        # 同步寫進 scraper_log
        getattr(self.scraper_log, level.lower())(message)

    def _parse_mate_info(self, main_tag, post_data):
        # 解析文章的meta信息（作者、標題、時間、看板）
        metainfo = main_tag.select(".article-metaline .article-meta-value")

        if not metainfo:
            self._log("解析metadata欄位", "failed", "找不到文章meta信息，可能是投票文或其他特殊格式", "WARNING")
            return None
        try:
            # 作者
            if len(metainfo) > 0:
                post_data["author"] = metainfo[0].text
                self._log("解析作者欄位", "success", f"{post_data['author']}", "DEBUG")

            # 標題
            if len(metainfo) > 1:
                post_data["title"] = metainfo[1].text
                self._log("解析標題欄位", "success", f"{post_data['title']}", "DEBUG")

            # 時間
            if len(metainfo) > 2:
                created_at = main_tag.select(".article-metaline .article-meta-value")[2].text

                # 把字串轉成 datetime 物件
                dt = datetime.strptime(created_at, "%a %b %d %H:%M:%S %Y")
                # 拆成 DATE 和 TIME
                post_data["created_date"] = dt.strftime("%Y-%m-%d")  # MySQL DATE 格式
                post_data["created_time"] = dt.strftime("%H:%M:%S")  # MySQL TIME 格式
                self._log("解析發文日期欄位", "success", f"{post_data['created_date']}", "DEBUG")
                self._log("解析發文時間欄位", "success", f"{post_data['created_time']}", "DEBUG")

            # 看板
            board_tag = main_tag.select_one(".article-metaline-right .article-meta-value")
            if board_tag:
                post_data["board"] = board_tag.text
                self.scraper_log.info(f"看板: {post_data['board']}")
            self._log("解析看板欄位", "success", f"{post_data['board']}", "DEBUG")


        except Exception as e:
            # 可能出現沒有metadata的文章
            self._log("解析metadata", "failed", f"{e}", "WARNING")

    def _parse_ip_location(self, main_tag, post_data):
        # 要嘛沒有f2，要嘛就是出現下面兩種格式
        f2_tag = main_tag.select(".f2")
        if not f2_tag:
            self._log("解析f2欄位", "failed", "沒有f2欄位", "WARNING")
            return None
        try:
            for tag in f2_tag:
                text = tag.text.strip()
                if "發信站" in text:
                    # 格式: ※ 發信站: 批踢踢實業坊(ptt.cc), 來自: IP (地點)
                    ip_location_tag = text
                    part = ip_location_tag.split("來自:")[-1].strip()
                    post_data["author_ip"], post_data["location"] = part.split(" ", 1)
                    post_data["location"] = post_data["location"].strip("()")
                    self._log("解析ip欄位(發信站版本)", "success", f"{post_data['author_ip']}", "DEBUG")
                    self._log("解析地點欄位(發信站版本)", "success", f"{post_data['location']}", "DEBUG")

                elif text.startswith("※ 編輯:"):
                    # 格式: ※ 編輯: 使用者 (IP 地點), 日期 時間
                    # 先抓括號內的內容
                    if "(" in text and ")" in text:
                        inner = text.split("(")[1].split(")")[0]  # 59.124.228.9 臺灣
                        parts = inner.split(" ", 1)
                        post_data["author_ip"] = parts[0]
                        post_data["location"] = parts[1] if len(parts) > 1 else None
                        self._log("解析ip欄位(編輯版本)", "success", f"{post_data['author_ip']}", "DEBUG")
                        self._log("解析地點欄位(編輯版本)", "success", f"{post_data['location']}", "DEBUG")

        except Exception as e:
            self._log("解析f2欄位", "failed", f"{e}", "ERROR")

    def _parse_content(self, main_tag, post_data):
        for meta in main_tag.select(".article-metaline"):
            meta.decompose()
        for board_tmp in main_tag.select(".article-metaline-right"):
            board_tmp.decompose()
        for push in main_tag.select(".push"):
            push.decompose()
        for info in main_tag.select(".f2"):
            info.decompose()
        post_data["content"] = main_tag.text
        self._log("解析內文", "success", f"{post_data['content']}", "DEBUG")

    def parse_post(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        # 先準備預設值，以應對頁面缺漏
        post_data = {
            "author": None,
            "title": None,
            "created_date": None,
            "created_time": None,
            "board": None,
            "author_ip": None,
            "location": None,
            "url": self.driver.current_url,
            "content": None,
            "crawled_at": None
        }

        # 一篇文一定有main-content
        main_tag = soup.find("div", id="main-content")

        # 抓出metaData:發文日期、時間、作者帳號、看板，並更新到post_data
        self._parse_mate_info(main_tag, post_data)

        # 抓出發文者ip與地點
        self._parse_ip_location(main_tag, post_data)

        # 抓出內文
        self._parse_content(main_tag, post_data)
        self.scraper_log.info("文章解析完成")

        # 取得現在時間
        now = datetime.now()

        # 轉成 MySQL datetime 格式字串
        crawled_at = now.strftime("%Y-%m-%d %H:%M:%S")
        post_data["crawled_at"] = crawled_at

        return post_data

    def _parse_comment_datetime(self, comment_tag, comment_data, year):
        ip_datetime_tag = comment_tag.find("span", class_="push-ipdatetime")
        if not ip_datetime_tag:
            self._log("解析留言的IP、時間資訊", "failed", "該留言沒有時間、IP資訊")
            return None

        ip_datetime_text = ip_datetime_tag.get_text(strip=True)

        try:
            parts = ip_datetime_text.split()

            if len(parts) >= 3:
                # 完整格式：IP 日期 時間
                ip, date_part, time_part = parts[0], parts[1], parts[2]
                comment_data["author_ip"] = ip
                self._log("判斷留言的IP、日期、時間資訊", "success", f"三個都有")
            elif len(parts) == 2:
                # 沒有IP：日期 時間
                date_part, time_part = parts[0], parts[1]
                self._log("判斷留言的IP、日期、時間資訊", "success", "只有日期、時間")
            else:
                self._log("判斷留言的IP、日期、時間資訊", "failed", f"該欄位異常:{ip_datetime_text}", "DEBUG")
                return None

            # 解析日期時間
            try:
                date_obj = datetime.strptime(f"{year}/{date_part} {time_part}", "%Y/%m/%d %H:%M")
                comment_data["created_date"] = date_obj.strftime("%Y-%m-%d")
                comment_data["created_time"] = date_obj.strftime("%H:%M:%S")
                self._log("留言時間格式轉換", "success",
                          f"日期:{comment_data['created_date']},時間{comment_data['created_time']}", "DEBUG")
            except ValueError as e:
                self._log("留言時間格式轉換", "failed", f"可能是該位置並非時間，error:{e}", "ERROR")
        except Exception as e:
            self._log("解析留言的IP、時間資訊", "failed", f"發生錯誤；{e}", "ERROR")

    def extract_year(self, main_tag):
        try:
            created_at = main_tag.select(".article-metaline .article-meta-value")[2].text
            year = created_at.split()[-1]
            self._log("年份提取", "success", f"{year}", "DEBUG")
            return year
        except Exception as e:
            self._log("年份提取", "failed", f"{e}", "ERROR")

            # 預設為當前年份
            return str(datetime.now().year)

    def _parse_single_comment(self, comment_tag, year, url):
        # 解析單則留言
        comment_data = {
            "content": None,
            "author": None,
            "author_ip": None,
            "created_date": None,
            "created_time": None,
            "is_push": 0,
            "is_boo": 0,
            "url": url
        }
        # 推噓箭頭
        push_tag_span = comment_tag.select_one("span.push-tag")
        push_tag = push_tag_span.text.strip()

        if push_tag == '推':
            comment_data["is_push"], comment_data["is_boo"] = 1, 0
        elif push_tag == '噓':
            comment_data["is_push"], comment_data["is_boo"] = 0, 1
        elif push_tag == '→':
            comment_data["is_push"], comment_data["is_boo"] = 0, 0

        self._log("解析留言推噓", "success", f"{comment_data['is_push']}，{comment_data['is_boo']}", "DEBUG")

        # 作者
        author_tag = comment_tag.find("span", class_="f3 hl push-userid")
        comment_data["author"] = author_tag.text
        self._log("解析作者欄位", "success", f"{comment_data['author']}", "DEBUG")

        # 留言內文
        content_tag = comment_tag.find("span", class_="f3 push-content")
        if content_tag:
            content = content_tag.get_text().lstrip(':').strip()
            comment_data["content"] = content
        self._log("解析留言內文欄位", "success", f"{comment_data['content']}", "DEBUG")

        # IP、日期、時間
        self._parse_comment_datetime(comment_tag, comment_data, year)

        return comment_data

    def parse_comment(self, html):
        self.scraper_log.info("開始解析ptt留言")
        try:
            soup = BeautifulSoup(html, 'html.parser')
            main_tag = soup.find("div", id="main-content")
            comment_tags = main_tag.find_all("div", class_="push")

            # 判斷有沒有留言
            if not comment_tags:
                self._log("解析留言", "failed", "此貼文沒有留言")
                return []

            # 找出此貼文年分
            year = self.extract_year(main_tag)

            # 逐則處理，comments放所有留言
            comments = []
            for i, comment_tag in enumerate(comment_tags):
                try:
                    # 每一篇交給_parse_single_comment解析
                    comment_data = self._parse_single_comment(comment_tag, year, self.driver.current_url)
                    if comment_data:
                        comments.append(comment_data)
                except Exception as e:
                    self._log("每一篇交給_parse_single_comment解析", "failed", f"{e}", "ERROR")
                    continue
            return comments

        except Exception as e:
            self._log("留言解析", "failed", f"{e}", "ERROR")
