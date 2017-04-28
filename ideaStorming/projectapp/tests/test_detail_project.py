from .test_common import BaseProjectWebTest
from projectapp.models import Comment
from projectapp.forms import NewCommentForm
from authapp.models import User

from django.test import TestCase
from unittest import skip

class DetailProjectTest(BaseProjectWebTest):
    fixtures = ['users','projects']

    ##################
    #Comments section and score
    ##################
    @skip("Don't want to test")
    def test_display_project_comments(self):
        page = self.app.get("/detail-project/App_that_recommend_Restaurants/2/pepereria/") #project owener pedro.
        self.assertContains(page,"Este es el primer comentario")    #user5
        self.assertContains(page,"Este es el segundo comentario")   #user3
        self.assertContains(page,"Este es el tercer comentario")    #user4

    def test_dont_display_new_comment_form_to_unlogged_user(self):
        page = self.app.get("/detail-project/App_that_recommend_Restaurants/2/pepereria/")
        self.assertNotContains(page,"id=\"new_comment\"")

    def test_display_new_comment_form_to_logged_user(self):
        self.loginJuan()
        page = self.app.get("/detail-project/App_that_recommend_Restaurants/2/pepereria/")
        self.assertContains(page,"id=\"new_comment\"")

    def test_user_add_new_comment(self):
        self.loginJuan()
        page = self.app.get("/detail-project/App_that_recommend_Restaurants/2/pepereria/")
        self.assertContains(page,"id=\"new_comment\"")
        form = page.forms['new_comment']
        form['comment'] = "Este es el tercer comentario."
        form['score']  = 5
        page = form.submit()
        self.assertEqual(page.status_int,302) 
        #comment is now in database
        comment = Comment.objects.get(user__username="prueba@email.cl")
        self.assertEqual(comment.comment,"Este es el tercer comentario.")
        self.assertEqual(comment.score,5)
        #comment is displayed in comment list
        page = self.app.get("/detail-project/App_that_recommend_Restaurants/2/pepereria/")
        self.assertContains(page,"Este es el tercer comentario.")

    #pedro add comment to own project.
    def test_user_cant_add_comment_own_project(self):
        #dont display new comment form
        self.loginPedro()
        page = self.app.get("/detail-project/App_that_recommend_Restaurants/2/pepereria/")
        self.assertNotContains(page,"id=\"new_comment\"")

    #user3 (already have one comment in project) want to add new comment.
    def test_user_cant_add_second_comment(self):
        #dont display new comment form
        self.loginUser3()
        page = self.app.get("/detail-project/App_that_recommend_Restaurants/2/pepereria/")
        self.assertNotContains(page,"id=\"new_comment\"")

    def test_user_add_empty_comment(self):
        pass


class AddCommentFormTest(TestCase):
    fixtures = ['users','projects']

    def test_valid_data_form_new_comment(self):
        user = User.objects.get(pk=1)
        form  = NewCommentForm(user,{
            'comment':'Este es un commentario',
            'score': 5,
            'project_title':'App that recommend Restaurants'
            })
        self.assertTrue(form.is_valid)
        comment = form.save()
        self.assertEqual(comment.comment,"Este es un commentario")
        self.assertEqual(comment.score,5)

    def test_invalid_data_project_title_dont_exist(self):
        pass
       
    def test_invalid_data_user_is_none(self):
        pass 
