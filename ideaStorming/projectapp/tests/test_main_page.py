from .test_common import BaseProjectWebTest


class MainPageTest(BaseProjectWebTest):
    fixtures = ['users','project_ranking_column']

    def test_display_most_popular_project(self):
        page = self.app.get("/")
        self.assertContains(page,"project with mark 3.601")
        self.assertContains(page,"project with mark 4.631")
        self.assertContains(page,"project with mark 1.991")
        self.assertContains(page,"project with mark 1.821")
        self.assertContains(page,"project with mark 1.691")
        #next 15 project
    
    def test_display_latest_project(self):
        page = self.app.get("/")
        self.assertContains(page,"2017-03-29")
        self.assertContains(page,"2017-03-28")
        self.assertContains(page,"2017-03-11")
        self.assertContains(page,"2017-03-01")
        self.assertContains(page,"2017-01-28")
        #next 15 project
    