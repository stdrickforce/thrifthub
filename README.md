# thrifthub
Thrift version control through gitlab repo.

## usage

```python
# set gitlab token api.
thub token <your access token>

# push thrift file to gitlab.
thub push -t master -n user service.thrift

# pull thrift file from gitlab.
thub pull user:master >> service.thrift
```
