# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import biophony

def test_empty():
    read = biophony.BioRead(seq = biophony.BioSeq(biophony.ElemSeq("")),
                            qual = (' ', ' '))
    assert read.seq.seqid == ""
    assert read.seq.desc == ""
    assert read.seq.seq == ""
    assert read.qual == (' ', ' ')

def test_with_seq():
    s = "ACTG"
    read = biophony.BioRead(seq = biophony.BioSeq(biophony.ElemSeq(s)),
                            qual = ('a', 'z'))
    assert read.seq.seqid == ""
    assert read.seq.desc == ""
    assert read.seq.seq == s
    assert read.qual == ('a', 'z')
