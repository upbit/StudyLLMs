## [`use_2to3` is invalid](https://stackoverflow.com/questions/72414481/error-in-anyjson-setup-command-use-2to3-is-invalid)

错误提示：`error in demjson setup command: use_2to3 is invalid.`

```python
pip install -U "setuptools<58.0.0" wheel

pip install demjson
```

## [fatal error: mpi.h: No such file or directory](https://stackoverflow.com/questions/26920083/fatal-error-mpi-h-no-such-file-or-directory-include-mpi-h)

错误提示：`fatal error: mpi.h: No such file or directory #include <mpi.h>`

```python
apt-get remove mpich  
MPICC=openmpicc pip install --upgrade mpi4py
apt-get install openmpi-bin openmpi-common libopenmpi-dev

pip install mpi4py
```

### from cmake import cmake: ModuleNotFoundError

错误出现在 samplerate 安装中
```
Building wheel for samplerate (pyproject.toml) ... error
  error: subprocess-exited-with-error
  
  × Building wheel for samplerate (pyproject.toml) did not run successfully.
  │ exit code: 1
  ╰─> [61 lines of output]
      running bdist_wheel
      running build
      running build_ext
      Traceback (most recent call last):
        File "/usr/local/bin/cmake", line 5, in <module>
          from cmake import cmake
      ModuleNotFoundError: No module named 'cmake'


```
问题在于 /usr/local/bin/cmake 版本太老，先删除这个文件。接着安装cmake
`pip install scikit-build "cmake==3.11.4"`

再安装 `pip install "samplerate>=0.2.1"` 即可

## (MacOS) No module named 'datrie'

错误提示: `_build_env/bin/llvm-ar' failed: No such file or directory`

```python
AR=/usr/bin/ar pip install datrie
```

## fitz

```python
pip install PyMuPDF
```
## PIL

```python
pip install pillow
```

## cv2

```python
pip install opencv-python
```