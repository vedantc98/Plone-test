zope.browser
============

.. image:: https://travis-ci.org/zopefoundation/zope.browser.png?branch=master
        :target: https://travis-ci.org/zopefoundation/zope.browser

This package provides shared browser components for the Zope Toolkit.


.. contents::

IView
-----

Views adapt both a context and a request.

There is not much we can test except that ``IView`` is importable
and an interface:

  >>> from zope.interface import Interface
  >>> from zope.browser.interfaces import IView
  >>> Interface.providedBy(IView)
  True

IBrowserView
-------------

Browser views are views specialized for requests from a browser (e.g.,
as distinct from WebDAV, FTP, XML-RPC, etc.).

There is not much we can test except that ``IBrowserView`` is importable
and an interface derived from ``IView``:

  >>> from zope.interface import Interface
  >>> from zope.browser.interfaces import IBrowserView
  >>> Interface.providedBy(IBrowserView)
  True
  >>> IBrowserView.extends(IView)
  True

IAdding
-------

Adding views manage how newly-created items get added to containers.

There is not much we can test except that ``IAdding`` is importable
and an interface derived from ``IBrowserView``:

  >>> from zope.interface import Interface
  >>> from zope.browser.interfaces import IAdding
  >>> Interface.providedBy(IBrowserView)
  True
  >>> IAdding.extends(IBrowserView)
  True

ITerms
------

The ``ITerms`` interface is used as a base for ``ISource`` widget
implementations.  This interfaces get used by ``zope.app.form`` and was
initially defined in ``zope.app.form.browser.interfaces``, which made it
impossible to use for other packages like ``z3c.form`` wihtout depending on
``zope.app.form``.

Moving such base components / interfaces to ``zope.browser`` makes it
possible to share them without undesirable dependencies.

There is not much we can test except that ITerms is importable
and an interface:

  >>> from zope.interface import Interface
  >>> from zope.browser.interfaces import ITerms
  >>> Interface.providedBy(ITerms)
  True

ISystemErrorView
----------------

Views providing this interface can classify their contexts as system
errors. These errors can be handled in a special way (e. g. more
detailed logging).

There is not much we can test except that ISystemErrorView is importable
and an interface:

  >>> from zope.interface import Interface
  >>> from zope.browser.interfaces import ISystemErrorView
  >>> Interface.providedBy(ISystemErrorView)
  True


Changelog
=========

2.1.0 (2014-12-26)
------------------

- Add support for Python 3.4.

- Add support for testing on Travis.

2.0.2 (2013-03-08)
------------------

- Add Trove classifiers indicating CPython, 3.2 and PyPy support.

2.0.1 (2013-02-11)
------------------

- Add support for testing with tox.

2.0.0 (2013-02-11)
------------------

- Test coverage of 100% verified.

- Add support for Python 3.3 and PyPy.

- Drop support for Python 2.4 and 2.5.

1.3 (2010-04-30)
----------------

- Remove ``test`` extra and ``zope.testing`` dependency.

1.2 (2009-05-18)
----------------

- Move ``ISystemErrorView`` interface here from
  ``zope.app.exception`` to break undesirable dependencies.

- Fix home page and author's e-mail address.

- Add doctests to ``long_description``.

1.1 (2009-05-13)
----------------

- Move ``IAdding`` interface here from ``zope.app.container.interfaces``
  to break undesirable dependencies.

1.0 (2009-05-13)
----------------

- Move ``IView`` and ``IBrowserView`` interfaces here from
  ``zope.publisher.interfaces`` to break undesirable dependencies.

0.5.0 (2008-12-11)
------------------

- Move ``ITerms`` interface here from ``zope.app.form.browser.interfaces``
  to break undesirable dependencies.


