Introduction
============

``plone.resource`` publishes directories of static files via the ZPublisher.
These directories may be located either in the ZODB (as OFS folders and files), or on the filesystem.

Each resource directory has a type and a name. When combined, these are used to traverse to the resource directory.
For example::

    /++theme++mytheme/<subpath>
    /++sitelayout++mylayout/<subpath>
    /++templatelayout++mylayout<subpath>


Where resources can be stored
-----------------------------

Resource directory contents can be found by the traverser in several different places.
The following locations are tried in order.

Files in the ZODB
^^^^^^^^^^^^^^^^^

Installing ``plone.resource`` creates a Zope-folder called ``portal_resources``.
It can be used to store resource directories persistently.
By convention:

- the top-level folders under this folder correspond to resource types,
- the second-level folders correspond to the resource directory name.

So, the file traversable at ``/++theme++mytheme/myfile`` could be physically located at ``some_site/++etc++site/resources/theme/mytheme``

.. TODO (XXX: provide a helper to upload a tarball/zip)


Files in Python distributions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A folder in a Python distribution (e.g. egg) can be registered as a resource directory of a particular type and name using the ``plone:static`` ZCML directive.
For example, this registers a directory named "theme" as a resource directory of type "theme" under the name "mytheme".
It would be accessible at ``++theme++mytheme``::

    <plone:static
        directory="theme"
        type="theme"
        name="mytheme"
    />

  .. note::
     You must do ``<include package="plone.resource" file="meta.zcml"/>``
     before you can use the plone:static directive.

The name of the resource directory defaults to the name of the package, so can be omitted.
E.g. the following directive in a package named "mytheme" would result in the same registration as above::

    <plone:static
        directory="resources"
        type="theme"
    />

Traversing upward in directory paths using ``..`` is not supported for security reasons, as it could allow unwanted file access.

Minimum zcml config example
^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    <configure xmlns:plone="http://namespaces.plone.org/plone">
      <include package="plone.resource" file="meta.zcml"/>
      <plone:static
          directory="resources"
          type="theme"
          name="myproject"
        />
    </configure>

    ..

Files in a central resource directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the ``plone:static`` directive is used from ``site.zcml`` (i.e., with no active package in the ZCML import context),
then it may specify the absolute path to a top-level resources directory.

This directory should have the same sub-directory structure as explained above (in-ZODB resources directory):

- the top-level folders under this folder correspond to resource types,
- the second-level folders correspond to the resource directory name.

In addition, in order for resources to be available, the top-level directories *require a traverser* to be registered!

For example, the following in ``site.zcml`` registers the given path within the buildout root::

    <plone:static
        directory="/path/to/buildout/resources"
    />

In order to automate this at buildout time, `plone.recipe.zope2instance`_  recipe has the option ``resources``.
It injects the above zcml snippet with into ``site.zcml`` by specifying the option like this::

      [instance]
      ...
      resources = ${buildout:directory}/resources
      ...

Example:
Using ``plone.app.theming`` - which provides the ``++theme++`` traverser - given an image file located in filesystem at::

    ${buildout:directory}/resources/theme/my.project/logo.png``

This would be traversable at a URL like so::

    http://localhost:8080/Plone/++theme++my.project/logo.png

.. _`plone.recipe.zope2instance`: http://pypi.python.org/pypi/plone.recipe.zope2instance

Additional traversers
---------------------

Custom traversers can be registered via ZCML using an adapter like so::

    <adapter
        name="demo"
        for="* zope.publisher.interfaces.IRequest"
        provides="zope.traversing.interfaces.ITraversable"
        factory="my.project.traversal.MyTraverser"
    />

with a corresponding simple factory definition of::

    from plone.resource.traversal import ResourceTraverser
    class MyTraverser(ResourceTraverser):
        name = 'demo'

This, when coupled with configuration like that in the `Files in a central resource directory`_ section above, would mean that resources located at::

    ${buildout:directory}/resources/demo/my.project/logo.png

would be traversable at a URL like so::

    http://localhost:8080/Plone/++demo++my.project/logo.png

.. TODO: What types of resources can be stored


Changelog
=========

2.0.1 (2018-02-05)
------------------

New features:

- Add python 2 / 3 compatibility


2.0.0 (2018-01-17)
------------------

Breaking changes:

- Remove Python2.6 support.
  [ale-rt]

Bug fixes:

- Fixed 'ValueError: substring not found' in ``FilesystemResourceDirectory`` representation.
  This happens when you register a directory with a name that differs from the directory name.
  Visiting the ``/++theme++myname`` url would then give this error.
  We also avoid listing a longer part of the path in case the directory name happens to be in the path multiple times.
  [maurits]


1.2.1 (2016-12-30)
------------------

Bug fixes:

- 'unittest2' is a test dependency, make this explicit in setup.py.
  [jensens]


1.2 (2016-11-09)
----------------

New features:

- Fire events on resources creation/modification
  [jpgimenez, ebrehault]


1.1 (2016-10-04)
----------------

New features:

- Use ``mimetypes_registry`` utility to dertermine mimetype if available.
  [jensens]

Bug fixes:

- Remove duplicte import
  [jensens]

- Add coding headers on python files.
  [gforcada]

1.0.7 (2016-09-08)
------------------

Bug fixes:

- Applied 20160830 security hotfix.  [maurits]


1.0.6 (2016-08-10)
------------------

Fixes:

- Do not leave an ``.svn`` file behind when running the tests.  [maurits]

- Use zope.interface decorator.
  [gforcada]


1.0.5 (2016-02-26)
------------------

Fixes:

- Test fix: ``clearZCML`` was removed from ``zope.component.tests``.
  [thet]

- Cleanup: PEP8, plone-coding conventions, ReST fixes, documentation
  overhaul, et al.
  [jensens]


1.0.4 (2015-03-21)
------------------

- use utf-8 encoding when writing more than just text/html
  [vangheem]

- provides a proper __contains__ method in FilesystemResourceDirectory
  [ebrehault]


1.0.3 (2014-10-13)
------------------

- security hardening: we don't want the anonymous user to look at our fs
  [giacomos]


1.0.2 (2013-01-01)
------------------

- Nothing changed yet.


1.0.1 (2012-05-25)
------------------

- Make sure text/html files imported as persistent files will be
  served with a utf-8 encoding. This fixes
  https://dev.plone.org/ticket/12838
  [davisagli]

1.0 (2012-04-15)
----------------

- Add __setitem__() support for writeable resource directories.
  [optilude]

1.0b6 (2011-11-24)
------------------

- Added rename() method for writable resource directories
  [optilude]

- Added cloneResourceDirectory() helper method in the utils module
  [optilude]

- Add a ++unique++ resource traverser for resource directories to cache as
  'plone.stableResource'.
  [elro]

1.0b5 (2011-06-08)
------------------

- Ensure any files are skipped in iterDirectoriesOfType.
  [elro]

1.0b4 (2011-05-29)
------------------

- Add queryResourceDirectory() helper method.
  [optilude]

1.0b3 (2011-05-23)
------------------

- Fix resource directory download bug with subdirectories.
  [elro]

1.0b2 (2011-05-16)
------------------

- Add a more compatible filestream iterator for filesystem files that allows
  coercion to string or unicode. This fixes possible compatibility issues
  with resource merging through Resource Registries.
  [optilude]

1.0b1 (2011-04-22)
------------------

- Initial release


