"""
Helper functions for testing.
"""

import importlib
import inspect
import string
from pathlib import Path

from pygmt.exceptions import GMTImageComparisonFailure
from pygmt.io import load_dataarray
from pygmt.src import which


def check_figures_equal(*, extensions=("png",), tol=0.0, result_dir="result_images"):
    """
    Decorator for test cases that generate and compare two figures.

    The decorated function must return two arguments, *fig_ref* and *fig_test*,
    these two figures will then be saved and compared against each other.

    This decorator is practically identical to matplotlib's check_figures_equal
    function, but adapted for PyGMT figures. See also the original code at
    https://matplotlib.org/3.3.1/api/testing_api.html#
    matplotlib.testing.decorators.check_figures_equal

    Parameters
    ----------
    extensions : list
        The extensions to test. Default is ["png"].
    tol : float
        The RMS threshold above which the test is considered failed.
    result_dir : str
        The directory where the figures will be stored.

    Examples
    --------

    >>> import pytest
    >>> import shutil
    >>> from pygmt import Figure
    >>> from pathlib import Path

    >>> @check_figures_equal(result_dir="tmp_result_images")
    ... def test_check_figures_equal():
    ...     fig_ref = Figure()
    ...     fig_ref.basemap(projection="X5c", region=[0, 5, 0, 5], frame=True)
    ...     fig_test = Figure()
    ...     fig_test.basemap(
    ...         projection="X5c", region=[0, 5, 0, 5], frame=["WrStZ", "af"]
    ...     )
    ...     return fig_ref, fig_test
    >>> test_check_figures_equal()
    >>> assert len(list(Path("tmp_result_images").iterdir())) == 0
    >>> shutil.rmtree(path="tmp_result_images")  # cleanup folder if tests pass

    >>> @check_figures_equal(result_dir="tmp_result_images")
    ... def test_check_figures_unequal():
    ...     fig_ref = Figure()
    ...     fig_ref.basemap(projection="X5c", region=[0, 6, 0, 6], frame=True)
    ...     fig_test = Figure()
    ...     fig_test.basemap(projection="X5c", region=[0, 3, 0, 3], frame=True)
    ...     return fig_ref, fig_test
    >>> with pytest.raises(GMTImageComparisonFailure):
    ...     test_check_figures_unequal()
    >>> for suffix in ["", "-expected", "-failed-diff"]:
    ...     assert (
    ...         Path("tmp_result_images") / f"test_check_figures_unequal{suffix}.png"
    ...     ).exists()
    >>> shutil.rmtree(path="tmp_result_images")  # cleanup folder if tests pass
    """
    allowed_chars = set(string.digits + string.ascii_letters + "_-[]()")
    keyword_only = inspect.Parameter.KEYWORD_ONLY

    def decorator(func):
        import pytest
        from matplotlib.testing.compare import compare_images

        Path(result_dir).mkdir(parents=True, exist_ok=True)
        old_sig = inspect.signature(func)

        @pytest.mark.parametrize("ext", extensions)
        def wrapper(*args, ext="png", request=None, **kwargs):
            if "ext" in old_sig.parameters:
                kwargs["ext"] = ext
            if "request" in old_sig.parameters:
                kwargs["request"] = request
            try:
                file_name = "".join(c for c in request.node.name if c in allowed_chars)
            except AttributeError:  # 'NoneType' object has no attribute 'node'
                file_name = func.__name__
            try:
                fig_ref, fig_test = func(*args, **kwargs)
                ref_image_path = Path(result_dir) / f"{file_name}-expected.{ext}"
                test_image_path = Path(result_dir) / f"{file_name}.{ext}"
                fig_ref.savefig(ref_image_path)
                fig_test.savefig(test_image_path)

                # Code below is adapted for PyGMT, and is originally based on
                # matplotlib.testing.decorators._raise_on_image_difference
                err = compare_images(
                    expected=ref_image_path,
                    actual=test_image_path,
                    tol=tol,
                    in_decorator=True,
                )
                if err is None:  # Images are the same
                    ref_image_path.unlink()
                    test_image_path.unlink()
                else:  # Images are not the same
                    for key in ["actual", "expected", "diff"]:
                        err[key] = Path(err[key]).relative_to(".")
                    raise GMTImageComparisonFailure(
                        f"images not close (RMS {err['rms']:.3f}):\n"
                        f"\t{err['actual']}\n"
                        f"\t{err['expected']}"
                    )
            finally:
                del fig_ref
                del fig_test

        parameters = [
            param
            for param in old_sig.parameters.values()
            if param.name not in {"fig_test", "fig_ref"}
        ]
        if "ext" not in old_sig.parameters:
            parameters += [inspect.Parameter("ext", keyword_only)]
        if "request" not in old_sig.parameters:
            parameters += [inspect.Parameter("request", keyword_only)]
        new_sig = old_sig.replace(parameters=parameters)
        wrapper.__signature__ = new_sig

        # reach a bit into pytest internals to hoist the marks from
        # our wrapped function
        new_marks = getattr(func, "pytestmark", []) + wrapper.pytestmark
        wrapper.pytestmark = new_marks

        return wrapper

    return decorator


def load_static_earth_relief():
    """
    Load the static_earth_relief file for internal testing.

    Returns
    -------
    data : xarray.DataArray
        A grid of Earth relief for internal tests.
    """
    fname = which("@static_earth_relief.nc", download="c")
    return load_dataarray(fname)


def skip_if_no(package):
    """
    Generic function to help skip tests when required packages are not present on the
    testing system.

    This function returns a pytest mark with a skip condition that will be
    evaluated during test collection. An attempt will be made to import the
    specified ``package``.

    The mark can be used as either a decorator for a test class or to be
    applied to parameters in pytest.mark.parametrize calls or parametrized
    fixtures. Use pytest.importorskip if an imported moduled is later needed
    or for test functions.

    If the import is unsuccessful, then the test function (or test case when
    used in conjunction with parametrization) will be skipped.

    Adapted from
    https://github.com/pandas-dev/pandas/blob/v2.1.4/pandas/util/_test_decorators.py#L121

    Parameters
    ----------
    package : str
        The name of the required package.

    Returns
    -------
    pytest.MarkDecorator
        A pytest.mark.skipif to use as either a test decorator or a
        parametrization mark.
    """
    import pytest

    try:
        _ = importlib.import_module(name=package)
        has_package = True
    except ImportError:
        has_package = False
    return pytest.mark.skipif(not has_package, reason=f"Could not import '{package}'")
