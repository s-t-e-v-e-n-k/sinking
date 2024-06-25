import pathlib


def create_file_in_dir(
    basedir: pathlib.Path, name: str, dirname=None
) -> pathlib.Path:
    if dirname is not None:
        newdir = basedir / dirname
    else:
        newdir = basedir / name
    newdir.mkdir()
    filename = newdir / f"{name}.bar"
    filename.touch()
    return filename
