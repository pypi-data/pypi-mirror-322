# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import biophony

def test_default_params():
    gen = biophony.BioReadGen()
    for read in gen:
        assert isinstance(read, biophony.BioRead)

def test_10_reads():
    gen = biophony.BioReadGen(count = 10, quality = ('a', 'z'), seqlen = 16)
    i = 0
    for read in gen:
        i += 1
        assert isinstance(read, biophony.BioRead)
        assert len(read.seq.seq) == 16
        # pylint: disable=use-a-generator
        assert all([ord(c) >= ord('a') and ord(c) <= ord('z')
                    for c in read.qual])

    assert i == 10
