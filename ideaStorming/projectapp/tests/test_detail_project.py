from .test_common import BaseProjectWebTest


class DetailProjectTest(BaseProjectWebTest):
    fixtures = ['users','projects']

    ##################
    #Comments section and score
    ##################

    def test_display_project_comments(self):
        pass
        #page = self.app.get("/detail-project/App_that_recommend_Restaurants/")
        #self.assertContains(page,"Este es el primer comentario")
        #self.assertContains(page,"Este es el segundo comentario")
        #self.assertContains(page,"Este es el tercer comentario")

    def test_user_add_comment(self):
        pass

    def test_user_cant_add_comment_own_project(self):
        pass

    def test_user_cant_add_second_comment(self):
        pass