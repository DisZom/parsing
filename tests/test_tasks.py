import pytest
from app.tasks import ParseXMLTask, ParsePageTask, app


@pytest.fixture(autouse = True)
def setup_celery():
    app.conf.update(task_always_eager = True)


def test_parsexml():
    URL: str = "https://zakupki.gov.ru/epz/order/notice/printForm/viewXml.html?regNumber=0338100004625000003"
    Result: str = '"https://zakupki.gov.ru/epz/order/notice/printForm/viewXml.html?regNumber=0338100004625000003"-"2025-03-03T20:39:00.581+12:00"'
    
    assert ParseXMLTask.apply_async((URL, )).get() == Result

def test_parsepage():
    PAGE: int = 1
    assert ParsePageTask.apply_async((PAGE, )).get() == 10
