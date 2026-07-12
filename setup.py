from setuptools import setup, find_packages

setup(
    name="aizen-todo",
    version="2.0.0",
    packages=find_packages(include=["aizen_todo", "aizen_todo.*"]),
    install_requires=["rich>=13.0", "click>=8.0"],
    entry_points={
        "console_scripts": [
            "aizen-todo = aizen_todo.__main__:main",
        ],
    },
    python_requires=">=3.8",
)
