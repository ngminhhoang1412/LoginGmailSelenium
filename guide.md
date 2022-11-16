# **Upload to pypi guide**

1. Organize your code into proper file hierarchy
2. Add a LICENSE and a README.md if not already done

#### Example
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
>Before you begin, run the following command to update required packages:
  ```python
pip install --upgrade setuptools wheel
python setup.py sdist bdist_wheel
```
> This should create a dist/ folder in your main directory with the compressed files for your package!
5. Upload your distribution archives to PyPI
  ```python
pip install --upgrade twine
python setup.py sdist bdist_wheel
```
>You will be prompted for your PyPI login credentials, and then the upload will begin. Now you should be able to log in to your PyPI account and see your package.

6. Usage
  ```python
pip install login_gmail_selenium
```
And then call
  ```python
login(email, password, backup_email)
```
