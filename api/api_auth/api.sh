#!/bin/bash
# correct password Rxinui: pass123!?
# correct password Jxsset: 0v3rk1ll

curl 127.0.0.1:3000/user/login \
-H "Content-Type: application/json" \
-X POST \
-d '
{"username": "Jxsset",
"email": "jxsset@dojoplateforme.com",
"password": "0v3rk1ll"}
' 