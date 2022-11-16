# **TeraBoxUtility**

## Overview 

>TeraBoxUtility is a tool to quickly upload data to TeraBox. Store large amounts of information securely. 

## Requirement
> TeraBoxUtility use python 9 and chrome driver.
Need to have google chrome to use.



## Usage

In file main.py, Need to specify the path to the directory.

```python
from util.tera import TeraBox

# Set path to folder
# Example D:\test1
tera = TeraBox("D:\\test1")
tera.upload()
```
Create file .env with format like this

```cvs
# Email to login google account.
EMAIL=email:password:backup_email
# Key use to encrypt and decrypt. It is any string. sdfsjd is example.
KEY='sdfsjd'
# App_id in TeraBox
APP_ID='250528'
# Type of file is .zip
FILE_TYPE=.zip
```

## Credit


## License
Copyright © 2022 moligroup