from django.test import TestCase
from django.db.models import Q

from .test_common import BaseProjectWebTest
from authapp.models import User
from projectapp.models import Project, Tag


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