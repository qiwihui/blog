# Python 函数变量类型注释会导致用 Cython 编译后执行与直接执行结果不一致

最近工作中遇到关于函数类型注释引起的错误，特此记录一下。

起因是公司的项目为了安全和执行速度，在发布时会使用 Cython 转为 C 语言并编译成动态连接库进行调用，但是有个函数在 Python 执行时正常，但是在动态连接库中却执行错误。

<!--more-->

## 错误复现

测试用例 `test.py`：

```python
def ip_str(ips: str):
    ips = [x for x in ips]

def ip(ips):
    ips = [x for x in ips]
```

编译 `compile.py`：

```python
from setuptools import setup
from Cython.Build import cythonize

extensions = ["test.py",]

setup(name='test',
      ext_modules=cythonize(extensions)
)
```

运行编译：

```bash
python compile.py build
```

编译之后进入对应 so 文件目录 `build/lib-{平台架构}`，运行对比：

```bash
>>> import test
>>> test.ip("123")
>>> test.ip_str("123")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "test.py", line 5, in test.ip_str
TypeError: Expected str, got list
```

经过调查发现，当函数变量做了类型注释时，不能重新赋值为其他类型，否则会在 Cython 编译后执行时报错。

Cython 可以在编译时推断出部分简单的错误，比如：

```python
def ip1():
    ips: str = '1'
    ips = ['1']
```

```bash
Error compiling Cython file:
------------------------------------------------------------
...

def ip1():
    ips: str = '1'
    ips = ['1']
         ^
------------------------------------------------------------

test.py:10:10: Cannot coerce list to type 'str object'
```

但如果代码比较复杂，则只能在运行时才会出错。所以上述错误只能在执行的时候才被抛出。

## 原因

Cython 将 Python 转为 C 代码比较后类型注释与否代码比较：

- 没有类型注释：

    ```c
    /* "test.py":2
     * 
     * def ip_str(ips: str):             # <<<<<<<<<<<<<<
     *     ips = [x for x in ips]
     * 
     */

    /* Python wrapper */
    static PyObject *__pyx_pw_4test_1ip_str(PyObject *__pyx_self, PyObject *__pyx_v_ips); /*proto*/
    static PyMethodDef __pyx_mdef_4test_1ip_str = {"ip_str", (PyCFunction)__pyx_pw_4test_1ip_str, METH_O, 0};
    static PyObject *__pyx_pw_4test_1ip_str(PyObject *__pyx_self, PyObject *__pyx_v_ips) {
      PyObject *__pyx_r = 0;
      __Pyx_RefNannyDeclarations
      __Pyx_RefNannySetupContext("ip_str (wrapper)", 0);
      if (unlikely(!__Pyx_ArgTypeTest(((PyObject *)__pyx_v_ips), (&PyString_Type), 1, "ips", 1))) __PYX_ERR(0, 2, __pyx_L1_error)
      __pyx_r = __pyx_pf_4test_ip_str(__pyx_self, ((PyObject*)__pyx_v_ips));

      /* function exit code */
      goto __pyx_L0;
      __pyx_L1_error:;
      __pyx_r = NULL;
      __pyx_L0:;
      __Pyx_RefNannyFinishContext();
      return __pyx_r;
    }

    static PyObject *__pyx_pf_4test_ip_str(CYTHON_UNUSED PyObject *__pyx_self, PyObject *__pyx_v_ips) {
      PyObject *__pyx_v_x = NULL;
      PyObject *__pyx_r = NULL;
      __Pyx_RefNannyDeclarations
      PyObject *__pyx_t_1 = NULL;
      PyObject *__pyx_t_2 = NULL;
      PyObject *(*__pyx_t_3)(PyObject *);
      PyObject *__pyx_t_4 = NULL;
      __Pyx_RefNannySetupContext("ip_str", 0);
      __Pyx_INCREF(__pyx_v_ips);

      /* "test.py":3
     * 
     * def ip_str(ips: str):
     *     ips = [x for x in ips]             # <<<<<<<<<<<<<<
     * 
     * def ip(ips):
     */
      __pyx_t_1 = PyList_New(0); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 3, __pyx_L1_error)
      __Pyx_GOTREF(__pyx_t_1);
      __pyx_t_2 = PyObject_GetIter(__pyx_v_ips); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 3, __pyx_L1_error)
      __Pyx_GOTREF(__pyx_t_2);
      __pyx_t_3 = Py_TYPE(__pyx_t_2)->tp_iternext; if (unlikely(!__pyx_t_3)) __PYX_ERR(0, 3, __pyx_L1_error)
      for (;;) {
        {
          __pyx_t_4 = __pyx_t_3(__pyx_t_2);
          if (unlikely(!__pyx_t_4)) {
            PyObject* exc_type = PyErr_Occurred();
            if (exc_type) {
              if (likely(__Pyx_PyErr_GivenExceptionMatches(exc_type, PyExc_StopIteration))) PyErr_Clear();
              else __PYX_ERR(0, 3, __pyx_L1_error)
            }
            break;
          }
          __Pyx_GOTREF(__pyx_t_4);
        }
        __Pyx_XDECREF_SET(__pyx_v_x, __pyx_t_4);
        __pyx_t_4 = 0;
        if (unlikely(__Pyx_ListComp_Append(__pyx_t_1, (PyObject*)__pyx_v_x))) __PYX_ERR(0, 3, __pyx_L1_error)
      }
      __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
      if (!(likely(PyString_CheckExact(__pyx_t_1))||(PyErr_Format(PyExc_TypeError, "Expected %.16s, got %.200s", "str", Py_TYPE(__pyx_t_1)->tp_name), 0))) __PYX_ERR(0, 3, __pyx_L1_error)
      __Pyx_DECREF_SET(__pyx_v_ips, ((PyObject*)__pyx_t_1));
      __pyx_t_1 = 0;
    ```

- 有类型注释：

    ```c
    /* "test.py":2
     * 
     * def ip_str(ips: str):             # <<<<<<<<<<<<<<
     *     ips = [x for x in ips]
     * 
     */

      /* function exit code */
      __pyx_r = Py_None; __Pyx_INCREF(Py_None);
      goto __pyx_L0;
      __pyx_L1_error:;
      __Pyx_XDECREF(__pyx_t_1);
      __Pyx_XDECREF(__pyx_t_2);
      __Pyx_XDECREF(__pyx_t_4);
      __Pyx_AddTraceback("test.ip_str", __pyx_clineno, __pyx_lineno, __pyx_filename);
      __pyx_r = NULL;
      __pyx_L0:;
      __Pyx_XDECREF(__pyx_v_x);
      __Pyx_XDECREF(__pyx_v_ips);
      __Pyx_XGIVEREF(__pyx_r);
      __Pyx_RefNannyFinishContext();
      return __pyx_r;
    }

    /* "test.py":5
     *     ips = [x for x in ips]
     * 
     * def ip(ips):             # <<<<<<<<<<<<<<
     *     ips = [x for x in ips]
     */

    /* Python wrapper */
    static PyObject *__pyx_pw_4test_3ip(PyObject *__pyx_self, PyObject *__pyx_v_ips); /*proto*/
    static PyMethodDef __pyx_mdef_4test_3ip = {"ip", (PyCFunction)__pyx_pw_4test_3ip, METH_O, 0};
    static PyObject *__pyx_pw_4test_3ip(PyObject *__pyx_self, PyObject *__pyx_v_ips) {
      PyObject *__pyx_r = 0;
      __Pyx_RefNannyDeclarations
      __Pyx_RefNannySetupContext("ip (wrapper)", 0);
      __pyx_r = __pyx_pf_4test_2ip(__pyx_self, ((PyObject *)__pyx_v_ips));

      /* function exit code */
      __Pyx_RefNannyFinishContext();
      return __pyx_r;
    }

    static PyObject *__pyx_pf_4test_2ip(CYTHON_UNUSED PyObject *__pyx_self, PyObject *__pyx_v_ips) {
      PyObject *__pyx_v_x = NULL;
      PyObject *__pyx_r = NULL;
      __Pyx_RefNannyDeclarations
      PyObject *__pyx_t_1 = NULL;
      PyObject *__pyx_t_2 = NULL;
      Py_ssize_t __pyx_t_3;
      PyObject *(*__pyx_t_4)(PyObject *);
      PyObject *__pyx_t_5 = NULL;
      __Pyx_RefNannySetupContext("ip", 0);
      __Pyx_INCREF(__pyx_v_ips);

      /* "test.py":6
     * 
     * def ip(ips):
     *     ips = [x for x in ips]             # <<<<<<<<<<<<<<
     */
      __pyx_t_1 = PyList_New(0); if (unlikely(!__pyx_t_1)) __PYX_ERR(0, 6, __pyx_L1_error)
      __Pyx_GOTREF(__pyx_t_1);
      if (likely(PyList_CheckExact(__pyx_v_ips)) || PyTuple_CheckExact(__pyx_v_ips)) {
        __pyx_t_2 = __pyx_v_ips; __Pyx_INCREF(__pyx_t_2); __pyx_t_3 = 0;
        __pyx_t_4 = NULL;
      } else {
        __pyx_t_3 = -1; __pyx_t_2 = PyObject_GetIter(__pyx_v_ips); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 6, __pyx_L1_error)
        __Pyx_GOTREF(__pyx_t_2);
        __pyx_t_4 = Py_TYPE(__pyx_t_2)->tp_iternext; if (unlikely(!__pyx_t_4)) __PYX_ERR(0, 6, __pyx_L1_error)
      }
      for (;;) {
        if (likely(!__pyx_t_4)) {
          if (likely(PyList_CheckExact(__pyx_t_2))) {
            if (__pyx_t_3 >= PyList_GET_SIZE(__pyx_t_2)) break;
            #if CYTHON_ASSUME_SAFE_MACROS && !CYTHON_AVOID_BORROWED_REFS
            __pyx_t_5 = PyList_GET_ITEM(__pyx_t_2, __pyx_t_3); __Pyx_INCREF(__pyx_t_5); __pyx_t_3++; if (unlikely(0 < 0)) __PYX_ERR(0, 6, __pyx_L1_error)
            #else
            __pyx_t_5 = PySequence_ITEM(__pyx_t_2, __pyx_t_3); __pyx_t_3++; if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 6, __pyx_L1_error)
            __Pyx_GOTREF(__pyx_t_5);
            #endif
          } else {
            if (__pyx_t_3 >= PyTuple_GET_SIZE(__pyx_t_2)) break;
            #if CYTHON_ASSUME_SAFE_MACROS && !CYTHON_AVOID_BORROWED_REFS
            __pyx_t_5 = PyTuple_GET_ITEM(__pyx_t_2, __pyx_t_3); __Pyx_INCREF(__pyx_t_5); __pyx_t_3++; if (unlikely(0 < 0)) __PYX_ERR(0, 6, __pyx_L1_error)
            #else
            __pyx_t_5 = PySequence_ITEM(__pyx_t_2, __pyx_t_3); __pyx_t_3++; if (unlikely(!__pyx_t_5)) __PYX_ERR(0, 6, __pyx_L1_error)
            __Pyx_GOTREF(__pyx_t_5);
            #endif
          }
        } else {
          __pyx_t_5 = __pyx_t_4(__pyx_t_2);
          if (unlikely(!__pyx_t_5)) {
            PyObject* exc_type = PyErr_Occurred();
            if (exc_type) {
              if (likely(__Pyx_PyErr_GivenExceptionMatches(exc_type, PyExc_StopIteration))) PyErr_Clear();
              else __PYX_ERR(0, 6, __pyx_L1_error)
            }
            break;
          }
          __Pyx_GOTREF(__pyx_t_5);
        }
        __Pyx_XDECREF_SET(__pyx_v_x, __pyx_t_5);
        __pyx_t_5 = 0;
        if (unlikely(__Pyx_ListComp_Append(__pyx_t_1, (PyObject*)__pyx_v_x))) __PYX_ERR(0, 6, __pyx_L1_error)
      }
      __Pyx_DECREF(__pyx_t_2); __pyx_t_2 = 0;
      __Pyx_DECREF_SET(__pyx_v_ips, __pyx_t_1);
      __pyx_t_1 = 0;
    ```

主要区别在于，类型注释增加了变量检测 `__Pyx_ArgTypeTest` ，以及之后赋值 ips 时的类型检测 `PyString_CheckExact`；没有变量类型注释则进行了变量推测，判断是否为List（ `PyList_CheckExact`）或者Tuple （ `PyTuple_CheckExact`），还是可迭代类型。

## 结论

1. 类型注释在编译后会简化处理流程；
2. 类型注释的变量不能赋值为其他类型。

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)

