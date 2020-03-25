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


#### references

- form data:
  - https://fastapi.tiangolo.com/tutorial/request-forms/
- requests:
  - https://www.starlette.io/requests/
  - https://fastapi.tiangolo.com/advanced/using-request-directly/
