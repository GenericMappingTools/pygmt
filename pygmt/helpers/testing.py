"""
Helper functions for testing.
"""
import inspect
import os
import string

from matplotlib.testing.compare import compare_images

from ..exceptions import GMTImageComparisonFailure
from ..figure import Figure


def check_figures_equal(*, extensions=("png",), tol=0.0, result_dir="result_images"):
    """
    Decorator for test cases that generate and compare two figures.

    The decorated function must take two arguments, *fig_ref* and *fig_test*,
    and draw the reference and test images on them. After the function
    returns, the figures are saved and compared.

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

    >>> @check_figures_equal(result_dir="tmp_result_images")
    ... def test_check_figures_equal(fig_ref, fig_test):
    ...     fig_ref.basemap(projection="X5c", region=[0, 5, 0, 5], frame=True)
    ...     fig_test.basemap(projection="X5c", region=[0, 5, 0, 5], frame="af")
    >>> test_check_figures_equal()
    >>> assert len(os.listdir("tmp_result_images")) == 0
    >>> shutil.rmtree(path="tmp_result_images")  # cleanup folder if tests pass

    >>> @check_figures_equal(result_dir="tmp_result_images")
    ... def test_check_figures_unequal(fig_ref, fig_test):
    ...     fig_ref.basemap(projection="X5c", region=[0, 5, 0, 5], frame=True)
    ...     fig_test.basemap(projection="X5c", region=[0, 3, 0, 3], frame=True)
    >>> with pytest.raises(GMTImageComparisonFailure):
    ...     test_check_figures_unequal()
    >>> for suffix in ["", "-expected", "-failed-diff"]:
    ...     assert os.path.exists(
    ...         os.path.join(
    ...             "tmp_result_images",
    ...             f"test_check_figures_unequal{suffix}.png",
    ...         )
    ...     )
    >>> shutil.rmtree(path="tmp_result_images")  # cleanup folder if tests pass
    """
    ALLOWED_CHARS = set(string.digits + string.ascii_letters + "_-[]()")
    KEYWORD_ONLY = inspect.Parameter.KEYWORD_ONLY

    def decorator(func):
        import pytest

        os.makedirs(result_dir, exist_ok=True)
        old_sig = inspect.signature(func)

        @pytest.mark.parametrize("ext", extensions)
        def wrapper(*args, ext, request, **kwargs):
            if "ext" in old_sig.parameters:
                kwargs["ext"] = ext
            if "request" in old_sig.parameters:
                kwargs["request"] = request

            file_name = "".join(c for c in request.node.name if c in ALLOWED_CHARS)
            try:
                fig_ref = Figure()
                fig_test = Figure()
                func(*args, fig_ref=fig_ref, fig_test=fig_test, **kwargs)
                ref_image_path = os.path.join(result_dir, f"{file_name}-expected.{ext}")
                test_image_path = os.path.join(result_dir, f"{file_name}.{ext}")
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
                    os.remove(ref_image_path)
                    os.remove(test_image_path)
                else:  # Images are not the same
                    for key in ["actual", "expected", "diff"]:
                        err[key] = os.path.relpath(err[key])
                    raise GMTImageComparisonFailure(
                        "images not close (RMS %(rms).3f):\n\t%(actual)s\n\t%(expected)s "
                        % err
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
            parameters += [inspect.Parameter("ext", KEYWORD_ONLY)]
        if "request" not in old_sig.parameters:
            parameters += [inspect.Parameter("request", KEYWORD_ONLY)]
        new_sig = old_sig.replace(parameters=parameters)
        wrapper.__signature__ = new_sig

        # reach a bit into pytest internals to hoist the marks from
        # our wrapped function
        new_marks = getattr(func, "pytestmark", []) + wrapper.pytestmark
        wrapper.pytestmark = new_marks

        return wrapper

    return decorator
