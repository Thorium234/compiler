from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Assignment

User = get_user_model()

class AssignmentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='lecturer', password='pw', is_lecturer=True)
        self.assignment = Assignment.objects.create(
            title="Test Case 1",
            description="Write a program to print Hello",
            expected_output="Hello",
            created_by=self.user
        )

    def test_assignment_string_representation(self):
        self.assertEqual(str(self.assignment), "Test Case 1")

    def test_assignment_creation(self):
        self.assertEqual(self.assignment.title, "Test Case 1")
        self.assertEqual(self.assignment.created_by.username, "lecturer")
