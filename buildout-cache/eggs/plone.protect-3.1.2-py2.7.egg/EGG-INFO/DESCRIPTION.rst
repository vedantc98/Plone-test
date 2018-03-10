Introduction
============

This package contains utilities that can help protect parts of Plone
or applications build on top of the Plone framework.


1. Restricting to HTTP POST
===========================

a) Using decorator
------------------

If you only need to allow HTTP POST requests you can use the *PostOnly*
checker::

  from plone.protect import PostOnly
  from plone.protect import protect

  @protect(PostOnly)
  def manage_doSomething(self, param, REQUEST=None):
      pass

This checker operates only on HTTP requests; other types of requests
are not checked.

b) Passing request to a function validator
------------------------------------------

Simply::

    from plone.protect import PostOnly

    ...
    PostOnly(self.context.REQUEST)
    ...

2. Form authentication (CSRF)
=============================

A common problem in web applications is Cross Site Request Forgery or CSRF.
This is an attack method in which an attacker tricks a browser to do a HTTP
form submit to another site. To do this the attacker needs to know the exact
form parameters. Form authentication is a method to make it impossible for an
attacker to predict those parameters by adding an extra authenticator which
can be verified.

Generating the token
--------------------

To use the form authenticator you first need to insert it into your form.
This can be done using a simple TAL statement inside your form::

  <span tal:replace="structure context/@@authenticator/authenticator"/>

this will produce a HTML input element with the authentication information.

If you want to create the token value programmatically, use the following::

    from plone.protect.authenticator import createToken
    token = createToken()

Validating the token
--------------------

a) Zope Component Architecture way
**********************************

Next you need to add logic somewhere to verify the authenticator. This
can be done using a call to the authenticator view. For example::

   authenticator=getMultiAdapter((context, request), name=u"authenticator")
   if not authenticator.verify():
       raise Unauthorized

b) Using decorator
******************

You can do the same thing more conveniently using the ``protect`` decorator::

  from plone.protect import CheckAuthenticator
  from plone.protect import protect

  @protect(CheckAuthenticator)
  def manage_doSomething(self, param, REQUEST=None):
      pass

c) Passing request to a function validator
******************************************

Or just::

    from plone.protect import CheckAuthenticator

    ...
    CheckAuthenticator(self.context.REQUEST)
    ...

Headers
-------

You can also pass in the token by using the header ``X-CSRF-TOKEN``. This can be
useful for AJAX requests.


Protect decorator
=================

The most common way to use plone.protect is through the ``protect``
decorator. This decorator takes a list of *checkers* as parameters: each
checker will check a specific security aspect of the request. For example::

  from plone.protect import protect
  from plone.protect import PostOnly

  @protect(PostOnly)
  def SensitiveMethod(self, REQUEST=None):
      # This is only allowed with HTTP POST requests.

This **relies** on the protected method having a parameter called **REQUEST (case sensitive)**.

Customized Form Authentication
------------------------------

If you'd like use a different authentication token for different forms,
you can provide an extra string to use with the token::

  <tal:authenticator tal:define="authenticator context/@@authenticator">
    <span tal:replace="structure python: authenticator.authenticator('a-form-related-value')"/>
  </tal:authenticator>

To verify::

  authenticator=getMultiAdapter((context, request), name=u"authenticator")
  if not authenticator.verify('a-form-related-value'):
      raise Unauthorized

With the decorator::

  from plone.protect import CustomCheckAuthenticator
  from plone.protect import protect

  @protect(CustomCheckAuthenticator('a-form-related-value'))
  def manage_doSomething(self, param, REQUEST=None):
      pass


Automatic CSRF Protection
=========================

Since version 3, plone.protect provides automatic CSRF protection. It does
this by automatically including the auth token to all internal forms when
the user requesting the page is logged in.

Additionally, whenever a particular request attempts to write to the ZODB,
it'll check for the existence of a correct auth token.


Allowing write on read programmatically
---------------------------------------

When you need to allow a known write on read, you've got several options.

Adding a CSRF token to your links
**********************************

If you've got a GET request that causes a known write on read, your first
option should be to simply add a CSRF token to the URLs that result in that
request. ``plone.protect`` provides the ``addTokenToUrl`` function for this
purpose::

    from plone.protect.utils import addTokenToUrl

    url = addTokenToUrl(url)


If you just want to allow an object to be writable on a request...
******************************************************************

You can use the ``safeWrite`` helper function::

    from plone.protect.auto import safeWrite

    safeWrite(myobj, request)


Marking the entire request as safe
**********************************

Just add the ``IDisableCSRFProtection`` interface to the current request
object::

    from plone.protect.interfaces import IDisableCSRFProtection
    from zope.interface import alsoProvides

    alsoProvides(request, IDisableCSRFProtection)

Warning! When you do this, the current request is susceptible to CSRF
exploits so do any required CSRF protection manually.


Clickjacking Protection
=======================

plone.protect also provides, by default, clickjacking protection since
version 3.0.

To protect against this attack, Plone uses the X-Frame-Options
header. plone.protect will set the X-Frame-Options value to ``SAMEORIGIN``.

To customize this value, you can set it to a custom value for a custom view
(e.g. ``self.request.response.setHeader('X-Frame-Options', 'ALLOWALL')``),
override it at your proxy server, or you can set the environment variable of
``PLONE_X_FRAME_OPTIONS`` to whatever value you'd like plone.protect to set
this to globally.

You can opt out of this by making the environment variable empty.


Disable All Automatic CSRF Protection
=====================================

To disable all automatic CSRF protection, set the environment variable
``PLONE_CSRF_DISABLED`` value to ``true``.

WARNING! It is very dangerous to do this. Do not do this unless the ZEO client
with this setting is not public and you know what you are doing.

..note::
    This doesn't disable explicit and manual CSRF protection checks.


Fixing CSRF Protection failures in tests
========================================

If you get ``Unauthorized`` errors in tests due to unprotected form submission
where normally automatic protection would be in place you can use the following
blueprint to protect your forms::

    from plone.protect.authenticator import createToken
    from ..testing import MY_INTEGRATION_TESTING_LAYER
    import unittest

    class MyTest(unittest.TestCase):

        layer = MY_INTEGRATION_TESTING_LAYER

        def setUp(self):
            self.request = self.layer['request']
            # Disable plone.protect for these tests
            self.request.form['_authenticator'] = createToken()
            # Eventuelly you find this also useful
            self.request.environ['REQUEST_METHOD'] = 'POST'


Notes
=====

This package monkey patches a number of modules in order to better handle CSRF
protection::

  - Archetypes add forms, add csrf
  - Zope2 object locking support
  - pluggable auth csrf protection

If you are using a proxy cache in front of your site, be aware that
you will need to clear the entry for ``++resource++protect.js`` every
time you update this package or you will find issues with modals while
editing content.


Compatibility
=============

``plone.protect`` version 3 was made for Plone 5.  You can use it on
Plone 4 for better protection, but you will need the
``plone4.csrffixes`` hotfix package as well to avoid getting
needless warnings or errors.  See the `hotfix announcement`_ and the
`hotfix page`_.

.. _`hotfix announcement`: https://plone.org/products/plone/security/advisories/security-vulnerability-20151006-csrf
.. _`hotfix page`: https://plone.org/products/plone-hotfix/releases/20151006

Changelog
=========

3.1.2 (2018-02-02)
------------------

Bug fixes:

- Transform does not log a warning for empty responses
  (Fixes https://github.com/plone/plone.protect/issues/15)
  [fRiSi]

- Add Python 2 / 3 compatibility
  [vincero]


3.1.1 (2017-08-27)
------------------

Bug fixes:

- README wording tweaks
  [tkimnguyen]


3.1 (2017-08-14)
----------------

New features:

- Log forbidden URLs.
  Fixes https://github.com/plone/plone.protect/issues/66
  [gforcada]


3.0.26 (2017-08-04)
-------------------

New features:

- Catch ``AttributeError`` on transform.
  [hvelarde]


3.0.25 (2017-07-18)
-------------------

Bug fixes:

- Fix logging to no longer write traceback to stdout, but include it in the
  logging message instead.
  [jone]


3.0.24 (2017-07-03)
-------------------

Bug fixes:

- Remove unittest2 dependency
  [kakshay21]


3.0.23 (2016-11-26)
-------------------

Bug fixes:

- Allow ``confirm-action`` for all contexts, instead of only Plone Site root.
  This avoids an error when calling it on a subsite.
  Fixes `issue #51 <https://github.com/plone/plone.protect/issues/51>`_.
  [maurits]

- Code Style: utf8-headers, import sorting, new style namespace declaration, autopep8
  [jensens]

- Fix #57: Html must contain "body", otherwise plone.protect breaks.
  [jensens]


3.0.22 (2016-11-17)
-------------------

Bug fixes:

- avoid zope.globalrequest.getRequest()
  [tschorr]


3.0.21 (2016-10-05)
-------------------

Bug fixes:

- Avoid regenerating image scale over and over in Plone 4.
  Avoid (unnoticed) error when refreshing lock in Plone 4,
  plus a few other cases that were handled by plone4.csrffixes.
  Fixes https://github.com/plone/plone.protect/issues/47
  [maurits]


3.0.20 (2016-09-08)
-------------------

Bug fixes:

- Only try the confirm view for urls that are in the portal.
  This applies PloneHotfix20160830.  [maurits]

- Removed ``RedirectTo`` patch.  The patch has been merged to
  ``Products.CMFFormController`` 3.0.7 (Plone 4.3 and 5.0) and 3.1.2
  (Plone 5.1).  Note that we are not requiring those versions in our
  ``setup.py``, because the code in this package no longer needs it.
  [maurits]


3.0.19 (2016-08-19)
-------------------

New:

- Added protect.js from plone4.csrffixes.  This adds an ``X-CSRF-TOKEN``
  header to ajax requests.
  Fixes https://github.com/plone/plone.protect/issues/42
  [maurits]

Fixes:

- Use zope.interface decorator.
  [gforcada]


3.0.18 (2016-02-25)
-------------------

Fixes:

- Fixed AttributeError when calling ``safeWrite`` on a
  ``TestRequest``, because this has no ``environ.``.  [maurits]


3.0.17 (2015-12-07)
-------------------

Fixes:

- Internationalized button in confirm.pt.
  [vincentfretin]


3.0.16 (2015-11-05)
-------------------

Fixes:

- Make sure transforms don't fail on redirects.
  [lgraf]


3.0.15 (2015-10-30)
-------------------

- make sure to always compare content type with a string when checking
  if we should show the confirm-action view.
  [vangheem]

- Internationalized confirm.pt
  [vincentfretin]

- Disable editable border for @@confirm-action view.
  [lgraf]

- Make title and description show up on @@confirm-action view.
  [lgraf]

- Allow views to override 'X-Frame-Options' by setting the response header
  manually.
  [alecm]

- Avoid parsing redirect responses (this avoids a warning on the log files).
  [gforcada]

3.0.14 (2015-10-08)
-------------------

- Handle TypeError caused by getToolByName on an
  invalid context
  [vangheem]

- You can opt out of clickjacking protection by setting the
  environment variable ``PLONE_X_FRAME_OPTIONS`` to an empty string.
  [maurits]

- Be more flexible in parsing the ``PLONE_CSRF_DISABLED`` environment
  variable.  We are no longer case sensitive, and we accept ``true``,
  ``t``, ``yes``, ``y``, ``1`` as true values.
  [maurits]

- Avoid TypeError when checking the content-type header.
  [maurits]


3.0.13 (2015-10-07)
-------------------

- Always force html serializer as the XHTML variant seems
  to cause character encoding issues
  [vangheem]

3.0.12 (2015-10-06)
-------------------

- Do not check writes to temporary storage like session storage
  [davisagli]

3.0.11 (2015-10-06)
-------------------

- play nicer with inline JavaScript
  [vangheem]


3.0.10 (2015-10-06)
-------------------

- make imports backward compatible
  [vangheem]


3.0.9 (2015-09-27)
------------------

- patch pluggable auth with marmoset patch because
  the patch would not apply otherwise depending on
  somewhat-random import order
  [vangheem]

- get auto-csrf protection working on the zope root
  [vangheem]


3.0.8 (2015-09-20)
------------------

- conditionally patch Products.PluggableAuthService if needed
  [vangheem]

- Do not raise ComponentLookupError on transform
  [vangheem]


3.0.7 (2015-07-24)
------------------

- Fix pluggable auth CSRF warnings on zope root. Very difficult to reproduce.
  Just let plone.protect do it's job also on zope root.
  [vangheem]


3.0.6 (2015-07-20)
------------------

- Just return if the request object is not valid.
  [vangheem]


3.0.5 (2015-07-20)
------------------

- fix pluggable auth CSRF warnings
  [vangheem]

- fix detecting safe object writes on non-GET requests
  [vangheem]

- instead of using _v_safe_write users should now use the safeWrite function
  in plone.protect.auto
  [vangheem]


3.0.4 (2015-05-13)
------------------

- patch locking functions to use _v_safe_write attribute
  [vangheem]

- Be able to use _v_safe_write attribute to specify objects are safe to write
  [vangheem]


3.0.3 (2015-03-30)
------------------

- handle zope root not having IKeyManager Utility and CRSF protection
  not being supported on zope root requests yet
  [vangheem]

3.0.2 (2015-03-13)
------------------

- Add ITransform.transformBytes for protect transform to fix compatibility
  with plone.app.blocks' ESI-rendering
  [atsoukka]


3.0.1 (2014-11-01)
------------------

- auto CSRF protection: check for changes on all the storages
  [mamico]

- CSRF test fixed
  [mamico]


3.0.0 (2014-04-13)
------------------

- auto-rotate keyrings
  [vangheem]

- use specific keyring for protected forms
  [vangheem]

- add automatic clickjacking protection(thanks to Manish Bhattacharya)
  [vangheem]

- add automatic CSRF protection
  [vangheem]


2.0.2 (2012-12-09)
------------------

- Use constant time comparison to verify the authenticator. This is part of the
  fix for https://plone.org/products/plone/security/advisories/20121106/23
  [davisagli]

- Add MANIFEST.in.
  [WouterVH]

- Add ability to customize the token created.
  [vangheem]


2.0 - 2010-07-18
----------------

- Update license to BSD following board decision.
  http://lists.plone.org/pipermail/membership/2009-August/001038.html
  [elro]

2.0a1 - 2009-11-14
------------------

- Removed deprecated AuthenticateForm class and zope.deprecation dependency.
  [hannosch]

- Avoid deprecation warning for the sha module in Python 2.6.
  [hannosch]

- Specify package dependencies
  [hannosch]

1.1 - 2008-06-02
----------------

- Add an optional GenericSetup profile to make it easier to install
  plone.protect.
  [mj]

1.0 - 2008-04-19
----------------

- The protect decorator had a serious design flaw which broke it. Added
  proper tests for it and fixed the problems.
  [wichert]

1.0rc1 - 2008-03-28
-------------------

- Rename plone.app.protect to plone.protect: there is nothing Plone-specific
  about the functionality in this package and it really should be used outside
  of Plone as well.
  [wichert]

- Made utils.protect work with Zope >= 2.11.
  [stefan]

1.0b1 - March 7, 2008
---------------------

- Refactor the code to offer a generic protect decorator for methods
  which takes a list of checkers as options. Add checkers for both the
  authenticator verification and HTTP POST-only.
  [wichert]

1.0a1 - January 27, 2008
------------------------

- Initial release
  [wichert]


