from .test_common import BaseProjectWebTest


class DetailProjectTest(BaseProjectWebTest):
    fixtures = ['users','projects']

    ##################
    #Comments section and score
    ##################

    def test_display_project_comments(self):
        page = self.app.get("/detail-project/App_that_recommend_Restaurants/") #project owener pedro.
        self.assertContains(page,"Este es el primer comentario")    #user5
        self.assertContains(page,"Este es el segundo comentario")   #user3
        self.assertContains(page,"Este es el tercer comentario")    #user4

    def test_dont_display_new_comment_form_to_unlogged_user(self):
        page = self.app.get("/detail-project/App_that_recommend_Restaurants/")
        self.assertNotContains(page,"id=\"new_comment\"")

    def test_display_new_comment_form_to_logged_user(self):
        self.loginJuan()
        page = self.app.get("/detail-project/App_that_recommend_Restaurants/")
        self.assertContains(page,"id=\"new_comment\"")

    def test_user_add_new_comment(self):
        self.loginJuan()
        page = self.app.get("/detail-project/App_that_recommend_Restaurants/")
        self.assertContains(page,"id=\"new_comment\"")
        form = page.forms['new_comment']
        form['comment'] = "Este es el tercer comentario."
        form['score']  = 5
        page = form.submit()
        self.assertContains(page,"Este es el tercer comentario.")


    #pedro add comment to own project.
    def test_user_cant_add_comment_own_project(self):
        #dont display new comment form
        self.loginPedro()
        page = self.app.get("/detail-project/App_that_recommend_Restaurants/")
        self.assertNotContains(page,"id=\"new_comment\"")


    #user3 want to add new comment.
    def test_user_cant_add_second_comment(self):
        #dont display new comment form
        self.loginUser3()
        page = self.app.get("/detail-project/App_that_recommend_Restaurants/")
        self.assertNotContains(page,"id=\"new_comment\"")
