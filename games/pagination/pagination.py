from typing import List
from games.domainmodel.model import Game
from math import ceil


class Pagination:
    PAGE_SIZE = 6  # no of games per page

    def __init__(self, games: List[Game]):
        self.__games = games

        self.__current_page = 1  # starts at 1, careful when accessing games
        self.__page_count = ceil(len(self.__games) / self.PAGE_SIZE)

    @property
    def current_page(self) -> int:
        return self.__current_page

    @property
    def page_count(self) -> int:
        return self.__page_count

    # deprecated, use go_to_page() instead
    # def go_to_next_page(self):
    #     if self.__current_page < self.page_count:
    #         self.__current_page += 1

    # def go_to_previous_page(self):
    #     if self.__current_page > 1:
    #         self.__current_page -= 1

    # def go_to_first_page(self):
    #     self.__current_page = 1

    # def go_to_last_page(self):
    #     self.__current_page = self.page_count

    def go_to_page(self, page: int):
        if 1 <= page <= self.page_count:
            self.__current_page = page

    def get_page_content(self) -> List[Game]:
        # first item is a multiple of PAGE_SIZE, -1 because page starts at 1
        first_item = (self.current_page - 1) * self.PAGE_SIZE

        last_item = first_item + self.PAGE_SIZE
        # last item should not exceed total number of games
        if last_item >= len(self.__games):
            last_item = len(self.__games)

        return self.__games[first_item:last_item]
