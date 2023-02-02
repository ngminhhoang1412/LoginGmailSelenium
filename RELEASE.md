# **Release new version**

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
3. Create (if not have) and update version number on setup.py

4. Generate distribution archive files

```pycon
pip install --upgrade setuptools wheel
python setup.py sdist bdist_wheel
```
This should create a dist/ and build/ folder in your main directory with the compressed files of your package!
5. Upload your distribution archives to PyPI
```pycon
pip install --upgrade twine
twine upload dist/*
```
You will be prompted for your PyPI login credentials, and then the upload will begin. 
Now you should be able to log in to your PyPI account and see your package.

## Release on github

1. Create Pull Request to branch `main`, have it reviewed and approved
2. Merge to branch 'main' with tag format `vx.x.x` (eg `v1.0.0`)
3. Prepare release note and create a release at 
[New Release](https://github.com/ngminhhoang1412/LoginGmailSelenium/releases/new)

>Patches and small versions don't need to be released on Github.
