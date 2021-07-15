import os
import io
import re
import sys
import requests
import warnings
import shutil
import subprocess
from packaging import version
from bs4 import BeautifulSoup
from zipfile import ZipFile
from requests.auth import HTTPProxyAuth

warnings.filterwarnings("ignore")

class CheckUpdateVersionOfDCT:
    def __init__(self, _path, proxy_user=None, proxy_pass=None, proxy_name=None, proxy_port=None):
        self.dct_url = "https://owasp.org/www-project-dependency-check/"
        self.dct_system_path = _path
        self.proxyusername = proxy_user
        self.proxypassword = proxy_pass
        self.proxyname = proxy_name
        self.proxyport = proxy_port
        self.local_dct_version = None
        self.web_dct_version = None
        self.status = False

    def getDCTDataFromWeb(self, url):
        try:
            request = requests.Session()
            if self.proxyusername and self.proxypassword:
                proxies = {
                    "http://" + str(self.proxyusername) + ":" + str(self.proxyport),
                    "https://" + str(self.proxyusername) + ":" + str(self.proxyport)
                }
                auth = HTTPProxyAuth(self.proxyusername, self.proxypassword)
                request.proxies = proxies
                request.auth = auth
            request.verify = False
            data = request.get(url=url)
        except Exception as e:
            data = None
            print("error in getDataFromWeb method.......")
            sys.exit(e)
        return data

    def updateDCT(self, parsed_dct_data):
        try:
            dct_path = os.path.dirname(os.path.dirname(self.dct_system_path))
            print('[INFO] Upgrading Dependency Check Tool ....')
            dct_download_url = parsed_dct_data.select("div[role=complementary] ul li a[href]")[0].get('href')
            dct_data = self.getDCTDataFromWeb(dct_download_url)
            if os.path.isdir(dct_path):
                shutil.rmtree(dct_path)
                with ZipFile(io.BytesIO(dct_data.content), 'r') as zf:
                    zf.extractall(path=os.path.dirname(dct_path))
                    self.status = True
            print('[INFO] Uprade Completed ......')
        except Exception as e:
            print(e)
        return self.status

    def versionCheck(self):
        try:
            self.local_dct_version = subprocess.check_output([self.dct_system_path, '--version'], universal_newlines=True).strip('\n').split(' ')[-1]
            dct_data = self.getDCTDataFromWeb(self.dct_url)
            parsed_dct_data = BeautifulSoup(dct_data.text, 'lxml')
            self.web_dct_version = parsed_dct_data.find(string=re.compile('''Version \\d+(?:\\.\\d+)+''')).split(" ")[-1]
            if version.parse(self.web_dct_version) > version.parse(self.local_dct_version):
                print()
                print("[Warn] Currently you are using lower version of Dependency Check Tool("+self.local_dct_version+").")
                print("[Warn] There is Higher version of Dependency Check Tool("+self.web_dct_version+") is avaliable in web.")
                print()
                self.updateDCT(parsed_dct_data)
            else:
                print()
                print("[Info] Checking Update for DCT is completed.")
                print("[Info] Already you are using igher version DCT.")
                print()
        except Exception as e:
            sys.exit(e)

        return ""


if __name__ == "__main__":
    
    check = CheckUpdateVersionOfDCT()
    check.versionCheck()
