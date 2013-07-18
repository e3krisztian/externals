from externals.fake import Fake
import abc


class External_copy_to__mixin(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def external(self):
        pass

    def test_to_fake(self):
        mem = Fake()
        content = self.external.content
        
        self.external.copy_to(mem)

        self.assertEqual(content, mem.content)

    def test_from_fake(self):
        mem = Fake()
        mem.content = 'small something'

        external = self.external
        mem.copy_to(external)

        self.assertEqual('small something', external.content)


class External_copy_to__multiread_mixin(External_copy_to__mixin):

    def test_incomplete_reads_are_concatenated(self):
        mem = Fake()
        external = self.external

        reads = ['a', 'b', 'c', EOFError]
        with mock.patch.object(external, 'read', side_effect=reads):
            external.copy_to(mem)
            
            self.assertEqual('abc', mem.content)
