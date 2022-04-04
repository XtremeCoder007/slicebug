from cx_Freeze import Executable, setup

from slicebug.version import VERSION

setup(
    name="slicebug",
    version=VERSION,
    description="A CLI for controlling Cricut cutters.",
    executables=[Executable("slicebug/__main__.py", target_name="slicebug")],
    options={
        "build_exe": {
            "excludes": ["tkinter"],
            "zip_include_packages": ["*"],
            "zip_exclude_packages": [],
            "include_files": ["README.md", "docs", "examples"],
        }
    },
)
