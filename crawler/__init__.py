from abc import ABCMeta, abstractmethod


class AbstractCrawler(metaclass=ABCMeta):
    def __init__(self, connector):
        self.connector = connector

    @abstractmethod
    def crawling(self):
        pass
