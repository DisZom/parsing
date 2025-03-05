from utils.web import WebClient

from selectolax.lexbor import LexborHTMLParser as HTMLParser
from selectolax.lexbor import LexborNode

import xmltodict


class ZakupkiAPI:
    def __init__(self):
        self.MainURL: str = "https://zakupki.gov.ru"
        self.TenderSelector: str = '.registry-entry__header  * .registry-entry__header-top__icon > a[target="_blank"]'

    def GetPublishDTInEIS(self, url: str) -> str | None:
        with WebClient() as Session:
            if XMLResponse := Session.Fetch(url):
                XMLDict: dict = xmltodict.parse(XMLResponse.Content)
                return XMLDict[tuple(XMLDict.keys())[0]].get("commonInfo", {}).get("publishDTInEIS")

        return None

    def GetTenders(self, page: int) -> list[str]:
        URL: str = f"{self.MainURL}/epz/order/extendedsearch/results.html?fz44=on&pageNumber={page}"

        with WebClient() as Session:
            if TenderResponse := Session.Fetch(URL):
                TendersNodes: list[LexborNode] = HTMLParser(TenderResponse.Content).css(self.TenderSelector)
                return [ f'{self.MainURL}{i.attributes["href"].replace("view.html", "viewXml.html")}' for i in TendersNodes ]
    
        return None

Zakupki: ZakupkiAPI = ZakupkiAPI()
