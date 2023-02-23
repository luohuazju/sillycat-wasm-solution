### Command to Run

```commandline
wagi -e 'PYTHONHOME=/opt/wasi-python/lib/python3.10' -e 'PYTHONPATH=/opt/wasi-python/lib/python3.10' -c modules.toml
```

```commandline
curl http://127.0.0.1:3000
Hello from python on wasi

### Arguments ###

['/wasiconsumer/env.py']

### Env Vars ###

AUTH_TYPE: 
CONTENT_LENGTH: 0
CONTENT_TYPE: 
GATEWAY_INTERFACE: CGI/1.1
HTTP_ACCEPT: */*
HTTP_HOST: 127.0.0.1:3000
HTTP_USER_AGENT: curl/7.61.1
PATH_INFO: 
PATH_TRANSLATED: 
PYTHONHOME: /opt/wasi-python/lib/python3.10
PYTHONPATH: /opt/wasi-python/lib/python3.10
QUERY_STRING: 
REMOTE_ADDR: 127.0.0.1
REMOTE_HOST: 127.0.0.1
REMOTE_USER: 
REQUEST_METHOD: GET
SCRIPT_NAME: /
SERVER_NAME: 127.0.0.1
SERVER_PORT: 3000
SERVER_PROTOCOL: HTTP/1.1
SERVER_SOFTWARE: WAGI/1
X_FULL_URL: http://127.0.0.1:3000/
X_MATCHED_ROUTE: /
X_RAW_PATH_INFO: 

### Files ###

env.py
```