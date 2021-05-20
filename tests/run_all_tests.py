import unittest

suite = unittest.TestLoader().discover('.', pattern = "test_*.py")
unittest.TextTestRunner(verbosity=2).run(suite)