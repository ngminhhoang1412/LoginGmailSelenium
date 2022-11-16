# **Turn Your Python Code Into a pip Package**

## Initial Steps

1. Organize your code into the proper file hierarchy
2. Add your `__init__.py` files
3. Add a license and a README.md if not already done

####Example
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
4. Adding a License
5. Create your setup.py file

####Example
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
6. Create your Distribution Archive Files
>Before you begin, run the following command to update needed packages:
  ```python
pip install --upgrade setuptools wheel
python setup.py sdist bdist_wheel
```
> This should create a dist/ folder in your main directory with the compressed files for your package!
7. Upload your distribution archives to PyPI
  ```python
pip install --upgrade twine
python setup.py sdist bdist_wheel
```
>You will be prompted for your PyPI login credentials, and then the upload will begin. Now you should be able to login to your PyPI account and you will see your package. Notice that PyPI displays your README on the package’s main page, so use that space to give useful information about your library.
