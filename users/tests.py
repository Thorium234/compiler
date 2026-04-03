from django.test import TestCase
from .models import User

class UserModelTest(TestCase):
    def test_user_roles(self):
        student = User.objects.create_user(username='student', password='pw', is_student=True)
        lecturer = User.objects.create_user(username='lecturer', password='pw', is_lecturer=True)
        
        self.assertTrue(student.is_student)
        self.assertFalse(student.is_lecturer)
        self.assertTrue(lecturer.is_lecturer)
        self.assertFalse(lecturer.is_student)

    def test_assigned_lecturer(self):
        lecturer = User.objects.create_user(username='lecturer', password='pw', is_lecturer=True)
        student = User.objects.create_user(username='student', password='pw', is_student=True, assigned_lecturer=lecturer)
        
        self.assertEqual(student.assigned_lecturer, lecturer)
        self.assertIn(student, lecturer.students.all())
