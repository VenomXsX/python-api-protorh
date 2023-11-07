## Summary

[Back to README](README.md)

- [File organization](README.md#file-organization)
- [Usage](usage.md)
  - [It works](usage.md#it-works)
  - [Authentication](usage.md#authentication)
    - [connect](usage.md#connect)
    - [revalidate](usage.md#revalidate)
  - [User picture](usage.md#user-picture)
    - [upload picture](usage.md#upload-picture)
    - [get user's picture](usage.md#get-users-picture)
  - [User data](usage.md#user-data)
    - [get all](usage.md#get-all-users-data)
    - [get me](usage.md#get-me-current-connected-user)
    - [get by id](usage.md#get-user-by-id)
    - [create an user](usage.md#create-an-user)
    - [delete an user by id](usage.md#delete-an-user-by-id)
    - [update user's data](usage.md#update-users-data)
    - [update user's password](usage.md#update-users-password)

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

#### Connect

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

#### Revalidate

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

### User management

#### upload picture

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

#### get user's picture

[Go to summary](#summary)

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

#### **Create** a user

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

Replace `{user_id}`

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

#### **Update** user's data

update a specific user column(s) \
for this example we update only `firstname`

[Go to summary](#summary)

Replace `{user_id}`

> - Endpoint: `/api/user/update/{user_id}`
> - Method: `PATCH`
> - JWT Required: `true`

```bash
curl  -X PATCH \
  'http://127.0.0.1:4242/api/user/update/7' \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "firstname": "first test up"
}'

# response 200
{
  "message": "Successfully updated, id: 7",
  "data": {
    "id": "7",
    "firstname": "first test up"
  }
}
```

#### **Update** user's password

update password for specific user

[Go to summary](#summary)

Replace `{user_id}`

> - Endpoint: `/api/user/password`
> - Method: `PATCH`
> - JWT Required: `false`

```bash
curl  -X PATCH \
  'http://127.0.0.1:4242/api/user/password' \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "email": "test@test.test",
  "password": "test",
  "new_password": "newtest",
  "repeat_new_password": "newtest"
}'

# response 200
"User's password has been updated"
```

### Department management

#### Get all

[Go to summary](#summary)

gets all departments

> - Endpoint: `/api/departments`
> - Method: `GET`
> - JWT Required: `false`

```bash
$ curl --request GET \
  --url http://127.0.0.1:4242/api/departments \

# response 200
[
  {
    "id": 1,
    "name": "somewhere"
  },
  ...
]

# response 404
{
	"detail": "There's no departments"
}
```

#### Create a department

[Go to summary](#summary)

Create a department

> - Endpoint: `/api/departments`
> - Method: `POST`
> - JWT Required: `false`

```bash
$ curl --request POST \
  --url http://127.0.0.1:4242/api/departments \
  --header 'Content-Type: application/json' \
  --data '{
	"name": "<departname>"
}'

# response 200
{
	"message": "Successfully added: <departname>"
}

# response 500
{
	"detail": "Something went wrong, please retry"
}
```

#### Get all users from a department

[Go to summary](#summary)

Get all users using department id

> - Endpoint: `/api/departments/{department_id}/users`
> - Method: `GET`
> - JWT Required: `True`

```bash
$ curl --request GET \
  --url http://127.0.0.1:4242/api/departments/9/users \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json'

# response 200
[
	{
		<user informations>
	},
  ...
]

# response 404
{
	"detail": "No department or user assigned"
}
```

#### Add users to department

[Go to summary](#summary)

Add users to a department

> - Endpoint: `/api/departments/{department_id}/users/add`
> - Method: `POST`
> - JWT Required: `True`

```bash
$ curl --request POST \
  --url http://127.0.0.1:4242/api/departments/{department_id}/users/add \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '[<id>,...]'

# response 200
"updated successfully, <rowcount> affected"
```

#### Remove user

[Go to summary](#summary)

Remove users from department

> - Endpoint: `/api/departments/{department_id}/users/remove`
> - Method: `POST`
> - JWT Required: `True`

```bash
$ curl --request POST \
  --url http://localhost:4242/api/departments/9/users/remove \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '[<id>,...]'

# response 200
"updated successfully, <rowcount> affected"
```

### Events management

#### Get all events

[Go to summary](#summary)

Get all events

> - Endpoint: `/api/events/`
> - Method: `GET`
> - JWT Required: `false`

```bash
$ curl --request GET \
  --url http://localhost:4242/api/events \
  --header 'Content-Type: application/json' \

# response 200
"string"
```

#### Get event by id

[Go to summary](#summary)

Get event by their ID

> - Endpoint: `/api/events/{id}`
> - Method: `GET`
> - JWT Required: `false`

```bash
$ curl --request GET \
  --url http://localhost:4242/api/events \
  --header 'Content-Type: application/json' \

# response 200
"string"

# response 422
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

#### Delete event by id

[Go to summary](#summary)

Delete an event by uts ID

> - Endpoint: `/api/events/{id}`
> - Method: `DELETE`
> - JWT Required: `false`

```bash
$ curl --request DELETE \
  --url http://localhost:4242/api/events \
  --header 'Content-Type: application/json' \

# response 200
"string"

# response 422
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

#### Update event

[Go to summary](#summary)

Update an event by its ID

> - Endpoint: `/api/events/{id}`
> - Method: `PATCH`
> - JWT Required: `false`

```bash
$ curl --request PATCH \
  --url http://localhost:4242/api/events/{id} \
  --header 'Authorization: Bearer <token> \
  --header 'Content-Type: application/json' \
  --data '{
  "name": "string",
  "date": "2023-11-07",
  "description": "string",
  "user_id": 0,
  "department_id": 0
}'

# response 200
"string"

# response 422
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

#### Create event

[Go to summary](#summary)

Create an event

> - Endpoint: `/api/events/create`
> - Method: `POST`
> - JWT Required: `false`

```bash
$ curl --request PATCH \
  --url http://localhost:4242/api/events/create \
  --header 'Authorization: Bearer <token> \
  --header 'Content-Type: application/json' \
  --data '{
  "name": "string",
  "date": "2023-11-07",
  "description": "string",
  "user_id": 0,
  "department_id": 0
}'

# response 200
"string"

# response 422
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

#### Update or Create an event

[Go to summary](#summary)

Update or create an event

> - Endpoint: `/api/events/{id}`
> - Method: `PUT`
> - JWT Required: `false`

```bash
$ curl --request PATCH \
  --url http://localhost:4242/api/events/{id} \
  --header 'Authorization: Bearer <token> \
  --header 'Content-Type: application/json' \
  --data '{
  "name": "string",
  "date": "2023-11-07",
  "description": "string",
  "user_id": 0,
  "department_id": 0
}'

# response 200
"string"

# response 422
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```
