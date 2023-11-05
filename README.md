# ProtoRH project

Groupe de **PHAN** et **ZHU**

## Summary

- [File organization](README.md#file-organization)
- [Usage](usage.md)
  - [It works](usage.md#it-works)
  - [Authentication](usage.md#authentication)
  - [User picture](usage.md#user-picture)

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
