from warnings import warn
from typing import Union
import inspect


class Function:

    def __init__(self, callable: callable, *args: any, **kwargs: any):
        self.callable = callable
        self.args = args
        self.kwargs = kwargs

    def call(self, *args: any, **kwargs: any):
        combined_kwargs = kwargs | self.kwargs
        if self.args:
            args = self.args
        if args:
            if combined_kwargs:
                return self.callable(*args, **combined_kwargs)
            return self.callable(*args)
        elif combined_kwargs:
            return self.callable(**combined_kwargs)
        else:
            self.callable()


class Signal:

    signals: dict[str, Function] = {}

    @classmethod
    def bind(cls, key: Union[str, int], callable: callable, *args: any, **kwargs: any) -> None:
        """Bind a callable that will be executed when the signal is emitted."""
        function = Function(callable, *args, **kwargs)
        if key in cls.signals:
            cls.__check_deviating_signature(key, cls.signals[key][0].callable, callable)
            cls.signals[key].append(function)
        else:
            cls.signals[key] = [function]

    @classmethod
    def unbind(cls, key: Union[str, int], callable: callable) -> None:
        """Unbind a callable from the signal."""
        if key in cls.signals:
            cls.signals[key] = [signal for signal in cls.signals[key] if signal.callable != callable]

    @classmethod
    def emit(cls, key: Union[str, int], *args: any, **kwargs: any) -> None:
        """Execute all callables bound to this signal."""
        if not key in cls.signals:
            return
        for function in cls.signals[key]:
            cls.__check_simultaneous_args_use(function.args, args)
            cls.__check_common_kwargs(function.kwargs, kwargs)
            function.call(*args, **kwargs)

    @classmethod
    def __check_simultaneous_args_use(cls, a, b):
        if a and b:
            raise ValueError(
                "Passing arguments as *args is only possible either in bind() or in emit(), but not in both simultaneously. Use **kwargs if you need this flexibility."
            )

    @classmethod
    def __check_common_kwargs(cls, a, b):
        common_keys = a.keys() & b.keys()
        if common_keys:
            raise ValueError(
                f"Passing arguments as **kwargs in bind() and emit() simultaneously is possible, however, the keys must be different (common keys found: {common_keys})."
            )

    @classmethod
    def __check_deviating_signature(cls, key: Union[str, int], a: callable, b: callable):
        if not len(inspect.signature(a).parameters) == len(inspect.signature(b).parameters):
            raise ValueError(
                f"Binding '{b.__name__}()' to signal '{key}' is not possible, as the method signature deviates from previously bound callables to signal '{key}'."
            )
