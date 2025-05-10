import unittest
from _tests_chinese_checkers import _test_player, _test_board, _test_piece, _test_game

def test_combined():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    # Add test cases from individual test modules
    suite.addTest(loader.loadTestsFromModule(_test_player))
    suite.addTest(loader.loadTestsFromModule(_test_board))
    suite.addTest(loader.loadTestsFromModule(_test_piece))
    suite.addTest(loader.loadTestsFromModule(_test_game))

    # Run the combined test suite
    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    if result.wasSuccessful():
        print("All tests passed!")
    else:
        print("Some tests failed!")

if __name__ == "__main__":
    test_combined()