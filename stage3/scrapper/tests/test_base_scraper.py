import pytest
from unittest.mock import MagicMock, patch
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from stage3.scrapper.base_scraper import BaseScraper


@pytest.fixture
def mock_driver():
    """建立 Selenium WebDriver 的 mock"""
    return MagicMock()


@pytest.fixture
def mock_log():
    """建立 logging 的 mock"""
    return MagicMock()


@pytest.fixture
def scraper(mock_driver, mock_log):
    # Patch DatabaseHandler，避免真實 DB 呼叫
    with patch("stage3.scrapper.base_scraper.DatabaseHandler") as MockDB:
        return BaseScraper(mock_driver, mock_log)


def test_navigate_success(scraper, mock_driver):
    # self.driver.get(url)不會回傳東西，所以回傳None就是模擬成功navigate
    mock_driver.get.return_value = None
    result = scraper.navigate("http://test.com")
    assert result is True
    # 驗證insert_log有被呼叫
    scraper.db_handler.insert_log.assert_called_once()
    scraper.scraper_log.debug.assert_called_once_with("導航到http://test.com")


def test_navigate_fail(scraper, mock_driver):
    # side_effect表示呼叫到driver.get時丟出Exception("bad url")例外
    mock_driver.get.side_effect = Exception("bad url")
    result = scraper.navigate("http://fail.com")
    assert result is False
    scraper.db_handler.insert_log.assert_called_once()
    scraper.scraper_log.error.assert_called_once()


def test_find_element_success(scraper, mock_driver):
    # 模擬find_element找到的元素
    fake_element = MagicMock()
    mock_driver.find_element.return_value = fake_element
    element = scraper.find_element("id", "ok")
    assert element == fake_element


def test_find_element_fail(scraper, mock_driver):
    # 模擬丟出例外情況
    mock_driver.find_element.side_effect = NoSuchElementException()
    element = scraper.find_element("id", "notfound")
    assert element is None
    scraper.scraper_log.error.assert_called_once()


def test_wait_for_element_success(scraper):
    fake_element = MagicMock()
    # 把WebDriverWait替換成mock，他如果成功會回傳一個web element，這邊用fake_element替代
    with patch("stage3.scrapper.base_scraper.WebDriverWait") as MockWait:
        MockWait.return_value.until.return_value = fake_element
        # 呼叫我們要測的function，但我們已經把webDriverWait mock掉了，所以不會真的等
        element = scraper.wait_for_element("id", "ok", timeout=1)
    assert element == fake_element


def test_wait_for_element_timeout(scraper):
    with patch("stage3.scrapper.base_scraper.WebDriverWait") as MockWait:
        # 跟上面同理，模擬丟出例外情況
        MockWait.return_value.until.side_effect = TimeoutException()
        # 把上一頁的動作mock掉
        scraper.back = MagicMock()
        element = scraper.wait_for_element("id", "timeout", timeout=1)
    # 驗證timeout後回傳為None
    assert element is None
    # 驗證scraper_log.error和上一頁有被呼叫
    scraper.scraper_log.error.assert_called_once()
    scraper.back.assert_called_once()


def test_move_to_element_success(scraper, mock_driver):
    fake_element = MagicMock()
    result = scraper.move_to_element(fake_element)
    assert result is True
    # 驗證driver.execute_script有被呼叫
    mock_driver.execute_script.assert_called_once()


def test_move_to_element_none(scraper):
    # 欲移動到的元素為None
    result = scraper.move_to_element(None)
    assert result is False
    # 驗證warning
    scraper.scraper_log.warning.assert_called_once()


def test_move_to_element_fail(scraper, mock_driver):
    fake_element = MagicMock()
    # 滾動失敗的情況，會回傳false
    mock_driver.execute_script.side_effect = Exception("scroll fail")
    result = scraper.move_to_element(fake_element)
    assert result is False
    scraper.scraper_log.error.assert_called_once()


def test_handle_over18_success(scraper, mock_driver):
    fake_btn = MagicMock()
    mock_driver.find_element.return_value = fake_btn
    result = scraper.handle_over18()
    assert result is True
    fake_btn.click.assert_called_once()
    scraper.scraper_log.info.assert_called_once_with("已點擊成功")


def test_handle_over18_no_popup(scraper, mock_driver):
    mock_driver.find_element.side_effect = NoSuchElementException()
    result = scraper.handle_over18()
    assert result is False  # 沒有 popup 當正常流程


def test_back_success(scraper, mock_driver):
    scraper.back()
    mock_driver.back.assert_called_once()


def test_back_fail(scraper, mock_driver):
    mock_driver.back.side_effect = NoSuchElementException()
    result = scraper.back()
    assert result is False
    scraper.scraper_log.error.assert_called_once()


def test_click_element():
    fake_element = MagicMock()
    assert BaseScraper.click_element(fake_element) is True
    fake_element.click.assert_called_once()


def test_safe_to_text_normal():
    fake_element = MagicMock()
    fake_element.text = " hello "
    assert BaseScraper.safe_to_text(fake_element) == "hello"


def test_safe_to_text_none():
    assert BaseScraper.safe_to_text(None, default="x") == "x"


def test_safe_to_text_with_error():
    bad_element = MagicMock()
    type(bad_element).text = property(lambda self: 1 / 0)  # 故意觸發例外
    assert BaseScraper.safe_to_text(bad_element, default="err") == "err"
