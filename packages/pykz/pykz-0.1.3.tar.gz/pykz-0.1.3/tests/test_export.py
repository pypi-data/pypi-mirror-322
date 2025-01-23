import pykz.io as io

TEX_STRING = r"""
\documentclass{article}
\begin{document}
    hello world.
\end{document}
"""


def test_export_noerrors():
    file = io.__export_to_tempfile(TEX_STRING)
    with open(file, "r") as f:
        reread = f.read()
    assert reread == TEX_STRING, f"Reloaded tex code did not match original, got back\n{reread}"
    import os
    os.remove(file)


def test_preview_noerrors():
    io.export_pdf_from_code(TEX_STRING)
