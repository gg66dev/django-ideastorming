from django_webtest import WebTest

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


