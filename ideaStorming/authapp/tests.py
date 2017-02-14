from django_webtest import WebTest

from django.test import TestCase
from .forms import UserForm
from .models import User


class UserFormTest(TestCase):

    def setUp(self):
        self.user = User(
            first_name = "Gustavo",
            last_name = "Pfeifer",
            email = "prueba@email.cl",
            company = "myCompany S.A.",
            country = "Chile",
            password = "1234",
       )

    def test_init(self):
        UserForm(self.user)

    #def test_init_without_entry(self):
    #    with self.assertRaises(KeyError):
    #        UserForm()

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
        self.assertEqual(user.password, "abcd")
    
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
        

class UserViewTest(WebTest):
    def test_view_page(self):
        page = self.app.get("/register/")
        self.assertEqual(len(page.forms),1)

    def test_form_error(self):
        page = self.app.get("/register/")
        page = page.form.submit()
        self.assertContains(page,"This field is required.")

    def test_form_success(self):
        page = self.app.get("/register/")
        page.form['company'] = "other company SA"
        page.form['confirm_password'] = "abcd"
        page.form['country'] = "Chile"
        page.form['email'] = "pereira@email.cl"
        page.form['first_name'] = "Pedro"
        page.form['last_name'] = "Pereira"
        page.form['password'] = "abcd"
        page = page.form.submit()
        self.assertRedirects(page,"/register/")

    #todo: que confirm_password y password no son iguales

    