import unittest

from file_browser import can_rename, validate_filename, search_files, exists

validate_filename_table_tests = [
    {"name": "INVALID_1", "input": "", "expected": False},
    {"name": "INVALID_2", "input": "/../..", "expected": False},
    {"name": "INVALID_3", "input": "/../surrounded_by_dots/../path", "expected": False},
    {"name": "INVALID_4", "input": "startswith_dots/../path", "expected": False},
    {"name": "INVALID_5", "input": "filename/is/nested", "expected": False},
    {"name": "INVALID_6", "input": "pathname/", "expected": False},
    {"name": "INVALID_7", "input": "./p\athname", "expected": False},
    
    {"name": "VALID_1", "input": "pathname", "expected": True},
    {"name": "VALID_2", "input": ".pathname", "expected": True},
    {"name": "VALID_5", "input": ".pathname", "expected": True},
]

can_rename_table_tests = [
    {"name": "INVALID_1", "input1": "can_rename/123", "input2": "/cannot/123", "expected": False},
    {"name": "INVALID_2", "input1": "can-you-rename/123/to/this", "input2": "cannot-rename/123/to/this", "expected": False},

    {"name": "VALID_1", "input1": "/can/rename-old-1", "input2": "/can/rename-old-2", "expected": True},
    {"name": "VALID_2", "input1": "can/nested/rename-old-1", "input2": "can/nested/rename-old-2", "expected": True},
]


TEST_BASEPATH = "./test_fixtures/"

# this requires test_fixtures dir to exist with the following structure:
# test_fixtures
# ├── hello.txt
# ├── folder_one
# │   ├── world.txt
search_files_table_tests = [
    {"name": "INVALID", "input": "/finalize", "expected": []},
    {"name": "INVALID_2", "input": "/*finalize..ml;m,", "expected": []},

    # searching for "hello" returns all files containing the word "hello" inside the fixtures dir
    {"name": "find_hello", "input": "hello", "expected": ["hello.txt", "folder_one/also_hello.txt"]},
]



class TestFileBroweser(unittest.TestCase):
    def test_exists(self):
        # uses the same fixture dir as search_files_table_tests
        self.assertTrue(exists(TEST_BASEPATH, "hello.txt"))
        self.assertTrue(exists(TEST_BASEPATH, "folder_one/world.txt"))
        self.assertFalse(exists(TEST_BASEPATH, "folder_one/does_not_exist.txt"))

    def test_validate_path(self):
        for test in validate_filename_table_tests:
            with self.subTest(name=test["name"]):
                self.assertEqual(validate_filename(test["input"]), test["expected"], "EXPECTED: " + str(test["expected"]))

    def test_can_rename(self):
        for test in can_rename_table_tests:
            with self.subTest(name=test["name"]):
                self.assertEqual(can_rename(test["input1"], test["input2"]), test["expected"], "EXPECTED: " + str(test["expected"]))

    def test_search_files(self):
        for test in search_files_table_tests:
            with self.subTest(name=test["name"]):
                res = search_files(TEST_BASEPATH, test["input"])
                self.assertEqual(res, test["expected"], "EXPECTED: " + str(test["expected"]))

if __name__ == '__main__':
    unittest.main()