from abc import abstractmethod
from typing import Literal

import requests

from DFS_Wrapper.CustomExceptions import RateLimit, InvalidDFSBook

class DFS:
    DFS_BOOKS = {
        'underdog': 'https://api.underdogfantasy.com/beta/v5/over_under_lines',
        'prizepick': 'https://partner-api.prizepicks.com/projections'
    }
    def __init__(self):
        self.api_data = None

    def _get_api_data(self, dfs_book: Literal['underdog', 'prizepick']):
        if dfs_book.lower() not in ['underdog', 'prizepick']:
            raise InvalidDFSBook()

        api_data = requests.get(self.DFS_BOOKS[dfs_book.lower()])

        if api_data.status_code == 200:
            return api_data.json()
        elif api_data.status_code == 429:
            raise RateLimit()
        else:
            raise Exception(f"API Call Failed - Status Code: {api_data.status_code}")

    @abstractmethod
    def _get_leagues_(self):
        pass

    @abstractmethod
    def get_leagues(self):
        pass

    @abstractmethod
    def get_data(self, organized_data:bool=True):
        pass

    @abstractmethod
    def _organize_data(self, dfs_data):
        pass