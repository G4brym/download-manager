from inspect import signature, Signature

from common import provider


class DependencyWrapper(object):
    def __init__(self, func):
        self._func = func

        # This just makes things clear in the swagger interface
        self.__class__.__name__ = self._func.__name__

    @property
    def __annotations__(self):
        return dict()  # This solves Typer injections

    @property
    def __name__(self):
        return self._func.__name__

    @property
    def __signature__(self):
        # Get Signature to modify
        sig = signature(self._func)

        # Copy params
        params = sig._parameters.copy()

        # This list holds the parameters that can be provided
        to_remove = []

        # Iter all params
        for key, value in params.items():
            _instance = provider.get_instance(value.annotation)
            if _instance:
                to_remove.append(key)

        # Remove params that will be provided
        for key in to_remove:
            del params[key]

        # Build altered Signature
        return Signature(
            parameters=params.values(), return_annotation=sig.return_annotation
        )

    def __call__(self, *args, **kwargs):
        return provider.inject(self._func)(*args, **kwargs)
