# -*- coding: utf-8 -*-


def delete_method_docstring(klass, method_name):
    # Delete the docstring from the class method.
    # Objects must have a docstring to be published.
    # So this avoids them getting published.
    method = getattr(klass, method_name, None)
    if (method is not None and hasattr(method, 'im_func') and
            hasattr(method.im_func, '__doc__')):
        del method.im_func.__doc__


element_methods = [
    'getDoc',
    'getName',
    'getTaggedValue',
    'getTaggedValueTags',
    'queryTaggedValue',
    'setTaggedValue',
]
interface_methods = [
    'changed',
    'dependents',
    'direct',
    'extends',
    'get',
    'getBases',
    'getDescriptionFor',
    'implementedBy',
    'interfaces',
    'isEqualOrExtendedBy',
    'isOrExtends',
    'names',
    'namesAndDescriptions',
    'providedBy',
    'queryDescriptionFor',
    'subscribe',
    'unsubscribe',
    'validateInvariants',
    'weakref',
]


# Has this patch been applied yet?
_patched = False


def apply_patches():
    global _patched
    if _patched:
        return
    _patched = True

    from zope.interface import Attribute
    from zope.interface import Interface
    from zope.interface.interface import Element
    from zope.interface.interface import Method

    for klass in [Element, Attribute, Interface, Method]:
        try:
            del klass.__doc__
        except:
            pass
        for method_name in element_methods:
            delete_method_docstring(klass, method_name)

    for method_name in interface_methods:
        delete_method_docstring(Interface, method_name)
