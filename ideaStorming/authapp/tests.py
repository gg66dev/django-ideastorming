from unittest import skip
from django_webtest import WebTest

from django.test import TestCase
from .forms import UserForm
from .models import User

from django.contrib.auth import authenticate

#form of register test
class UserFormTest(TestCase):

    def setUp(self):
        self.user = User(
            first_name = "Juan",
            last_name = "Perez",
            email = "prueba@email.cl",
            company = "myCompany S.A.",
            country = "Chile",
            password = "pbkdf2_sha256$30000$sIJRxPDvtciA$Pqc9rmC+wH8AzXUpw8Zvx0LECqrmIf7CLASzw9s0jwE=", #abcd
       )


    def test_init(self):
        UserForm(self.user)

    
    def test_valid_data(self):
        form = UserForm({
            'first_name': 'Pedro',
            'last_name': 'Pereira' ,
            'email': 'pereira@email.cl' ,
            'company': 'other company SA',
            'country': 'Chile',
            'password': 'abcd',
            'confirm_password': 'abcd'
        })
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.first_name, "Pedro")
        self.assertEqual(user.last_name, "Pereira")
        self.assertEqual(user.email, "pereira@email.cl")
        self.assertEqual(user.company, "other company SA")
        self.assertEqual(user.country, "Chile")
        self.assertNotEqual(user.password, "abcd") # password is now encrypted
        self.assertTrue(len(user.password) > 20) # ~ length of encrypt password
        self.assertEqual(user.username, "pereira@email.cl")
    
    def test_blank_data(self):
        form = UserForm({})
        self.assertFalse(form.is_valid())
        check_list = sorted(list(form.errors.items()))
        self.assertEqual(check_list,[
            ('company',  ['This field is required.']),
            ('confirm_password', ['This field is required.']),
            ('country',  ['This field is required.']),
            ('email',  ['This field is required.']),
            ('first_name',  ['This field is required.']),
            ('last_name',  ['This field is required.']),
            ('password', ['This field is required.'])
        ])
        

# register view test
class UserViewTest(WebTest):
    def test_view_page(self):
        page = self.app.get("/register/")
        self.assertEqual(len(page.forms),1)
    
    @skip('no requeried submit form for the validation')
    def test_form_error(self):
        page = self.app.get("/register/")
        page = page.form.submit()
        self.assertContains(page,"This field is required.")

    def test_form_success(self):
        page = self.app.get("/register/")
        page.form['company'] = "other company SA"
        page.form['confirm_password'] = "abcdef"
        page.form['country'] = "Chile"
        page.form['email'] = "pereira2@email.cl"
        page.form['first_name'] = "Pedro"
        page.form['last_name'] = "Pereira"
        page.form['password'] = "abcdef"
        page = page.form.submit()
        self.assertRedirects(page,"/register/")
        user = User.objects.get(username='pereira2@email.cl')
        self.assertNotEqual(user,None);
        self.assertEqual(user.username,'pereira2@email.cl')
        self.assertNotEqual(user.password,'abcdef') # password is now encrypted
        self.assertTrue(len(user.password) > 20) # ~ length of encrypt password
   
    def test_passwords_dont_match(self):
        page = self.app.get("/register/")
        page.form['company'] = "other company SA"
        page.form['confirm_password'] = "abcd"
        page.form['country'] = "Chile"
        page.form['email'] = "pereira@email.cl"
        page.form['first_name'] = "Pedro"
        page.form['last_name'] = "Pereira"
        page.form['password'] = "1234"
        page = page.form.submit()
        self.assertContains(page,"Passwords dont match.")
    


#login - logout test
class LogInLogOutTest(WebTest):
    fixtures = ['users']

    def test_view_page(self):
        page = self.app.get("/")
        self.assertEqual(len(page.forms),1)
    
    def test_login_success(self):
        page = self.app.get("/")
        page.form['email'] = "prueba@email.cl"
        page.form['password'] = "abcd"
        page = page.form.submit()
        #redirecct to page with user info
        self.assertContains(page,"Hello, Juan Perez.")

    @skip('no requeried submit form for the validation')
    def test_login_blank_data(self):
        page = self.app.get("/")
        page.form['email'] = ""
        page.form['password'] = ""
        page = page.form.submit()
        #redirect to page with error message
        self.assertContains(page,"This field is required.")
    
    @skip('error message is display in alert')
    def test_login_wrong_username(self):
        page = self.app.get("/")
        page.form['email'] = "prueba666@email.cl"
        page.form['password'] = "1234"
        page = page.form.submit()
        #redirect to page with error message
        self.assertContains(page,"You entered an incorrect username or password")

    @skip('error message is display in alert')
    def test_login_wrong_password(self):
        page = self.app.get("/")
        page.form['email'] = "prueba@email.cl"
        page.form['password'] = "12345678"
        page = page.form.submit()
        #redirect to page with error message
        self.assertContains(page,"You entered an incorrect username or password")

    def test_logout_success(self):
        self.test_login_success()
        page = self.app.get("/logout/")
        self.assertEqual(len(page.forms),1)