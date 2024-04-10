## [`use_2to3` is invalid](https://stackoverflow.com/questions/72414481/error-in-anyjson-setup-command-use-2to3-is-invalid)

错误提示：`error in demjson setup command: use_2to3 is invalid.`

```python
pip install "setuptools<58.0.0"
```

## [fatal error: mpi.h: No such file or directory](https://stackoverflow.com/questions/26920083/fatal-error-mpi-h-no-such-file-or-directory-include-mpi-h)

错误提示：`fatal error: mpi.h: No such file or directory #include <mpi.h>`

```python
apt-get remove mpich  
MPICC=openmpicc pip install --upgrade mpi4py
apt-get install openmpi-bin openmpi-common libopenmpi-dev
```




