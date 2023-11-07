# Demo protoRH

[Back to README](README.md)

Here is the demo

## Create user

```bash
curl  -X POST \
  'http://127.0.0.1:4242/api/user/create' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "email": "test@test.test",
  "password": "test",
  "confirm_pass": "test",
  "firstname": "first test",
  "lastname": "last test",
  "birthday_date": "2000-10-10",
  "address": "an address",
  "postal_code": "a postal code"
}'
```

## get all users

```bash
curl  -X GET \
  'http://127.0.0.1:4242/api/user/'
```

## Update user

```bash
curl  -X PATCH \
  'http://127.0.0.1:4242/api/user/update/14' \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "firstname": "first test updated"
}'
```

## Connect

```bash
curl  -X POST \
  'http://127.0.0.1:4242/api/connect' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "email": "aze@aze",
  "password": "aze",
  "expire": 60
}'
```

## Delete user

```bash
curl  -X DELETE \
  'http://127.0.0.1:4242/api/user/delete/14'
```
