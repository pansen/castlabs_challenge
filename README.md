# [Castlabs Programming Task](https://github.com/castlabs/python_programming_task)

## Abstract

This repository tries to cover [the challenge](https://github.com/castlabs/python_programming_task)
as good as possible. Since this is a coding challenge, there are some limitations, some of them are 
marked as `TODO` in the code and maybe even mentioned below. 

## Usage

This repository is intented to be used locally for execution or development. 

### Local Execution 

#### Prerequisites

- You need to have UNIX compatible OS
- You need Docker installed
- You need `docker-compose` installed
- You should have `jq` installed
   
#### Go

To just run the current version, use 

```bash
docker-compose up --build
```

##### Test

###### Proxy HTTP GET

In an other terminal, you can call 

```bash
http_proxy=127.0.0.1:8000 curl 'httpbin.org/get?a=1'
```
or

###### Proxy HTTP POST

```bash
http_proxy=127.0.0.1:8000 curl -X POST 'httpbin.org/post?a=1'
```

to see the thing in action.

###### Proxy Status

To see the status of the instance, call

```bash
curl -s localhost:8000/status | jq .
```

### Local Development

#### Prerequisites

- You need to have UNIX compatible OS
- You need to have `make` and *Python3.8* installed
- Probably you also need a C compiler toolchain (not sure about the dependencies)
- It is assumed you have a Python IDE installed, particulary *PyCharm*
- After checkout, run `make bootstrap dev.build` *before* opening the project in PyCharm. 
  This ensures to let PyCharm find the `venv` and its containing local Python interpreter.
- After opening the project in PyCharm, ensure the projects test-runner is configured to use 
  `pytest`
  
  ![PyCharm Testrunner Configuration](doc/img/PyCharm_Testrunner.jpg)

#### Go

To build your development environment, use

```bash
make dev.build
```

To run all tests, use

```bash
make test
```

Once you followed the prerequisites section, you will also be able to run and debug single tests 
from PyCharm. 

