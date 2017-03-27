from django_webtest import WebTest

class BaseProjectWebTest(WebTest):

    def loginJuan(self):
        page = self.app.get("/")
        page.forms['login_form']['email'] = "prueba@email.cl"
        page.forms['login_form']['password'] = "abcd"
        page = page.forms['login_form'].submit()
       
    def loginPedro(self):
        page = self.app.get("/")
        page.forms['login_form']['email'] = "pepereria@email.cl"
        page.forms['login_form']['password'] = "perez"
        page = page.forms['login_form'].submit()
       
    def logout(self):
       self.app.get("/logout/");     


