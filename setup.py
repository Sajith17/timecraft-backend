import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

__version__ = "0.0.0"

REPO_NAME = "timecraft-backend"
AUTHOR_USER_NAME = "Sajith17"
SRC_REPO = "timecraft"
AUTHOR_EMAIL = "sajithseelan17@gmail.com"

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    AUTHOR_EMAIL=AUTHOR_EMAIL,
    description="Automatic timetable generator using Genetic Algorithm",
    long_description_content=long_description,
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
)
