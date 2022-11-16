import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="login_gmail_selenium",
    version="0.0.1",
    author="Minh Hoang",
    author_email="nguyenthanhdungktm@gmail.com",
    description="A python package for login google by selenium",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ngminhhoang1412/LoginGmailSelenium",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ),
)