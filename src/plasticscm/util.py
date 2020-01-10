# Copyright (c) 2019-2020 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/zlib

import inspect
import enum

from public import public


@public
def inherit_docs(cls: type) -> type:
    """Copies all the missing docstrings of derived attributes
    (methods, properties, attrs) from the parent classes.

    Args:
         cls: class to fix up.

    Returns:
        The fixed class.
    """
    # if_print = cls.__name__.endswith("ObjectType")
    # if if_print: print("@@@", cls, cls.__mro__[1:])
    to_inherit = {cls.__name__: cls}
    to_inherit.update({name: attr for name, attr in vars(cls).items()
                       if not name.startswith("_") and attr.__doc__ is None})
    for name, attr in to_inherit.items():
        if isinstance(attr, type) and issubclass(attr, enum.Enum):
            parent_doc = next((parent.__doc__ for parent in attr.__mro__[1:]
                               if parent.__doc__ is not None), None)
        else:
            parent_doc = inspect.getdoc(attr)
        # if if_print: print("   ", name, attr, parent_doc)
        if parent_doc is None:
            continue
        if isinstance(attr, property):
            # copy property, since its doc attribute is read-only
            prop = property(attr.fget, attr.fset, attr.fdel, doc=parent_doc)
            setattr(cls, name, prop)
        else:
            try:
                attr.__doc__ = parent_doc
            except: # some __doc__'s are not writable
                pass
        """
        if isinstance(attr, types.FunctionType):
            for parent in cls.__bases__:
                parfunc = getattr(parent, name, None)
                if parfunc and getattr(parfunc, '__doc__', None):
                    attr.__doc__ = parfunc.__doc__
                    break
        elif isinstance(attr, property) and not attr.fget.__doc__:
            for parent in cls.__bases__:
                parprop = getattr(parent, name, None)
                if parprop and getattr(parprop.fget, '__doc__', None):
                    newprop = property(fget=attr.fget,
                                       fset=attr.fset,
                                       fdel=attr.fdel,
                                       parprop.fget.__doc__)
                    setattr(cls, name, newprop)
                    break
        """
    return cls

"""
def inherit_docs(cls):
    for name in dir(cls):
        func = getattr(cls, name)
        if func.__doc__: 
            continue
        for parent in cls.mro()[1:]:
            if not hasattr(parent, name):
                continue
            doc = getattr(parent, name).__doc__
            if not doc: 
                continue
            try:
                # __doc__'s of properties are read-only.
                # The work-around below wraps the property into a new property.
                if isinstance(func, property):
                    # We don't want to introduce new properties, therefore check
                    # if cls owns it or search where it's coming from.
                    # With that approach (using dir(cls) instead of var(cls))
                    # we also handle the mix-in class case.
                    wrapped = property(func.fget, func.fset, func.fdel, doc)
                    clss = filter(lambda c: name in vars(c).keys() and not getattr(c, name).__doc__, cls.mro())
                    setattr(clss[0], name, wrapped)
                else:
                    try:
                        func = func.__func__ # for instancemethod's
                    except:
                        pass
                    func.__doc__ = doc
            except: # some __doc__'s are not writable
                pass
            break
    return cls
"""