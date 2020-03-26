# fastapi-twilio

### python code formartter

- [`black`](https://github.com/psf/black)
- [`flake8`](http://flake8.pycqa.org/en/latest/)
- 

#### virtualenv

```
# virtualenv
$ virtualenv -p python3 venv
$ source venv/bin/activate
```

#### install requirements

```
$ cd fastapi-twilio
$ pip install -r requirements.txt
```

#### run

```
$  uvicorn app:app --reload
```

#### add media

```
$ curl -X POST --data '{"tag":"cute cat","url":"https://images.unsplash.com/photo-1572097664187-7b183a6bda78?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=675&q=80"}' -H "Content-Type: application/json"  http://127.0.0.1:8000/add/media
```

#### references

- form data:
  - https://fastapi.tiangolo.com/tutorial/request-forms/
- requests:
  - https://www.starlette.io/requests/
  - https://fastapi.tiangolo.com/advanced/using-request-directly/
