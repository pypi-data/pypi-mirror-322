"""
kndxhz_tools

A collection of useful tools for various tasks.
"""

__version__ = "0.1.0"
__author__ = "kndxhz"

import subprocess

def version():
    """返回版本号"""
    return __version__

def author():
    """返回作者"""
    return __author__



def get_ip(use_all: bool = False) -> list:
    """

    
    作用:
        获取当前主机的公网IP地址 
    
    参数:
        use_all - 是否获取全部,False则获取优先地址 - bool (可选,默认值: False)
    
    返回:
        如果use_all为True,则返回一个包含所有IP地址的列表,否则返回一个包含一个优先地址的字符串
        列表:```[ip.sb,4.ipw.cn,6.ipw.cn,test.ipw.cn]```
    

    """
    
    if use_all:
        ip = []
        ip.append(subprocess.check_output("curl ip.sb", shell=True).decode().strip())
        ip.append(subprocess.check_output("curl 4.ipw.cn", shell=True).decode().strip())
        ip.append(subprocess.check_output("curl 6.ipw.cn", shell=True).decode().strip())
        ip.append(subprocess.check_output("curl test.ipw.cn", shell=True).decode().strip())
    else:
        ip = subprocess.check_output("curl test.ipw.cn", shell=True).decode().strip()
          
    return ip

print(f"""欢迎使用 kndxhz_tools v{__version__}~""")

if __name__ == "__main__":
    print(get_ip())