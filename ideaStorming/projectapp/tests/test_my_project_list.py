from django.test import TestCase
from django.db.models import Q

from .test_common import BaseProjectWebTest

from authapp.models import User
from projectapp.models import Project, Tag


class MyProjectListTest(BaseProjectWebTest):
    fixtures = ['users', 'projects']
   
    #todo
    def test_view_my_projects_empty(self):
        pass

    """
    * todo: assert ranking of projects
    """
    def test_view_my_projects_page_juan(self):
        #juan login to the page
        self.loginJuan()
        #juan go to 'my projects'
        page = self.app.get("/my-projects/")
        #Juan see the two projects that he had. (todo: count number of project)
        self.assertContains(page,"Virtual cat shop")
        self.assertContains(page,"2017-01-10")
        self.assertContains(page,"Modern suitcase")
        self.assertContains(page,"2017-01-13")
        self.assertNotContains(page,"App that recommend Restaurants")
        self.assertNotContains(page,"2017-01-28")
        #juan logout.
        self.logout();
    
    
    def test_view_my_projects_page_pedro(self):
        #pedro login to de page.
        self.loginPedro()
        #go to 'my-projects'.
        page = self.app.get("/my-projects/")
        #see just one project that he have.  (todo: count number of project)
        self.assertNotContains(page,"Virtual cat shop")
        self.assertNotContains(page,"2017-01-10")
        self.assertNotContains(page,"Modern suitcase")
        self.assertNotContains(page,"2017-01-13")
        self.assertContains(page,"App that recommend Restaurants")
        self.assertContains(page,"2017-01-28")
        #pedro logout.
        self.logout();
        