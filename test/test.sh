#!/bin/bash

curl -X 'POST' \
  'http://127.0.0.1:8000/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "admin",
  "email": "admin@example.com",
  "password": "admin"
}';
echo \n;
curl -X 'POST' \
  'http://127.0.0.1:8000/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "zhu",
  "email": "zhu@example.com",
  "password": "zhu"
}';echo \n;
curl -X 'POST' \
  'http://127.0.0.1:8000/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "lou",
  "email": "lou@example.com",
  "password": "lou"
}';echo \n;
curl -X 'POST' \
  'http://127.0.0.1:8000/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "testuser",
  "email": "testuser@example.com",
  "password": "testuser"
}';echo \n;
curl -X 'POST' \
  'http://127.0.0.1:8000/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "testuser",
  "email": "testuser@example.com",
  "password": "testuser"
}';echo \n;
curl -X 'POST' \
  'http://127.0.0.1:8000/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "testuser1",
  "email": "testuser1@example.com",
  "password": "testuser1"
}';echo \n;
curl -X 'GET' \
  'http://127.0.0.1:8000/users/' \
  -H 'accept: application/json';echo \n;
curl -X 'GET' \
  'http://127.0.0.1:8000/users/1' \
  -H 'accept: application/json';echo \n;
curl -X 'PUT' \
  'http://127.0.0.1:8000/users/3' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "louzunxian",
  "password": "louzunxian",
  "email": "louzunxian@example.com"
}';echo \n;
curl -X 'DELETE' \
  'http://127.0.0.1:8000/users/5' \
  -H 'accept: */*';echo \n;
curl -X 'DELETE' \
  'http://127.0.0.1:8000/users/5' \
  -H 'accept: */*';echo \n;
curl -X 'POST' \
  'http://127.0.0.1:8000/user/auth/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "string",
  "email": "user@example.com",
  "password": "string"
}';echo \n;
curl -X 'POST' \
  'http://127.0.0.1:8000/user/auth/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=admin&password=admin&scope=&client_id=string&client_secret=string';echo \n;
curl -X 'GET' \
  'http://127.0.0.1:8000/user/auth/me' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTczNzkwNDI3MX0.uuzxMn0qT8pEUflb_pBx1xsQw_3unQHVxQCF_nJ__7w';echo \n
echo post:;
curl -X 'POST' \
  'http://127.0.0.1:8000/posts/posts/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "第一个文章",
  "user_id": 1,
  "tags": [
    "测试标签1"
  ]
}';echo \n;
curl -X 'POST' \
  'http://127.0.0.1:8000/posts/posts/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "文章",
  "user_id": 2,
  "tags": [
    "测试标签1",
    "测试标签2"
  ]
}';echo \n;
curl -X 'POST' \
  'http://127.0.0.1:8000/posts/posts/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "第一个文章",
  "user_id": 3,
  "tags": [
    "测试标签1",
    "测试标签2"
  ]
}';echo \n;
curl -X 'POST' \
  'http://127.0.0.1:8000/posts/posts/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "第一个文章",
  "user_id": 4,
  "tags": [
    "测试标签1",
    "测试标签2",
    "测试标签3"
  ]
}';echo \n;
curl -X 'GET' \
  'http://127.0.0.1:8000/posts/posts/author/1' \
  -H 'accept: application/json';echo \n;
curl -X 'GET' \
  'http://127.0.0.1:8000/posts/posts/' \
  -H 'accept: application/json';echo \n;

curl -X 'GET' \
  'http://127.0.0.1:8000/tags/' \
  -H 'accept: application/json'