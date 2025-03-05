from utils.logger import Logger
from utils.config import Config

from api import Zakupki
import celery


app = celery.Celery("zakupki", broker = Config.BROKER_URI)

class ParseXMLTask(celery.Task):
    def run(self, url: str) -> str | None:
        if Data := Zakupki.GetPublishDTInEIS(url):
            Msg: str = f'"{url}"-"{Data}"'

            Logger.info(Msg)
            return Msg
        
        return None

ParseXMLTask = app.register_task(ParseXMLTask())

class ParsePageTask(celery.Task):
    def run(self, page: int) -> int | None:
        if Tenders := Zakupki.GetTenders(page):
            for i in Tenders:
                ParseXMLTask.apply_async(args = (i, ))

            return len(Tenders)

        return None

ParsePageTask = app.register_task(ParsePageTask())

class ParseTendersTask(celery.Task):
    def run(self, maxPage: int):
        for i in range(1, maxPage + 1):
            ParsePageTask.apply_async(args = (i, ))

ParseTendersTask = app.register_task(ParseTendersTask())
