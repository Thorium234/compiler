from django.test import TestCase
import json
from submissions.services import run_python_code
from submissions.views import flexible_compare

class ExecutionEngineTest(TestCase):
    def test_basic_execution(self):
        result = run_python_code("print('Hello World')")
        self.assertEqual(result['stdout'].strip(), "Hello World")
        self.assertEqual(result['exit_code'], 0)

    def test_input_execution(self):
        result = run_python_code("name = input(); print(f'Hello {name}')", inputs="Campus")
        self.assertEqual(result['stdout'].strip(), "Hello Campus")
        self.assertEqual(result['exit_code'], 0)

    def test_syntax_error(self):
        result = run_python_code("print('Hello")
        self.assertIn("SyntaxError", result['stderr'])
        self.assertNotEqual(result['exit_code'], 0)

    def test_timeout(self):
        code = "import time\ntime.sleep(20)"
        result = run_python_code(code)
        self.assertIn("Time Limit Exceeded", result['stderr'])
        self.assertEqual(result['exit_code'], 124)

    def test_infinite_loop(self):
        code = "while True: pass"
        result = run_python_code(code)
        self.assertIn("Time Limit Exceeded", result['stderr'])
        self.assertEqual(result['exit_code'], 124)

class GradingLogicTest(TestCase):
    def test_flexible_compare_basic(self):
        self.assertTrue(flexible_compare("hello", "hello"))
        self.assertTrue(flexible_compare("hello  ", "hello"))
        self.assertTrue(flexible_compare("hello\n", "hello"))
        self.assertTrue(flexible_compare("hello \n ", "hello"))

    def test_flexible_compare_multiline(self):
        actual = "line1  \nline2\n"
        expected = "line1\nline2"
        self.assertTrue(flexible_compare(actual, expected))

    def test_flexible_compare_mismatch(self):
        self.assertFalse(flexible_compare("hello", "world"))
        self.assertFalse(flexible_compare("line1\nline2", "line1\nline3"))

class GuestAccessTest(TestCase):
    def test_practice_view_guest_access(self):
        # Should be accessible without login
        response = self.client.get('/submissions/practice/')
        self.assertEqual(response.status_code, 200)

    def test_execute_code_guest_access(self):
        # Should be accessible without login (POST)
        response = self.client.post('/submissions/execute/', data=json.dumps({'code': 'print(1)', 'inputs': ''}), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_assignment_editor_guest_access(self):
        # Should NOT be accessible without login
        response = self.client.get('/submissions/editor/1/')
        self.assertEqual(response.status_code, 302) # Redirect to login
