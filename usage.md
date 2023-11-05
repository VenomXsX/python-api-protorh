## Summary

[Back to README](README.md)

- [File organization](README.md#file-organization)
- [Usage](usage.md)
  - [It works](usage.md#it-works)
  - [Authentication](usage.md#authentication)
  - [User picture](usage.md#user-picture)
  - [User data](usage.md#user-data)
    - [get all](usage.md#get-all-users-data)
    - [get me](usage.md#get-me-current-connected-user)
    - [get by id](usage.md#get-user-by-id)
    - [create an user](usage.md#create-an-user)
    - [delete an user by id](usage.md#delete-an-user-by-id)

## usage

### It works

[Go to summary](#summary)

> - Endpoint: `/`
> - Method: `GET`

```bash
$ curl  -X GET \
  'http://127.0.0.1:4242/'

# response 200
"REST API is working yey"
```

### Authentication

[Go to summary](#summary)

Connect with **email** and **password**, it accepts **expire** (in minutes)

> - Endpoint: `/api/connect`
> - Method: `POST`
> - JWT Required: `false`

```bash
$ curl  -X POST \
  'http://127.0.0.1:4242/api/connect' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "email": "aze@aze",
  "password": "aze",
  "expire": 60
}'

# response 200
{
  "access_token": "<token>",
  "token_type": "bearer"
}
```

Revalidate token (for front app)

> - Endpoint: `/api/revalidate`
> - Method: `POST`
> - JWT Required: `true`

```bash
$ curl  -X GET \
  'http://127.0.0.1:4242/api/revalidate' \
  --header 'Authorization: bearer <token>'

# response 200
{
  "access_token": "<token>",
  "token_type": "bearer"
}
```

### User picture

[Go to summary](#summary)

**Upload an image**, only accept `png`, `jpeg` and `gif`. \
Replace `<path_to_file>` and `{user_id}`

> - Endpoint: `/api/upload/picture/user/{user_id}`
> - Method: `POST`
> - JWT Required: `false`

```bash
$ curl  -X POST \
  'http://127.0.0.1:4242/api/upload/picture/user/<user_id>' \
  --form 'image=@<path_to_file>'

# response 200
{
  "message": "picture uploaded"
}
```

**Get user's image** \
Replace `{user_id}`

> - Endpoint: `/api/picture/user/{user_id}`
> - Method: `GET`
> - JWT Required: `false`

```bash
curl  -X GET \
  --JO 'http://127.0.0.1:4242/api/picture/user/{user_id}'

# response 200
<image>
```

> flag: `-JO` is to get original filename

### user data

#### Get **all users data**

[Go to summary](#summary)

> - Endpoint: `/api/user`
> - Method: `GET`
> - JWT Required: `false`

```bash
$ curl  -X GET \
  'http://127.0.0.1:4242/api/user'

# response 200
[
  { <user data> },
  { <user data> },
  ...
]
```

#### Get **me** (current connected user)

[Go to summary](#summary)

> - Endpoint: `/api/user/me`
> - Method: `GET`
> - JWT Required: `true`

```bash
$ curl  -X GET \
  'http://127.0.0.1:4242/api/user/me' \
  --header 'Authorization: Bearer <token>'

# response 200
{
  <current user data>
}
```

#### Get **user by id**

[Go to summary](#summary)

Replace `{user_id}`

> - Endpoint: `/api/user/{user_id}`
> - Method: `GET`
> - JWT Required: `true`

```bash
$ curl  -X GET \
  'http://127.0.0.1:4242/api/user/{user_id}' \
  --header 'Authorization: Bearer <token>'

# response 200
{
  <user data>
}
```

#### **Create** an user

[Go to summary](#summary)

> - Endpoint: `/api/user/create`
> - Method: `POST`
> - JWT Required: `false`

```bash
$ curl  -X POST \
  'http://127.0.0.1:4242/api/user/create' \
  --header 'Authorization: Bearer <token>' \
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

# response 200
{
  <user data>
}
```

#### **Delete** an user by id

[Go to summary](#summary)

Replace {user_id}

> - Endpoint: `/api/user/delete/{user_id}`
> - Method: `DELETE`
> - JWT Required: `false`

```bash
$ curl  -X POST \
  'http://127.0.0.1:4242/api/user/delete/{user_id}'

# response 200
{
  <user data>
}
```
