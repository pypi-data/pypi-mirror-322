#!/usr/bin/env python3
"""Test utilities."""


import contextlib
import datetime
import pathlib
import tempfile


@contextlib.contextmanager
def tmp_file(text=None, extension=".txt"):
    """
    Create a temporary file in a temporary directory.

    Returns:
        A 3-tuple with the file content, the file modification time and the
        path.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = pathlib.Path(tmp_dir) / f"tmp{extension}"
        if text is None:
            text = "placeholder text"
        tmp_path.write_text(text)
        mtime = datetime.datetime.fromtimestamp(
            tmp_path.stat().st_mtime, datetime.timezone.utc
        )
        yield text, mtime, tmp_path
