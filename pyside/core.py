class Pagination:
    def __init__(self, page=1, page_size=20):
        self.page = page
        self.page_size = page_size
        self.total = 0

    @property
    def total_pages(self):
        if self.page_size == 0:
            return 1
        return (self.total + self.page_size - 1) // self.page_size
