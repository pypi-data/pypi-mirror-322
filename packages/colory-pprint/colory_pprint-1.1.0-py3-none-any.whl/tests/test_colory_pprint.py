import unittest
from colory_pprint import ColoryPPrint

class TestColoryPPrint(unittest.TestCase):
    def test_basic_logging(self):
        log = ColoryPPrint()
        log({"message": "Hello, World!"})  # Ensure no exceptions are raised

    def test_custom_styles(self):
        log = ColoryPPrint(debug=True)
        log.red.bold({"status": "error", "message": "An error occurred."})

if __name__ == "__main__":
    unittest.main()
