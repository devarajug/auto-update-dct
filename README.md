# Auto Update Dependency Check Tool
The utility helps you to automatically update the **`Dependency Check Tool`** when the new version of tool is released to web.

# Installation
You can install by using following command
```
pip install auto-update-dct

pip install auto-update-dct --user
```
if **`pip`** is not working then try using **`pip3`**

# How to Use
```
from auto_update_dct.check import CheckUpdateVersionOfDCT

tool_path = "D:\\path to dependency check tool\\bin\\dependency-check.bat"  #windows
tool_path = "D:\\path to dependency check tool\\bin\\dependency-check.sh"  #Linux

check = CheckUpdateVersionOfDCT(_path = tool_path)

# if you are in behind corporate proxy
'''
check = CheckUpdateVersionOfDCT(
    _path = tool_path,
    proxy_name = 'proxy.company.com',
    proxy_port = '5555',
    proxy_user = 'proxyusername',
    proxy_pass = 'XXXXX'
)
'''
check.versionCheck()
```

# License

Copyright (c) 2021 Devaraju Garigapati

This repository is licensed under the [MIT](https://opensource.org/licenses/MIT) license. See [LICENSE](https://opensource.org/licenses/MIT) for details.
