from django.test import TestCase
from django_webtest import WebTest
from django.db.models import Q

from authapp.models import User
from .models import Project, Tag


class BaseProjectWebTest(WebTest):

    def loginJuan(self):
        page = self.app.get("/")
        page.form['email'] = "prueba@email.cl"
        page.form['password'] = "abcd"
        page = page.form.submit()
       
    def loginPedro(self):
        page = self.app.get("/")
        page.form['email'] = "pepereria@email.cl"
        page.form['password'] = "perez"
        page = page.form.submit()
       
    def logout(self):
       self.app.get("/logout/");     

class CreateNewProjectTest(BaseProjectWebTest):
    fixtures = ['users']

    def test_view_page(self):
        #user login
        self.loginJuan()
        #user go to new project
        page = self.app.get("/new-project/")
        #user find a form
        self.assertEqual(len(page.forms),1)
 

    def test_form_success(self):
        self.loginJuan()
        page = self.app.get("/new-project/")
        page.form['title'] = "virtual cat shop" 
        page.form['summary'] = """A virtual Shop with cat stuff where the customer can
                                    buy things with virtual currency, this currency the customer get, buying things in 
                                    other physic shops."""
        page.form['advantages'] = "The customer buy thing with virtual currency."
        page.form['investment'] = "$501 - $800 USD"
        page.form['tags'] = "cat,shop,virtual currency"
        page = page.form.submit()
        #get user
        user = User.objects.get(username='prueba@email.cl')
        #get project of the user with the title of the new project
        project = Project.objects.get(
            Q(user=user),
            Q(title='virtual cat shop')
            )
        #check project exist
        self.assertNotEqual(project,None);
        #check summary match
        self.assertEqual(project.summary,"""A virtual Shop with cat stuff where the customer can
                                    buy things with virtual currency, this currency the customer get, buying things in 
                                    other physic shops.""");
        #check advantages match
        self.assertEqual(project.advantages,"The customer buy thing with virtual currency.")
        #check investment match
        self.assertEqual(project.investment,"$501 - $800 USD")
        #check create date same update date
        self.assertEqual(project.date_creation,project.date_last_modification)
        #find tags of project
        test_tags = ['cat','shop','virtual currency']
        project_tags = project.tags.all().order_by('tag')
        self.assertNotEqual(project,project_tags)
        #check tags match
        save_tags = []
        for tag in project_tags:
            save_tags.append(tag.tag)
        self.assertEqual(save_tags, test_tags)    

    """
    * check project with already exist name
    * ...
    """

class CreateListProjectTest(BaseProjectWebTest):
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
        








