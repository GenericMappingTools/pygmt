"""
Tests for GMTTempFile class
"""
import os

from ..utils import GMTTempFile


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

    # check if the temporary file is really deleted
    assert not os.path.exists(tmpfile.name)
