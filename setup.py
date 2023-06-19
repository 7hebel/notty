from setuptools import setup, find_packages

setup(
    name="notty",
    description="LVCS",
    author="gental-py",
    author_email="gental.contact@gmail.com",
    url="https://github.com/gental-py/notty",
    packages=[".", "core"],
    install_requires=[
        'click',
        'colorama',
        'tabulate',
    ],
    entry_points = {
        'console_scripts': [
            "notty = main:main"
        ]
    }
)
