from django.test import TestCase
from django.db.models import Q


class CommentTest(BaseProjectWebTest):
    fixtures = ['users','projects']

    def test_select_comment_form_success(self):
        pass 
