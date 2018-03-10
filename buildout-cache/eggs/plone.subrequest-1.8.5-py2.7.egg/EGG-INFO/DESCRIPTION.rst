Overview
========

plone.subrequest provides a mechanism for issuing subrequests under Zope2.

Installation
============

Plone 4
-------

An entry point is provided so no special installation is required past adding
`plone.subrequest` to your instance's `eggs`.

Zope 2.12 without Plone
-----------------------

Load this package's ZCML in the usual manner.

Zope 2.10
---------

You must install ZPublisherEventsBackport_ to use this package with Zope 2.10
and load both package's ZCML. The tests require Zope 2.12 / Python 2.6 so will
not run.

.. _ZPublisherEventsBackport: http://pypi.python.org/pypi/ZPublisherEventsBackport


Usage
=====

Basic usage
-----------

.. test-case: absolute

Call ``subrequest(url)``, it returns a response object.

    >>> from plone.subrequest import subrequest
    >>> response = subrequest('/folder1/@@url')
    >>> response.getBody()
    'http://nohost/folder1'

.. test-case: response-write

``response.getBody()`` also works for code that calls ``response.write(data)``.

    >>> response = subrequest('/@@response-write')
    >>> response.getBody()
    'Some data.\nSome more data.\n'

But in this case ``response.getBody()`` may only be called once.

    >>> response.getBody()
    Traceback (most recent call last):
        ...
    ValueError: I/O operation on closed file

Accessing the response body as a file
-------------------------------------

.. test-case: stdout

Some code may call ``response.write(data)``.

    >>> response = subrequest('/@@response-write')

In which case you may access response.stdout as file.

    >>> response.stdout.seek(0, 0)
    >>> list(response.stdout)
    ['Some data.\n', 'Some more data.\n']

You can test whether a file was returned using ``response._wrote``.

    >>> response._wrote
    1

When you're done, close the file:

    >>> response.stdout.close()

.. test-case: response-outputBody

Use ``response.outputBody()`` to ensure the body may be accessed as a file.

    >>> from plone.subrequest import subrequest
    >>> response = subrequest('/folder1/@@url')
    >>> response._wrote
    >>> response.outputBody()
    >>> response._wrote
    1
    >>> response.stdout.seek(0, 0)
    >>> list(response.stdout)
    ['http://nohost/folder1']

Relative paths
--------------

.. test-case: relative

Relative paths are resolved relative to the parent request's location:

    >>> request = traverse('/folder1/@@test')
    >>> response = subrequest('folder1A/@@url')
    >>> response.getBody()
    'http://nohost/folder1/folder1A'

.. test-case: relative-default-view

This takes account of default view's url.

    >>> request = traverse('/folder1')
    >>> request['URL'] == 'http://nohost/folder1/@@test'
    True
    >>> response = subrequest('folder1A/@@url')
    >>> response.getBody()
    'http://nohost/folder1/folder1A'

Virtual hosting
---------------

.. test-case: virtual-hosting

When virtual hosting is used, absolute paths are traversed from the virtual host root.

    >>> request = traverse('/VirtualHostBase/http/example.org:80/folder1/VirtualHostRoot/')
    >>> response = subrequest('/folder1A/@@url')
    >>> response.getBody()
    'http://example.org/folder1A'

Specifying the root
-------------------

.. test-case: specify-root

You may also set the root object explicitly

    >>> app = layer['app']
    >>> response = subrequest('/folder1A/@@url', root=app.folder1)
    >>> response.getBody()
    'http://nohost/folder1/folder1A'

Error responses
---------------

.. test-case: not-found

Subrequests may not be found.

    >>> response = subrequest('/not-found')
    >>> response.status
    404

.. test-case: error-response

Or might raise an error.

    >>> response = subrequest('/@@error')
    >>> response.status
    500

Or might raise an error rendered by a custom error view.

    >>> response = subrequest('/@@custom-error')
    >>> response.status
    500
    >>> response.body
    'Custom exception occurred: A custom error'

.. test-case: status-ok

So check for the expected status.

    >>> response = subrequest('/')
    >>> response.status == 200
    True

Handling subrequests
--------------------

The parent request is set as PARENT_REQUEST onto subrequests.

Subrequests also provide the ``plone.subrequest.interfaces.ISubRequest``
marker interface.


Changelog
=========

1.8.5 (2018-01-30)
------------------

Bug fixes:

- Add Python 2 / 3 compatibility
  [pbauer]


1.8.4 (2017-09-06)
------------------

New features:

- Add support for Zope exception views when explicit exception handler
  is not defined
  [datakurre]

Bug fixes:

- Fix issue where the example unauthorized_exception_handler did
  not properly set response status code
  [datakurre]


1.8.3 (2017-08-30)
------------------

Bug fixes:

- Reverted "Remove vurl-parts from path", which resulted in broken p.a.mosaic pages
  [thet]


1.8.2 (2017-07-20)
------------------

Bug fixes:

- Remove vurl-parts from path
  [awello]


1.8.1 (2017-06-28)
------------------

Bug fixes:

- Remove unittest2 dependency
  [kakshay21]


1.8 (2016-11-01)
----------------

New features:

- Provide an exception-handler for rewriting Unauthorized to 401's.
  [jensens]


1.7.0 (2016-05-04)
------------------

New:

- Allow to pass a custom exception handler for the response.
  [jensens]

Fixes:

- When a subrequest modified the DB (or prior to the subrequest the main request),
  the oids annotated to the requests were doubled with each subsequent subrequest.
  This resulted in out-of-memory errors when using lots of subrequests,
  such as it happens on Mosaic based sites with a certain amount of tiles.
  Fixed by only adding new oids, not already known by parent request.
  [jensens]

- Housekeeping: isort imports, autopep8, minor manual cleanup (no zope.app. imports).
  [jensens]


1.6.11 (2015-09-07)
-------------------

- propagate IDisableCSRFProtection interface on subrequest to parent request object
  [vangheem]


1.6.10 (2015-08-14)
-------------------

- propagate registered safe writes from plone.protect to parent request object.
  [vangheem]


1.6.9 (2015-03-21)
------------------

- Workaround for broken test because of missing dependency declaration in
  upstream package, see https://github.com/plone/plone.app.blob/issues/19
  for details.
  [jensens]

- Housekeeping and code cleanup (pep8, et al).
  [jensens]

- Fix issue where new cookies from the main request.response are not passed to
  subrequests.
  [datakurre]

- normalise request path_info so that string indexing works properly.
  [gweiss]


1.6.8 (2014-03-04)
------------------
- Handle sub-requests which contain a doubled // in the path.
  [gweis]

1.6.7 (2012-10-22)
------------------

- Ensure correct handling of bare virtual hosting urls.
  [elro]

1.6.6 (2012-06-29)
------------------

- Log errors that occur handling a subrequest to help debug plone.app.theming
  errors including content from a different url
  [anthonygerrard]

1.6.5 (2012-04-15)
------------------

- Ensure parent url is a string and not unicode.
  [davisagli]

1.6.4 - 2012-03-22
------------------

- Fix problems with double encoding some unicode charse by not copying too
  many ``other`` variables.
  [elro]

1.6.3 - 2012-02-12
------------------

- Copy ``other`` request variables such as ``LANGUAGE`` to subrequest.
  [elro]

1.6.2 - 2011-07-04
------------------

- Handle spaces in default documents. http://dev.plone.org/plone/ticket/12278

1.6.1 - 2011-07-04
------------------

- Move tests to package directory to making testing possible when installed
  normally.

1.6 - 2011-06-06
----------------

- Ensure url is a string and not unicode.
  [elro]

1.6b2 - 2011-05-20
------------------

- Set PARENT_REQUEST and add ISubRequest interface to subrequests.
  [elro]

1.6b1 - 2011-02-11
------------------

- Handle IStreamIterator.
  [elro]

- Simplify API so ``response.getBody()`` always works.
  [elro]

1.5 - 2010-11-26
----------------

- Merge cookies from subrequest response into parent response.
  [awello]

1.4 - 2010-11-10
----------------

- First processInput, then traverse (fixes #11254)
  [awello]

1.3 - 2010-08-24
----------------

- Fixed bug with virtual hosting and quoted paths.
  [elro]

1.2 - 2010-08-16
----------------

- Restore zope.component site after subrequest.
  [elro]

1.1 - 2010-08-14
----------------

- Virtual hosting, relative url and error response support.
  [elro]

1.0 - 2010-07-28
----------------

- Initial release.
  [elro]


