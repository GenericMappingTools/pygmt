import os
import sys
from pathlib import Path
from matplotlib.testing.compare import compare_images
from ..exceptions import GMTImageComparisonFailure


def check_figures_equal(fig_ref, fig_test, fig_prefix=None, tol=0.0):
    result_dir = "result_images"

    if not fig_prefix:
        try:
            fig_prefix = sys._getframe(1).f_code.co_name
        except VauleError:
            raise GMTInvalidInput("fig_prefix is required.")

    os.makedirs(result_dir, exist_ok=True)

    ref_image_path = os.path.join(result_dir, fig_prefix + '-expected.png')
    test_image_path = os.path.join(result_dir, fig_prefix + '.png')

    fig_ref.savefig(ref_image_path)
    fig_test.savefig(test_image_path)

    err = compare_images(ref_image_path, test_image_path, tol, in_decorator=True)

    if err is None:  # Images are the same
        os.remove(ref_image_path)
        os.remove(test_image_path)
    else:
        for key in ["actual", "expected"]:
            err[key] = os.path.relpath(err[key])
        raise GMTImageComparisonFailure(
            'images not close (RMS %(rms).3f):\n\t%(actual)s\n\t%(expected)s '
             % err)
