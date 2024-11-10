import unittest

# import all test modules
from .test_local_viewer import TestLocalViewer
from .test_cli import TestCLI

# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromTestCase(TestLocalViewer))
suite.addTests(loader.loadTestsFromTestCase(TestCLI))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)