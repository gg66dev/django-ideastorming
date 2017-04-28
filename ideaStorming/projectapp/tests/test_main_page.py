from django.test import TestCase

from .test_common import BaseProjectWebTest
from projectapp.views import get_latest_project_list, get_ranked_project_list

class ViewFunctionTest(TestCase):
    fixtures = ['users','project_ranking_column']

    def test_get_most_popular_project(self):
        projects = get_ranked_project_list()
        self.assertEqual(len(projects),20)
    
    def test_get_ranked_project_list(self):
        projects = get_ranked_project_list()
        self.assertEqual(len(projects),20)
    

class MainPageTest(BaseProjectWebTest):
    fixtures = ['users','project_ranking_column']
   
   
    def test_display_most_popular_project(self):
        page = self.app.get("/")
        self.assertContains(page,"project with mark 3601")
        self.assertContains(page,"project with mark 4631")
        self.assertContains(page,"project with mark 1991")
        self.assertContains(page,"project with mark 1821")
        self.assertContains(page,"project with mark 1691")
        #next 15 project
    
    def test_display_latest_project(self):
        page = self.app.get("/")
        self.assertContains(page,"2017-03-29")
        self.assertContains(page,"2017-03-28")
        self.assertContains(page,"2017-03-11")
        self.assertContains(page,"2017-03-01")
        self.assertContains(page,"2017-01-28")
        #next 15 project
    