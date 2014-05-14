import unittest


class Test_imports(unittest.TestCase):

    def test_Memory(self):
        from externals import Memory
        Memory

    def test_File(self):
        from externals import File
        File

    def test_working_directory(self):
        from externals import working_directory
        working_directory

    def test_HierarchicalExternal(self):
        from externals import HierarchicalExternal
        HierarchicalExternal

    def test_NoParentError(self):
        from externals import NoParentError
        NoParentError
