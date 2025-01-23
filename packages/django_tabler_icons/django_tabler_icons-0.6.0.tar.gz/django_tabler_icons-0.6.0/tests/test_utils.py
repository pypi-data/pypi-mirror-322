import pathlib
import shutil
import tempfile

import pytest

from tabler_icons import utils


def test_download_icons():
    """Test that the icons are downloaded correctly."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        download_dir = pathlib.Path(tmp_dir) / "icons"
        utils.download_icons(download_dir)
        assert download_dir.exists()
        assert any(download_dir.iterdir())
        # check if there are svg files
        assert any(f.suffix == ".svg" for f in download_dir.iterdir())
        # cleanup
        shutil.rmtree(download_dir)
