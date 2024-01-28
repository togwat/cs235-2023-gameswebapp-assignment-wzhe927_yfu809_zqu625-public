PAGINATION_MENU_SIZE = 7    # how many pages in the pagination menu


def create_pagination_list(page_num: int, total_pages: int):
    """Returns an array containing the pages for the pagination menu"""
    start_page = page_num - PAGINATION_MENU_SIZE // 2
    end_page = page_num + PAGINATION_MENU_SIZE // 2
    # check for overflow
    if start_page < 1:
        start_page = 1
        end_page = min(PAGINATION_MENU_SIZE, total_pages)
    elif end_page > total_pages:
        end_page = total_pages
        start_page = max(total_pages - PAGINATION_MENU_SIZE + 1, 1)

    return list(range(start_page, end_page + 1))
