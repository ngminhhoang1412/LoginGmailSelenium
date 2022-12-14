# **Google login with Selenium**

## Overview
This is a small package to log in to Google account with Selenium. After signin,
Chrome profile of that user will be create and stored. With Chrome profile you can do so many automatic things
with it.

Always active extension is installed by default.
>This has been developed for testing purposes only.
> Any action you take using this script is strictly at your own risk. 
> I will not be liable for any losses or damages you face using this script.

## Requirement
Must have Python <= 3.9 and Google Chrome installed.

## Usage
```pycon
pip install login_gmail_selenium
```
And then on example.py
```pycon
from login_gmail_selenium.util.profile import ChromeProfile

profile = ChromeProfile(email, password, backup_email)
# To allow downloads add insecure=True to ChromeProfile
driver = profile.retrieve_driver()
profile.start()
# Do whatever with driver afterward
driver.get('https://www.google.com/')
...
```
Add folder extension/ if you want custom extensions for Chrome (.crx or .zip). 
Your folder should look like this
```cvs
/temp
    /profiles
      /profile1
      /profile2
/extension
    extension1.zip
    extension2.crx
example.py
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
3. Create (if not have) and check for version on setup.py

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

## License
Copyright ?? 2022 [MoliGroup](https://moligroup.co/), [MIT license](./LICENSE). 
For an improvement or a bug please feel free to open a PR

For work information please contact ngminhhoang1412@gmail.com or 
[LinkedIn](https://www.linkedin.com/in/ho%C3%A0ng-nguy%E1%BB%85n-1b13481b7/).
