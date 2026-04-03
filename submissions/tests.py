from django.test import TestCase
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
