from datetime import datetime
from bs4 import BeautifulSoup


class PttParser:
    @staticmethod
    def parse_post(html, driver):
        soup = BeautifulSoup(html, 'html.parser')
        main_tag = soup.find("div", id="main-content")

        # 作者
        author = main_tag.select(".article-metaline .article-meta-value")[0].text
        print(author)
        # 標題
        title = main_tag.select(".article-metaline .article-meta-value")[1].text
        print(title)

        # 時間
        created_at = main_tag.select(".article-metaline .article-meta-value")[2].text
        # 把字串轉成 datetime 物件
        dt = datetime.strptime(created_at, "%a %b %d %H:%M:%S %Y")
        # 拆成 DATE 和 TIME
        date_str = dt.strftime("%Y-%m-%d")  # MySQL DATE 格式
        time_str = dt.strftime("%H:%M:%S")  # MySQL TIME 格式
        print("created_date=", date_str)
        print("created_time=", time_str)

        # 看板
        board = soup.select_one(".article-metaline-right .article-meta-value").text
        print(board)

        # ip & 地點
        ip_location_tag = ""
        f2_tag = main_tag.select(".f2")
        for tag in f2_tag:
            if "發信站: 批踢踢實業坊(ptt.cc)" in tag.text:
                ip_location_tag = tag.text
        print(ip_location_tag)
        part = ip_location_tag.split("來自:")[-1].strip()
        author_ip, location = part.split(" ", 1)
        location = location.strip("()")
        print(author_ip)
        print(location)

        # url
        url = driver.current_url
        print(url)
        # 內文
        for meta in main_tag.select(".article-metaline"):
            meta.decompose()
        for board_tmp in main_tag.select(".article-metaline-right"):
            board_tmp.decompose()
        for push in main_tag.select(".push"):
            push.decompose()
        for info in main_tag.select(".f2"):
            info.decompose()
        content = main_tag.text
        print(content)

        return {
            "author": author,
            "title": title,
            "created_date": date_str,
            "created_time": time_str,
            "board": board,
            "author_ip": author_ip,
            "location": location,
            "url": url,
            "content": content
        }
