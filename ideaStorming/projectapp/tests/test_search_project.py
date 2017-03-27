from .test_common import BaseProjectWebTest


class SearchProjectTest(BaseProjectWebTest):
    fixtures = ['users','projects']

    def test_search_project(self):
        page = self.app.get("/search/?q=recommend")
        self.assertContains(page,"App that recommend Restaurants")