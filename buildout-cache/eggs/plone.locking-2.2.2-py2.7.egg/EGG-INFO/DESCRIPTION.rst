Overview
========

Provides basic automatic locking support for Plone. Locks are stealable by
default, meaning that a user with edit privileges will be able to steal
another user's lock, but will be warned that someone else may be editing
the same object. Used by Plone, Archetypes and plone.app.iterate

Compatibility
-------------

The versions 2.1.x (built from the master-branch) are used in Plone 5 and are not compatible with earlier Plone versions.

Versions 2.0.x are used by Plone 4.x (but *may* also be compatible with earlier versions).

Versions 1.x are used by Plone 3.

Changelog
=========

2.2.2 (2018-02-05)
------------------

Bug fixes:

- Update tests to not use plone.app.testing.bbb code.
  This should avoid test isolation problems.
  [gforcada]


2.2.1 (2018-02-02)
------------------

Bug fixes:

- Add Python 2 / 3 compatibility
  [pbauer]


2.2 (2017-06-08)
----------------

New features:

- All LockingOperations method can optionally redirect to the context view
  [ale-rt]

Bug fixes:

- Test fix: Use print in doctest (Python 3/ Zope 4 compat)
  [MatthewWilkes]


2.1.3 (2016-09-09)
------------------

New features:

- Update README.rst with Compatibility
  [djowett]


2.1.2 (2016-08-15)
------------------

Fixes:

- Use zope.interface decorator.
  [gforcada]


2.1.1 (2015-10-27)
------------------

New:

- Use registry lookup for types_use_view_action_in_listings
  [esteele]

- Locks stored on annotations are a safe write on read.
  [gforcada]


2.1.0 (2015-09-07)
------------------

- Pull lock_on_ttw_edit setting from the configuration registry
  [esteele]


2.0.8 (2015-07-20)
------------------

- Fix write on read CSRF issues with latest plone.protect
  [vangheem]


2.0.7 (2015-06-05)
------------------

- Fix possible package problem with Python 2.6 and old setuptools (at
  least 0.6c11) not finding the ``README.txt``.
  [maurits]


2.0.6 (2015-06-05)
------------------

- Pep8.
  [vangheem]


2.0.5 (2014-10-20)
------------------

- Adding "create_lock" to "plone_lock_operations"
  [hman]

- The locking timeout is now modifiable through LockType definition
  [parruc]

- Ported to plone.app.testing
  [tomgross]


2.0.4 (2012-10-20)
------------------

- Do not download the file when we click on "unlock" in the context of a file.
  Refs https://dev.plone.org/ticket/13191
  [thomasdesvenain]


2.0.3 (2012-01-04)
------------------

- Check if context is not joined to zodb connection for transaction where lock
  is added.
  [fafhrd91]

2.0.2 (2011-11-29)
------------------

- Do not cleanup stale lock if database is in read-only mode.
  http://dev.plone.org/ticket/12239
  [fafhrd91]


2.0.1 - 2011-05-12
------------------

- Make plone.locking check for the global lock settings if a context-specific
  adapter is not found. Fixes http://dev.plone.org/plone/ticket/11779
  [ggozad]

- Add MANIFEST.in.
  [WouterVH]


2.0 - 2010-07-18
----------------

- Define all package dependencies.
  [hannosch]

- Update license to GPL version 2 only.
  [hannosch]


1.2.1 - 2010-07-01
------------------

- Load the ``cmf.*`` permissions from Products.CMFCore.
  [hannosch]


1.2.0 - 2009-03-04
------------------

- Added IRefreshableLockable interface and TTWLockable implementation.
  [davisagli]

- Changed default lock timeout to 10 minutes.
  [davisagli]


1.1.0
-----

- Clarified license and copyright statements.
  [hannosch]

- Declare test dependencies in an extra. Avoid dependency on Plone.
  [hannosch]

- Specify package dependencies.
  [hannosch]

- Fix missing internationalization (#8609 thanks to Vincent Fretin)
  [encolpe]


1.0.5 - 2008-01-03
------------------

- Fix lock timeout which was set by default to 12 minutes, it is
  now set to maxtimeout (71582788 minutes).
  Fixes http://dev.plone.org/plone/ticket/7358
  [jfroche]

- Fix TypeError when an anonymous user locks content.  Fixes
  http://dev.plone.org/plone/ticket/7246
  [maurits]


1.0 - 2007-08-17
----------------

- Initial release.


