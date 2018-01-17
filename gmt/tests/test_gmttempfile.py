"""
Tests for GMTTempFile class
"""
import os

from ..utils import GMTTempFile


def test_gmttempfile():
    "Check that file is really created and deleted."
    with GMTTempFile() as tmpfile:
        assert os.path.exists(tmpfile.name)
    # File should be deleted when leaving the with block
    assert not os.path.exists(tmpfile.name)


def test_gmttempfile_unique():
    "Check that generating multiple files creates unique names"
    with GMTTempFile() as tmp1:
        with GMTTempFile() as tmp2:
            with GMTTempFile() as tmp3:
                assert tmp1.name != tmp2.name != tmp3.name


def test_gmttempfile_prefix_suffix():
    "Make sure the prefix and suffix of temporary files are user specifiable"
    with GMTTempFile() as tmpfile:
        assert os.path.basename(tmpfile.name).startswith('gmt-python-')
        assert os.path.basename(tmpfile.name).endswith('.txt')
    with GMTTempFile(prefix="user-prefix-") as tmpfile:
        assert os.path.basename(tmpfile.name).startswith('user-prefix-')
        assert os.path.basename(tmpfile.name).endswith('.txt')
    with GMTTempFile(suffix='.log') as tmpfile:
        assert os.path.basename(tmpfile.name).startswith('gmt-python-')
        assert os.path.basename(tmpfile.name).endswith('.log')
    with GMTTempFile(prefix="user-prefix-", suffix=".log") as tmpfile:
        assert os.path.basename(tmpfile.name).startswith('user-prefix-')
        assert os.path.basename(tmpfile.name).endswith('.log')


def test_gmttempfile_read():
    "Make sure GMTTempFile.read() works"
    with GMTTempFile() as tmpfile:
        with open(tmpfile.name, "w") as ftmp:
            ftmp.write('in.dat: N = 2\t<1/3>\t<2/4>\n')
        assert tmpfile.read() == 'in.dat: N = 2 <1/3> <2/4>\n'
        assert tmpfile.read(keep_tabs=True) == 'in.dat: N = 2\t<1/3>\t<2/4>\n'
