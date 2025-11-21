import unittest
import sys
import os

# Add BackEnd to path
sys.path.append(os.path.join(os.getcwd(), 'BackEnd'))

from parser.python_parser import parse_python_code
from parser.c_cpp_parser import parse_c_cpp_code
from parser.java_parser import parse_java_code
from parser.html_parser import parse_html_code

class TestParsers(unittest.TestCase):
    def test_python_parser(self):
        code = "def foo():\n    print('hello')"
        result = parse_python_code(code)
        self.assertIn('nodes', result)
        self.assertIn('edges', result)
        self.assertTrue(len(result['nodes']) > 0)

    def test_c_parser(self):
        code = """
        void main() {
            if(1) {
            }
        }
        """
        result = parse_c_cpp_code(code)
        print(f"C Parser Result: {result}")
        self.assertIn('nodes', result)
        self.assertIn('edges', result)
        self.assertTrue(len(result['nodes']) > 0)

    def test_java_parser(self):
        code = """
        public void main(String[] args) {
            if(true) {
            }
        }
        """
        result = parse_java_code(code)
        print(f"Java Parser Result: {result}")
        self.assertIn('nodes', result)
        self.assertIn('edges', result)
        self.assertTrue(len(result['nodes']) > 0)

    def test_html_parser(self):
        code = "<div><p>Hello</p></div>"
        result = parse_html_code(code)
        self.assertIn('nodes', result)
        self.assertIn('edges', result)
        self.assertTrue(len(result['nodes']) > 0)

if __name__ == '__main__':
    unittest.main()
