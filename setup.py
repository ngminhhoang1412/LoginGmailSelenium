import setuptools

with open("README.md", 'r') as fh:
    long_description = fh.read()

with open('requirements.txt', 'r', encoding='utf-16') as f:
    requirements = [line.rstrip('\n') for line in f]

setuptools.setup(
    name="login_gmail_selenium",
    version="1.0.9",
    author="Minh Hoang",
    author_email="ngminhhoang1412@gmail.com",
    description="A python package for login google by selenium",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ngminhhoang1412/LoginGmailSelenium",
    include_package_data=True,
    package_data={'': ['extension/*']},
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ),
    install_requires=requirements
)
