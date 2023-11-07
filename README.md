# ProtoRH project

Groupe de **PHAN** et **ZHU**

## Summary

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
  - [Department management](usage.md#department-management)
    - [get all department](usage.md#get-all-department)
    - [Create a department](usage.md#create-a-department)
    - [Get all users from a department](usage.md#get-all-users-from-a-department)
    - [Add users to department](usage.md#add-users-to-department)
    - [Remove user from department](usage.md#remove-user-from-department)
  - [Events management](usage.md#events-management)
    - [Get all events](usage.md#get-all-events)
    - [Get event by id](usage.md#get-event-by-id)
    - [Delete event by id](usage.md#delete-event-by-id)
    - [Update event](usage.md#update-event)
    - [Create event](usage.md#create-event)
    - [Update or Create an event](usage.md#update-or-create-an-event)
  - [Requests management](usage.md#requests-management)
    - [Get all requests](usage.md#get-all-requests)
    - [Get request by ID](usage.md#get-request-by-id)
    - [Add a request](usage.md#add-a-request)
    - [Close a request](usage.md#close-a-request)
    - [Update a request](usage.md#update-a-request)


## File organization

[Go to summary](#summary)

```bash
/
├── assets/ # auto created when using upload API route
├── front/ # protoRH front
│   ├── public/
│   │   └── favicon.svg
│   ├── src/
│   │   ├── components/
│   │   │   ├── Alert.astro
│   │   │   ├── Button.astro
│   │   │   ├── Card.astro
│   │   │   ├── Code.astro
│   │   │   ├── Input.astro
│   │   │   ├── Render.astro
│   │   │   └── Select.astro
│   │   ├── layouts/
│   │   │   └── Layout.astro
│   │   ├── lib/
│   │   │   ├── api.ts
│   │   │   └── filesystem.ts
│   │   ├── pages/
│   │   │   ├── connect.astro
│   │   │   ├── departments.astro
│   │   │   ├── disconnect.astro
│   │   │   ├── docs.astro
│   │   │   ├── events.astro
│   │   │   ├── index.astro
│   │   │   ├── request-rh.astro
│   │   │   └── users.astro
│   │   ├── utils/
│   │   │   └── helper.ts
│   │   └── env.d.ts
│   ├── astro.config.mjs
│   ├── package.json
│   ├── README.md
│   ├── tsconfig.json
│   └── yarn.lock
├── protorh/
│   ├── api/ # handle docs bug
│   ├── lib/
│   │   └── auth.py
│   ├── routes/
│   │   ├── connect.py
│   │   ├── department.py
│   │   ├── events.py
│   │   ├── requestRH.py
│   │   ├── test.py
│   │   ├── upload.py
│   │   └── users.py
│   ├── utils/
│   │   └── helper.py
│   ├── create_db.py
│   ├── database.py
│   ├── database_rh.psql
│   ├── env.py
│   ├── main.py
│   ├── models.py
│   ├── protorh.env
│   └── serializers.py
├── build.sh
├── README.md
├── requirements.txt
└── run.sh
```
