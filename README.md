# **Google login with Selenium**

## Overview
This is a small package to log in to Google account with Selenium. After signin,
Chrome profile of that user will be create and stored. With Chrome profile you can do so many automatic things
with it.
>This has been developed for testing purposes only.
> Any action you take using this script is strictly at your own risk. 
> I will not be liable for any losses or damages you face using this script.

## Requirement
Must have Python <= 3.9 and Google Chrome installed

## Usage
  ```python
pip install login_gmail_selenium
```
And then call
  ```python
login(email, password, backup_email)
```

## Upload to pypi

1. Organize your code into proper file hierarchy
2. Add a LICENSE and a README.md if not already done

```cvs
/demopackage
    __init__.py
    demopackage.py
    /demosubpackage
      __init__.py
      demosubpackage.py
    /tests
        test_package.py
LICENSE
setup.py
```
3. Create your setup.py

```python
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
```
4. Create distribution archive files

Before you begin, run the following command to update required packages:
  ```python
pip install --upgrade setuptools wheel
python setup.py sdist bdist_wheel
```
This should create a dist/ folder in your main directory with the compressed files for your package!
5. Upload your distribution archives to PyPI
  ```python
pip install --upgrade twine
python setup.py sdist bdist_wheel
twine upload dist/*
```
You will be prompted for your PyPI login credentials, and then the upload will begin. Now you should be able to log in to your PyPI account and see your package.

## License
Copyright © 2022 MoliGroup, [MIT licensed](./LICENSE).
