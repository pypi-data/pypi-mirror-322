import json
import chardet
from typing import Optional
from bs4 import BeautifulSoup

from scan.common import logger
from scan.thread_pool import timeout_pool


class Response:
    def __init__(self):
        self.__req_resp = None
        self.status_code = None
        self.message = ''
        self.ok = False
        self.client = None
        self.request_url = None

    async def aclose(self):
        if self.__req_resp:
            try:
                await self.__req_resp.aclose()
            except:
                pass
        if self.client:
            try:
                await self.client.aclose()
            except:
                pass

    @property
    def response(self):
        return self.__req_resp

    @response.setter
    def response(self, req_resp):
        self.__req_resp = req_resp
        self.status_code = req_resp.status_code

    def json(self):
        try:
            return json.loads(self.__req_resp.content)
        except Exception as e:
            logger.error(f'格式化json异常:{e}, 链接:{self.request_url}')

    def soup(self, features: str = 'lxml', timeout: int = 10) -> Optional[BeautifulSoup]:
        """
        解析HTML内容为BeautifulSoup对象
        Args:
            features: 解析器类型，默认为lxml
            timeout: 解析超时时间（秒）
        Returns:
            BeautifulSoup对象，解析失败时返回None
        """
        def parse_html(content: bytes, parser_features: str) -> Optional[BeautifulSoup]:
            return BeautifulSoup(content, parser_features)

        return timeout_pool.submit_task(
            parse_html,
            self.__req_resp.content,
            features,
            timeout=timeout
        )

    def text(self):
        try:
            return self.__req_resp.content.decode()
        except UnicodeDecodeError:
            try:
                encoding = chardet.detect(self.__req_resp.content).get('encoding')
                return self.__req_resp.content.decode(encoding)
            except Exception as e:
                logger.error(f'格式化text异常:{e}')
        except Exception as e:
            logger.error(f'格式化text异常:{e}, 链接:{self.request_url}')

    def content(self):
        try:
            content = self.__req_resp.content
            return content
        except Exception as e:
            logger.error(f'获取content异常:{e}, 链接:{self.request_url}')
