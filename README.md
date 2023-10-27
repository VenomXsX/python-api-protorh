# Groupe de PHAN et ZHU

## Important

use `/api` route at start

## File organization

- `main.py`: main endpoints file
- `models.py`: SQLAlchemy Table models
- `serializers.py`: Pydantic data validation declarations
- `database.py`: Create and connect to database
- `create_db.py`: Create all the tables in the database

- `assets`: auto create


## usage

### Upload picture to user

replace `<path_to_file>` and `{user_id}`

>- Endpoint: `/api/upload/picture/user/{user_id}`
>- Method: `POST`


```bash
curl  -X POST \
  'http://127.0.0.1:4242/api/upload/picture/user/<user_id>' \
  --form 'image=@<path_to_file>'
```

### get user picture

Replace `{user_id}`

>- Endpoint: `/api/picture/user/{user_id}`
>- Method: `GET`

```bash
curl  -X GET \
  --JO \
  'http://127.0.0.1:4242/api/picture/user/{user_id}'
```
> flag: `-JO` is to get original filename