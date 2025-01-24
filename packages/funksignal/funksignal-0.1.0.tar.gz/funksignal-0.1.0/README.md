## funksignal &middot; [![GitHub license](https://img.shields.io/badge/License-GPL--3.0-blue)](https://github.com/facebook/react/blob/main/LICENSE)
**funksignal** is a synchronous signaling library for event-driven programming. Bind methods to signals which will be executed once the signal is emitted.

## How to Install
To install **funksignal**, open a terminal and use the `pip` package manager:
```bash
   pip install funksignal
```

## Instructions
To use **funksignal** effectively, bind one or more methods to a signal identified by a unique key. When the signal is emitted, all methods bound to that signal will be executed. If you no longer need the binding, you can simply unbind it.
```Python
from funksignal import Signal

def example():
    print("Hello World")

Signal.bind("signal-key", example)
Signal.emit("signal-key")
Signal.unbind("signal-key", example)
```
funksignal provides an interface to pass arguments – from within `bind()`, `emit()` or `simultaniously` via `*args` and `**kwargs`.
```Python
from funksignal import Signal

def example(a, b):
    print(f"{a} {b}")

Signal.bind("1a", example)
Signal.emit("1a", "Hello", "World")

Signal.bind("1b", example, "Hello", "World")
Signal.emit("1b")

Signal.bind("2a", example)
Signal.emit("2a", a="Hello", b="World")

Signal.bind("2b", example, a="Hello", b="World")
Signal.emit("2b")

Signal.bind("2c", example, a="Hello")
Signal.emit("2c", b="World")
```

## Documentation
Auto-generated documentation using [pydoc-markdown](https://pypi.org/project/pydoc-markdown/).
#### bind

```python
@classmethod
def bind(cls, key: Union[str, int], callable: callable, *args: any, **kwargs: any) -> None
```

Binds a callable to a signal. The callable will be executed when the signal is emitted.

<a id="signal.Signal.unbind"></a>

#### unbind

```python
@classmethod
def unbind(cls, key: Union[str, int], callable: callable) -> None
```

Unbinds a callable from a signal. After unbinding, the callable will no longer be executed when the signal is emitted.

<a id="signal.Signal.emit"></a>

#### emit

```python
@classmethod
def emit(cls, key: Union[str, int], *args: any, **kwargs: any) -> None
```

Emits a signal identified by the given key. This triggers the execution of all callables that are bound to the signal. You can pass arguments to the bound methods via `*args` and `**kwargs`.