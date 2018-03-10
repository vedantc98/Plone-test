Dexterity
=========

    "Same, same, but different"

Dexterity is a system for building content types, both through-the-web and as filesystem code.
It is aimed at Plone, although this package should work with plain Zope + CMF systems.

Key use cases
-------------

Dexterity wants to make some things really easy. These are:

- Create a "real" content type entirely through-the-web without having to know programming.

- As a business user, create a schema using visual or through-the-web tools, and augment it with adapters, event handlers, and other Python code written on the filesystem by a Python programmer.

- Create content types in filesystem code quickly and easily, without losing the ability to customise any aspect of the type and its operation later if required.

- Support general "behaviours" that can be enabled on a custom type in a declarative fashion.
  Behaviours can be things like title-to-id naming, support for locking or versioning, or sets of standard metadata with associated UI elements.

- Easily package up and distribute content types defined through-the-web, on the filesystem, or using a combination of the two.

Philosophy
----------

Dexterity is designed with a specific philosophy in mind.
This can be summarised as follows:

Reuse over reinvention
   As far as possible, Dexterity should reuse components and technologies that already exist.
   More importantly, however, Dexterity should reuse *concepts* that exist elsewhere.
   It should be easy to learn Dexterity by analogy, and to work with Dexterity types using familiar APIs and techniques.

Small over big
   Mega-frameworks be damned.
   Dexterity consists of a number of specialised packages, each of which is independently tested and reusable.
   Furthermore, packages should have as few dependencies as possible, and should declare their dependencies explicitly.
   This helps keep the design clean and the code manageable.

Natural interaction over excessive generality
   The Dexterity design was driven by several use cases (see docs/Design.txt) that express the way in which we want people to work with Dexterity.
   The end goal is to make it easy to get started, but also easy to progress from an initial prototype to a complex set of types and associated behaviours through step-wise learning and natural interaction patterns.
   Dexterity aims to consider its users - be they business analysts, light integrators, or Python developers, and be they new or experienced - and cater to them explicitly with obvious, well-documented, natural interaction patterns.

Real code over generated code
   Generated code is difficult to understand and difficult to debug when it  doesn't work as expected.
   There is rarely, if ever, any reason to scribble methods or 'exec' strings of Python code.

ZCA over old Zope 2
   As many components as possible should work with plain ZCA (Zope Component Architecture, ``zope.*`` packages with origins in Zope 3).
   Although Dexterity does not pretend to work with non-CMF systems,
   Even where there are dependencies on Zope 2, CMF or Plone, they should - as far as is practical - follow ZCA techniques and best practices.
   Many operations (e.g. managing objects in a folder, creating new objects or manipulating objects through a defined schema) are better designed in
   ZCA than they were in Zope 2.

Zope concepts over new paradigms
   We want Dexterity to be "Zope-ish" (and really, "ZCA-ish").
   Zope is a mature, well-designed (well, mostly) and battle tested platform.
   We do not want to invent brand new paradigms and techniques if we can help it.

Automated testing over wishful thinking
   "Everything" should be covered by automated tests.
   Dexterity necessarily has a lot of moving parts.
   Untested moving parts tend to come lose and fall on people's heads.
   Nobody likes that.

What's it all about?
--------------------

With the waffle out of the way, let's look in a bit more detail about what
makes up a "content type" in the Dexterity system.

The model
   The Dexterity "model" describes a type's schemata and metadata associated with those schemata.
   A schema is just a series of fields that can be used to render add/edit forms and introspect an object of the given type.
   The metadata storage is extensible via the component architecture.
   Typical forms of metadata include UI hints such as specifying the type of widget to use when rendering a particular field, and per-field security settings.

   The model is described in also XML.
   Though at runtime it is an instance of an object providing the IModel interface from ``plone.supermodel``.
   Schemata in the model are interfaces with ``zope.schema`` fields.

   The model can exist purely as data in the ZODB if a type is created through-the-web.
   Alternatively, it can be loaded from a file.
   The XML representation is intended to be human-readable and self-documenting.
   It is also designed with tools like `AGX  <http://agx.me>`_ in mind, that can generate models from a visual representation.

The schema
   All content types have at least one (unnamed) schema.
   A schema is simply an Interface with zope.schema fields.
   The schema can be specified in Python code (in which case it is simply referenced by name), or it can be loaded from an XML model.

   The unnamed schema is also known as the IContentType schema.
   In that, the schema interface will provide the zope IContentType interface.
   This means that if you call ``queryContentType()`` on a Dexterity content object, you should get back its unnamed schema, and that schema should be provided by the object that was queried.
   Thus, the object will directly support the attributes promised by the schema.
   This makes Dexterity content objects "Pythonic" and easy to work with.

The class
   Of course, all content objects are instances of a particular class.
   It is easy to provide your own class, and Dexterity has convenient base classes for you to use.
   However, many types will not need a class at all.
   Instead, they will use the standard Dexterity "Item" and "Container" classes.

   Dexterity's content factory will initialise an object of one of these classes with the fields in the type's content schema.
   The factory will ensure that objects provide the relevant interfaces, including the schema interface itself.

   The preferred way to add behaviour and logic to Dexterity content objects is via adapters.
   In this case, you will probably want a filesystem version of the schema interface (this can still be loaded from XML if you
   wish, but it will have an interface with a real module path) that you  can register components against.

The factory
   Dexterity content is constructed using a standard zope IFactory named utility.
   By convention the factory utility has the same name as the portal_type of the content type.

   When a Dexterity FTI (Factory Type Information, see below) is created, an appropriate factory will be registered as a local utility unless one    with that name already exists.

   The default factory is capable of initialising a generic ``Item`` or  ``Container`` object to exhibit a content type schema and have the security and other aspects specified in the type's model.
   You can use this if you wish, or provide your own factory.

Views
   Dexterity will by default create an:
   - add view (registered as a local utility, since it needs to take the portal_type of the content type into account when determining what fields to render) and an
   - edit view (registered as a generic, global view, which inspects the context's portal_type at runtime) for each type.
   - A default main view exists, which simply outputs the fields set on the context.

   To register new views, you will normally need a filesystem schema interface.
   You can then register views for this interface as you normally would.

   If you need to override the default add view, create a view for IAdding with a name corresponding to the portal_type of the content type.
   This will prevent Dexterity from registering a local view with the same name when the FTI is created.

The Factory Type Information (FTI)
   The FTI holds various information about the content type.
   Many operations performed by the Dexterity framework begin by looking up the type's FTI to find out some information about the type.

   The FTI is an object stored in portal_types in the ZMI.
   Most settings can be changed through the web.
   See the IDexterityFTI interface for more information.

   When a Dexterity FTI is created, an event handler will create a few local components, including the factory utility and add view for the new type. The FTI itself is also registered as a named utility, to make it easy to look up using syntax like::

       getUtility(IDexterityFTI, name=portal_type)

   The FTI is also fully importable and exportable using GenericSetup.
   Thus, the easiest way to create and distribute a content type is to create a new FTI, set some properties (including a valid XML model,
   which can be entered TTW if there is no file or schema interface to use), and export it as a GenericSetup extension profile.

Behaviors
   Behaviors are a way write make re-usable bits of functionality that can be toggled on or off on a per-type basis.
   Examples may include common metadata, or common functionality such as locking, tagging or ratings.

   Behaviors are implemented using the plone.behavior package.
   See its documentation for more details about how to write your own behaviors.

   In Dexterity, behaviors can "inject" fields into the standard add and edit forms, and may provide marker interfaces for newly created objects.
   See the example.dexterity package for an example of a behavior that provides form fields.

   In use, a behavior is essentially just an adapter that only appears to be registered if the behavior is enabled in the FTI of the object being adapted.
   Thus, if you have a behavior described by my.package.IMyBehavior, you'll typically interact with this behavior by doing::

       my_behavior = IMyBehavior(context, None)
       if my_behavior is not None:
           ...

   The enabled behaviors for a given type are kept in the FTI, as a list of dotted interface names.

The Dexterity Ecosystem
-----------------------

The Dexterity system comprises a number of packages, most of which are
independently re-usable. In addition, Dexterity uses many components from
Zope and CMF.

The most important packages are:

`plone.dexterity <https://pypi.python.org/pypi/plone.alterego>`_ (CMF)
   **this package** Defines the FTI and content classes.
   It provides basic views (with forms based on z3c.form), handles security and so on.
   It also provides components to orchestrate the various functionality provided by the packages above in order to bring the Dexterity system together.

`plone.behavior <https://pypi.python.org/pypi/plone.behavior>`_ (ZCA)
   Supports "conditional" adapters. A product author can write and register  a generic behaviour that works via a simple adapter.
   The adapter will appear to be registered for types that have the named behaviour available.

   Dexterity wires this up in such a way that the list of enabled behaviours is stored as a property in the FTI.
   This makes it easy to add/remove behaviours through the web, or using GenericSetup at install time.

`plone.folder <https://pypi.python.org/pypi/plone.folder>`_ (CMF)
   This is an implementation of an ordered, BTree-backed folder, with ZCA
   dictionary-style semantics for managing content items inside the folder.
   The standard Dexterity 'Container' type uses plone.folder as its base.

`plone.autoform <https://pypi.python.org/pypi/plone.autoform>`_ (CMF, z3cform)
   Contains helper functions to construct forms based on tagged values stored on schema interfaces.

`plone.supermodel <https://pypi.python.org/pypi/plone.supermodel>`_ (ZCA)
   Supports parsing and serialisation of interfaces from/to XML.
   The XML format is based directly on the interfaces that describe zope.schema type fields.
   Thus it is easily extensible to new field types.
   This has the added benefit that the interface documentation in the zope.schema package applies to the XML format as well.

   Supermodel is extensible via adapters and XML namespaces.
   plone.dexterity uses this to allow security and UI hints to be embedded as metadata in the XML model.

`plone.alterego <https://pypi.python.org/pypi/plone.alterego>`_ (Python)
   Support for dynamic modules that create objects on the fly.
   Dexterity uses this to generate "real" interfaces for types that exist only through-the-web.
   This allows these types to have a proper IContentType schema.
   It also allows local adapters to be registered for this interface (e.g. a custom view with a template defined through the web).

   Note that if a type uses a filesystem interface (whether written manually or loaded from an XML model), this module is not used.

`plone.app.dexterity <https://pypi.python.org/pypi/plone.app.dexterity>`_ (Plone)
   This package contains all Plone-specific aspects of Dexterity, including Ploneish UI components, behaviours and defaults.


Developer Manual
----------------

The `Dexterity Developer Manual <http://docs.plone.org/external/plone.app.dexterity/docs/index.html>`_ is a complete documentation with practical examples and part of the `Offical Plone Documentation <http://docs.plone.org/>`_.


Source Code
===========

Contributors please read the document `Process for Plone core's development <http://docs.plone.org/develop/plone-coredev/index.html>`_

Sources are at the `Plone code repository hosted at Github <https://github.com/plone/plone.dexterity>`_.

Changelog
=========


2.5.5 (2018-02-05)
------------------

Bug fixes:

- Prepare for Python 2 / 3 compatibility
  [pbauer]


2.5.4 (2017-11-24)
------------------

Bug fixes:

- Fix tests on Zope 4. [davisagli]


2.5.3 (2017-10-17)
------------------

Bug fixes:

- Give more context to the 'schema cannot be resolved' warning.  [gotcha]


2.5.2 (2017-06-03)
------------------

Bug fixes:

- Fix problem with new zope.interface not accepting None as value.
  [jensens]


2.5.1 (2017-02-27)
------------------

Bug fixes:

- Make sure that all fields are initialized to their default value
  when items are added via the add form. This is important in the case
  of fields with a defaultFactory that can change with time
  (such as defaulting to the current date).
  [davisagli]


2.5.0 (2017-02-12)
------------------

Breaking changes:

- When calling the DC metadata accessor for ``Description``, remove newlines from the output.
  This makes the removal of newlines from the description behavior setter in plone.app.dexterity obsolete.
  [thet]

Bug fixes:

- Relax tests for ZMI tabs for compatibility with Zope 4. [davisagli]


2.4.5 (2016-11-19)
------------------

New features:

- Removed test dependency on plone.mocktestcase [davisagli]


2.4.4 (2016-09-23)
------------------

Bug fixes:

- Fix error when copying DX containers with AT children which caused the
  children to not have the UID updated properly.  [jone]


2.4.3 (2016-08-12)
------------------

Bug fixes:

- Use zope.interface decorator.
  [gforcada]


2.4.2 (2016-05-12)
------------------

Fixes:

- Added security declarations from Products.PloneHotfix20160419.  [maurits]


2.4.1 (2016-02-27)
------------------

Incompatibilities:

- addCreator should not add if a creator is already set for content. This prevents every
  editor on content from adding to the list of creators for an object.
  [vangheem]


2.4.0 (2016-02-17)
------------------

New:

- Added Russian translation.  [serge73]

- Updated to and depended on pytz 2015.7 and DateTime 4.0.1.  [jensens]

Fixes:

- Skipped the tests
  ``test_portalTypeToSchemaName_looks_up_portal_for_prefix`` and
  ``test_getAdditionalSchemata`` with isolation problems in Zope 4.
  [pbauer]

- Made utils/datify work with newer DateTime and pytz.  Adjust tests
  to reflect changes.  [jensens]

- Fixed: duplicate aq_base without using Acquistion API resulted in an
  AttributeError that was masqued in the calling hasattr and resulted
  in wrong conclusion.  [jensens]

- Made modification test more stable.  [do3cc]


2.3.7 (2016-01-08)
------------------

Fixes:

- Sync schema when schema_policy name is changed (issue #44)
  [sgeulette]

- Corrected tests on date comparison (avoid 1h shift)
  [sgeulette]


2.3.6 (2015-10-28)
------------------

Fixes:

- No longer rely on deprecated ``bobobase_modification_time`` from
  ``Persistence.Persistent``.
  [thet]


2.3.5 (2015-09-20)
------------------

- Use registry lookup for types_use_view_action_in_listings
  [esteele]

- Don't check type constraints in AddForm.update() if request provides
  IDeferSecurityChecks.
  [alecm]


2.3.4 (2015-08-14)
------------------

- Avoid our own DeprecationWarning about portalTypeToSchemaName.
  [maurits]

- Set title on WebDAV upload
  [tomgross]

2.3.3 (2015-07-29)
------------------

- This version is still Plone 4.3.x compatible. Newer versions
  are only Plone 5 compatible.

- Check add_permission before checking constrains. Refs #37
  [jaroel]

- Remove obsolete css-class and text from statusmessages.
  [pbauer]

- Complete invalidate_cache.
  [adamcheasley]


2.3.2 (2015-07-18)
------------------

- Check allowed types for add form.
  [vangheem]


2.3.1 (2015-05-31)
------------------

- Fix issue where webdav PUT created items with empty id
  [datakurre]

- fix #27: createContent ignores empty fields
  [jensens]


2.3.0 (2015-03-13)
------------------

- Use attribute for DefaultAddForm and DefaultEditForm success message so it can
  be easily customized.
  [cedricmessiant]

- Big major overhaul to use everywhere the same way to fetch the main schema,
  behavior schemata and its markers. This was very scrmabled: sometimes
  behaviors weren't taken into account, or only FTI based behaviors but not
  those returned by the IBehaviorAssignable adapter. Also the caching was
  cleaned up. The tests are now better readable (at least I hope so).  In order
  to avoid circular imports some methods where moved fro ``utils.py`` to
  ``schema.py``.  Deprecations are in place.
  [jensens]

- Fix (security): Attribute access to schema fields can be protected. This
  worked for direct schemas, but was not implemented for permissions coming
  from behaviors.
  [jensens]

2.2.4 (2014-10-20)
------------------

- Fix the default attribute accessor to bind field to context when finding
  the field default.
  [datakurre]

- fix: when Dexterity container or its children contains any AT content with
  AT references in them, any move or rename operation for the parent
  Dexterity object will cause AT ReferenceEngine to remove those references.
  see #20.
  [datakurre]

- Let utils.createContent also handle setting of attributes on behaviors, which
  derive from other behaviors.
  [thet]

- overhaul (no logic changed):
  pep8, sorted imports plone.api style, readability, utf8header,
  remove bbb code (plone 3)
  [jensens]

2.2.3 (2014-04-15)
------------------

- Re-release 2.2.2 which was a brown bag release.
  [timo]

2.2.2 (2014-04-13)
------------------

- Add a 'success' class to the status message shown after successfully
  adding or editing an item.  The previous 'info' class is also
  retained for backwards-compatibility.
  [davisagli]

- If an object being added to a container already has an id, preserve it.
  [davisagli]

2.2.1 (2014-02-14)
------------------

- Also check behavior-fields for IPrimaryField since plone.app.contenttypes
  uses fields provided by behaviors as primary fields
  [pbauer]


2.2.0 (2014-01-31)
------------------

- utils.createContent honors behaviors.
  [toutpt]

- Date index method works even if source field is a dexterity field
  wich provides a  datetime python value.
  Now you can manually add a field with the name of a common Plone metadata field
  (as effective_date, publication_date, etc.)
  [tdesvenain]

- Replace deprecated test assert statements.
  [timo]

- Put a marker interface on the default edit view so viewlets
  can be registered for it.
  [davisagli]

- Ensure FTI's isConstructionAllowed method returns a boolean.
  [danjacka]

- Hide the Dublin Core tab and show the Properties tab for
  items when viewed in the ZMI.
  [davisagli]

- Avoid storing dublin core metadata on new instances unless it
  differs from the default values.
  [davisagli]

- Implement CMF's dublin core interfaces inline rather than
  depending on CMFDefault.
  [davisagli]

- Support GenericSetup structure import/export of Dexterity content.
  Content is serialized the same way as for WebDAV,
  using plone.rfc822. Not all field types are supported yet,
  but this at least gets the basics in place.

  GS import used to work by accident in a basic way for Dexterity
  containers. If you were using this, you'll need to recreate your
  exported files with the rfc822 serialization.
  [davisagli]

- Creator accessor should return encoded strings
  If your catalog was broken, try to clear & reindex Creator::

    cat.clearIndex('Creator')
    cat.manage_reindexIndex(['Creator'])

  [kiorky]

- Use the same message string for the default fieldset as Archetypes does.
  [davisagli]

2.1.3 (2013-05-26)
------------------

- Fail gracefully when a schema lookup fails due to schema that doesn't
  exist or no longer exists for some reason or another.
  [eleddy]


2.1.2 (2013-03-05)
------------------

- Merged Rafael Oliveira's (@rafaelbco) @content-core views from
  collective.cmfeditionsdexteritycompat.
  [rpatterson]

2.1.1 (2013-01-17)
------------------

* No longer add title and description fields to new FTIs by default.
  [davisagli, cedricmessiant]

* When pasting into a dexterity container check the FTI for the the pasted
  object to see if it is allowed in the new container.
  [wichert]

* Fixed schema caching. Previously, a non-persistent counter would be
  used as part of the cache key, and changes made to this counter in
  one process would obviously not propagate to other processes.

  Instead, the cache key now includes the schema and subtypes which
  are both retrieved from a FTI-specific volatile cache that uses the
  modification time as its cache key.
  [malthe]


2.1 (2013-01-01)
----------------

* Added Finnish translations.
  [pingviini]

* Overrride allowedContentTypes and invokeFactory from PortalFolder
  to mimic the behavior of Archetypes based folders. This allows the
  registration of IConstrainTypes adapters to actually have the
  expected effect.
  [gaudenzius]

* The default attribute accessor now also looks through subtypes
  (behaviors) to find a field default.
  [malthe]

* Added support in the FTI to look up behaviors by utility name when
  getting additional schemata (i.e. fields provided by behaviors).

  This functionality makes it possible to create a behavior where the
  interface is dynamically generated.
  [malthe]

* Return early for attributes that begin with two underscores.
  https://github.com/plone/plone.dexterity/pull/11
  [malthe]

* Make it possible to define a SchemaPolicy for the FTI
  [Frédéric Péters]
  [gbastien]

2.0 (2012-08-30)
----------------

* Add a UID method to Dexterity items for compatibility with the Archetypes
  API.
  [davisagli]

* Remove hard dependency on zope.app.content.
  [davisagli]

* Use standard Python properties instead of rwproperty.
  [davisagli]

* Removed support for Plone 3 / CMF 2.1 / Zope 2.10.
  [davisagli]

* Update package dependencies and imports as appropriate for Zope 2.12 & 2.13.
  [davisagli]

1.1.2 - 2012-02-20
------------------

* Fix UnicodeDecodeError when getting an FTI title or description with
  non-ASCII characters.
  [davisagli]

1.1.1 - 2012-02-20
------------------

* When deleting items from a container using manage_delObjects,
  check for the "DeleteObjects" permission on each item being
  deleted. This fixes
  http://code.google.com/p/dexterity/issues/detail?id=252
  [davisagli]

1.1 - 2011-11-26
----------------

* Added Italian translation.
  [zedr]

* Ensure that a factory utility really isn't needed before removing it.
  [lentinj]

* Work around issue where user got a 404 upon adding content if a content
  rule had moved the new item to a different folder. This closes
  http://code.google.com/p/dexterity/issues/detail?id=240
  [davisagli]

* Added events: IEditBegunEvent, IEditCancelledEvent, IEditFinished,
  IAddBegunEvent, IAddCancelledEvent
  [jbaumann]

* Make sure Dexterity content items get UIDs when they are created if
  ``plone.uuid`` is present. This closes
  http://code.google.com/p/dexterity/issues/detail?id=235
  [davisagli]

* Make sure the Title() and Description() accessors of containers return an
  encoded bytestring as expected for CMF-style accessors.
  [buchi]

* Added zh_TW translation.
  [marr, davisagli]

1.0.1 - 2011-09-24
------------------

* Support importing the ``add_view_expr`` property of the FTI via GenericSetup.
  This closes http://code.google.com/p/dexterity/issues/detail?id=192
  [davisagli]

* Make it possible to use DefaultAddForm without a form wrapper.
  [davisagli]

* Make sure the Subject accessor returns an encoded bytestring as expected for
  CMF-style accessors. This fixes
  http://code.google.com/p/dexterity/issues/detail?id=197
  [davisagli]

* Added pt_BR translation.
  [rafaelbco, davisagli]


1.0 - 2011-05-20
----------------

* Make sure the Title and Description accessors handle a value of None.
  [davisagli]

* Make sure the Title() accessor for Dexterity content returns an encoded
  bytestring as expected for CMF-style accessors.
  [davisagli]

1.0rc1 - 2011-04-30
-------------------

* Look up additional schemata by adapting to IBehaviorAssignable in cases
  where a Dexterity instance is available. (The list of behaviors in the
  FTI is still consulted for add forms.)
  [maurits]

* Explicitly load CMFCore ZCML.
  [davisagli]

* Add ids to group fieldsets.
  [elro]

* Do a deep copy instead of shallow when assigning field defaults. Content
  generated via script wound up with linked list (and other
  AbstractCollection) fields.
  [cah190, esteele]

* Make setDescription coerce to unicode in the same way as setTitle.
  [elro]

* Change the FTI default to enable dynamic view.
  [elro]

* Setup folder permissions in the same way as Archetypes so copy / paste /
  rename work consistently with the rest of Plone.
  [elro]

* Make sure the typesUseViewActionInListings property is respected when
  redirecting after edit.
  [elro, davisagli]

* Fix #145: UnicodeDecodeError After renaming item from @@folder_contents
  [toutpt]

1.0b7 - 2011-02-11
------------------

* Add adapter for plone.rfc822.interfaces.IPrimaryFieldInfo.
  [elro]

* Fixed deadlock in synchronized methods of schema cache by using
  threading.RLock instead of threading.Lock.
  [jbaumann]

* Add Spanish translation.
  [dukebody]

* Add French translation.
  [toutpt]


1.0b6 - 2010-08-30
------------------

* Send ObjectCreatedEvent event from createContent utility method.
  [wichert]

* Update content base classes to use allow keyword arguments to set
  initial values for instance variables.
  [wichert]

* Avoid empty <div class="field"> tag for title and description in
  item.pt.
  [gaudenzius]


1.0b5 - 2010-08-05
------------------

* Fix folder ordering bug.
  See: http://code.google.com/p/dexterity/issues/detail?id=113
  [optilude]

* Switch to the .Title() and .Description() methods of fti when used in
  a translatable context, to ensure that these strings are translated.
  [mj]

* Add Norwegian translation.
  [mj]


1.0b4 - 2010-07-22
------------------

* Improve robustness: catch and log import errors when trying to resolve
  behaviours.
  [wichert]

* Add German translation from Christian Stengel.
  [wichert]


1.0b3 - 2010-07-19
------------------

* Clarify license to GPL version 2 only.
  [wichert]

* Configure Babel plugins for i18n extraction and add a Dutch translation.
  [wichert]


1.0b2 - 2010-05-24
------------------

* Fix invalid license declaration in package metadata.
  [wichert]

* Do not assume "view" is the right immediate view - in some cases
  it might not exist. Instead use the absolute URL directly.
  [wichert]


1.0b1 - 2010-04-20
------------------

* Update the label for the default fieldset to something more humane.
  [wichert]

* Make the default add form extend BrowserPage to avoid warnings about
  security declarations for nonexistent methods.  This closes
  http://code.google.com/p/dexterity/issues/detail?id=69
  [davisagli]

* For now, no longer ensure that Dexterity content provides ILocation (in
  particular, that it has a __parent__ pointer), since that causes problems
  when exporting in Zope 2.10.
  [davisagli]

* Don't assume the cancel and actions buttons are always present in the
  default forms.
  [optilude]

1.0a3 - 2010-01-08
------------------

* require zope.filerepresentation>=3.6.0 for IRawReadFile
  [csenger]

1.0a2 - 2009-10-12
------------------

* Added support for zope.size.interfaces.ISized. An adapter to this interface
  may be used to specify the file size that is reported in WebDAV operations
  or used for Plone's folder listings. This requires that the sizeForSorting()
  method is implemented to return a tuple ('bytes', numBytes), where numBytes
  is the size in bytes.
  [optilude]

* Added support for WebDAV. This is primarily implemented by adapting content
  objects to the IRawReadFile and IRawWriteFile interfaces from the
  zope.filerepresentation package. The default is to use plone.rfc822 to
  construct an RFC(2)822 style message containing all fields. One or more
  fields may be marked with the IPrimaryField interface from that package,
  in which case they will be sent in the body of the message.

  In addition, the creation of new files (PUT requests to a null resource) is
  delegated to an IFileFactory adapter, whilst the creation of new directories
  (MKCOL requests) is delegated to an IDirectoryFactory adapter. See
  zope.filerepresentation for details, and filerepresentation.py for the
  default implementation.
  [optilude]

* Move AddViewActionCompat to the second base class of DexterityFTI, so that
  the FTI interfaces win over IAction. This fixes a problem with GenericSetup
  export: http://code.google.com/p/dexterity/issues/detail?id=79
  [optilude]

* Add getMapping() to AddViewActionCompat.
  Fixes http://code.google.com/p/dexterity/issues/detail?id=78
  [optilude]

1.0a1 - 2009-07-25
------------------

* Initial release


