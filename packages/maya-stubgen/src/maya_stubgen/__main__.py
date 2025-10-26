import site
import sys
import sysconfig
from pathlib import Path

maya_python_versions = {
    "2023": "3.7",
    "2024": "3.10",
    "2025": "3.11",
}

maya_python_paths = {
    "win64": "",
    "darwin": "/Applications/Autodesk/maya{version}/Maya.app/Contents/Frameworks/Python.framework/Versions/Current/",
    "linux": "",
}


"/Applications/Autodesk/maya{version}/Maya.app/Contents/Frameworks/Python.framework/Versions/Current/"


"/Applications/Autodesk/maya2023/Maya.app/Contents/Frameworks/Python.framework/Versions/3.7/lib/python3.7"
"/Applications/Autodesk/maya2024/Maya.app/Contents/Frameworks/Python.framework/Versions/3.10/lib/python3.10"
"/Applications/Autodesk/maya2025/Maya.app/Contents/Frameworks/Python.framework/Versions/3.11/lib/python3.11"

"/Applications/Autodesk/maya2023/Maya.app/Contents/Frameworks/Python.framework/Versions/Current/lib/python3.7/site-packages"
"/Applications/Autodesk/maya2024/Maya.app/Contents/Frameworks/Python.framework/Versions/Current/lib/python3.10/site-packages"
"/Applications/Autodesk/maya2025/Maya.app/Contents/Frameworks/Python.framework/Versions/Current/lib/python3.11/site-packages"


maya_stdlib = Path(sysconfig.get_path("stdlib")).resolve()
venv_paths = ":".join(site.getsitepackages())

print(f"{sys.executable=}")
print(f"{maya_stdlib=}")
print(f"{venv_paths=}")


def ensure_maya() -> None:
    """Checks that maya modules are available, or attempts to rerun the command in a mayapy subprocess"""
    try:
        import maya  # pyright: ignore[reportUnusedImport]

        return
    except ImportError as e:
        import os
        import sys

        if os.path.basename(sys.executable).startswith("mayapy"):
            # prevent recursion
            raise RuntimeError("running with mayapy, but couldn't import maya") from e

    import site
    import subprocess
    import sysconfig
    from pathlib import Path
    from typing import Optional

    def _get_mayapy(path: Path) -> Optional[Path]:
        if (mayapy := (path / "bin" / "mayapy")).is_file():
            return mayapy
        elif (mayapy := mayapy.with_suffix(".exe")).is_file():
            return mayapy
        return None

    def _find_mayapy(path: Path) -> Optional[Path]:
        while True:
            if mayapy := _get_mayapy(path):
                return mayapy
            elif path.parent == path:
                return None

            path = path.parent

    maya_stdlib = Path(sysconfig.get_path("stdlib")).resolve()
    mayapy_path = _find_mayapy(maya_stdlib)
    if not mayapy_path:
        raise RuntimeError(
            f"could not find mayapy location (searched from: {maya_stdlib})"
        )

    import maya_stubgen

    subprocess.run(
        [mayapy_path, "-m", "maya_stubgen.__main__", *sys.argv[1:]],
        env={
            **os.environ,
            "PYTHONPATH": os.getcwd(),
            "MAYASTUB_VENV": ":".join(site.getsitepackages()),
        },
    )
    sys.exit(0)


def main() -> None:
    ensure_maya()
    from .cli import cli

    1 / 0
    cli()


if __name__ == "__main__":
    main()
