from externals.fake import Fake
import abc
import mock


class External_copy_to__mixin(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def external(self):
        '''
        I should return a context manager, whose value is the temporary external
        I will clean up the temporary external when leaving the context it is used in.
        '''
        pass

    def test_to_fake(self):
        mem = Fake()
        with self.external() as external:
            content = external.content
            external.copy_to(mem)

        self.assertEqual(content, mem.content)


    def test_from_fake(self):
        mem = Fake()
        mem.content = 'small something'

        with self.external() as external:
            mem.copy_to(external)

            self.assertEqual('small something', external.content)


class External_copy_to__multiread_mixin(External_copy_to__mixin):

    def test_incomplete_reads_are_concatenated(self):
        mem = Fake()
        with self.external() as external:
            def create_fragmenting_reader():
                class Reader(object):
                    def __init__(self, fragments):
                        self._read_count = 0
                        self._fragments = fragments
                    def read(self, *args, **kwargs):
                        if self._read_count >= len(self._fragments):
                            raise EOFError
                        value = self._fragments[self._read_count]
                        self._read_count += 1
                        return value
                    def __enter__(self, *args, **kwargs):
                        return self
                    def __exit__(self, *args, **kwargs):
                        pass
                return Reader(['a', 'b', 'c'])

            with mock.patch.object(external, 'readable_stream', create_fragmenting_reader):
                external.copy_to(mem)

        self.assertEqual('abc', mem.content)
