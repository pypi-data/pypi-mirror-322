"""
Mimic the `tqdm` progress bar interface, but don't actually display anything.
"""

__version__ = '0.1.0'

from typing import TypeAlias, Callable, Iterable
from contextlib import contextmanager

ProgressBarFactory: TypeAlias = Callable[..., Iterable]

class tquiet:
    """
    Mimic the `tqdm` progress bar interface, but don't actually display 
    anything.

    This class is meant to be a default argument for functions with long 
    running loops.  This allows the main function to remain in complete control 
    of terminal output.
    """

    def __init__(
            self,
            iterable=None,
            total=None,
            **kwargs,
    ):
        if total is None and iterable is not None:
            try:
                total = len(iterable)
            except (TypeError, AttributeError):
                total = None

        if total == float("inf"):
            total = None

        self.iterable = iterable
        self.total = total

    def __bool__(self):
        if self.total is not None:
            return self.total > 0
        if self.iterable is None:
            raise TypeError('bool() undefined when iterable == total == None')
        return bool(self.iterable)

    def __len__(self):
        return (
            self.total if self.iterable is None
            else self.iterable.shape[0] if hasattr(self.iterable, "shape")
            else len(self.iterable) if hasattr(self.iterable, "__len__")
            else self.iterable.__length_hint__() if hasattr(self.iterable, "__length_hint__")
            else getattr(self, "total", None)
        )

    def __reversed__(self):
        yield from reversed(self.iterable)

    def __contains__(self, item):
        return item in self.iterable

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __hash__(self):
        return id(self)

    def __iter__(self):
        yield from self.iterable

    def update(self, n=1):
        pass

    def close(self):
        pass

    def clear(self, nolock=False):
        pass

    def refresh(self, nolock=False, lock_args=None):
        pass

    def unpause(self):
        pass

    def reset(self, total=None):
        pass

    def set_description(self, desc=None, refresh=True):
        pass

    def set_description_str(self, desc=None, refresh=True):
        pass

    def set_postfix(self, ordered_dict=None, refresh=True, **kwargs):
        pass

    def set_postfix_str(self, s='', refresh=True):
        pass

    @property
    def format_dict(self):
        # This method probably should work, but I don't want to go to the 
        # effort to implement it right now.
        raise NotImplementedError

    def display(self, msg=None, pos=None):
        pass

    @classmethod
    @contextmanager
    def wrapattr(cls, stream, method, total=None, bytes=True, **tqdm_kwargs):
        # I'm not even really sure what this method does, but it seems like it 
        # might do something other than just render the progress bar.
        raise NotImplementedError
