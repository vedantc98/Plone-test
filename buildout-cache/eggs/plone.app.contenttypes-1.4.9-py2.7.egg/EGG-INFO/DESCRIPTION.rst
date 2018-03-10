.. contents::

.. image:: https://api.travis-ci.org/plone/plone.app.contenttypes.png?branch=master
    :target: http://travis-ci.org/plone/plone.app.contenttypes

.. image:: https://img.shields.io/pypi/dm/plone.app.contenttypes.svg
    :target: https://crate.io/packages/plone.app.contenttypes

.. image:: https://img.shields.io/pypi/v/plone.app.contenttypes.svg
    :target: https://crate.io/packages/plone.app.contenttypes

.. image:: https://img.shields.io/coveralls/plone/plone.app.contenttypes/master.svg
    :target: https://coveralls.io/github/plone/plone.app.contenttypes?branch=master


plone.app.contenttypes documentation
====================================


Introduction
------------

plone.app.contenttypes provides default content types for Plone based on Dexterity. It replaces ``Products.ATContentTypes`` and provides the default-types in Plone 5. It can be used as an add-on in Plone 4.x.

It contains the following types:

* Collection
* Document
* Event
* File
* Folder
* Image
* Link
* News Item

The main difference from a users perspective is that these types are editable and extendable through-the-web. This means you can add or remove fields and behaviors using the control-panel "Dexterity Content Types" (``/@@dexterity-types``).

**Warning: Using plone.app.contenttypes on a site with existing Archetypes-based content requires migrating the sites content. Please see the chapter "Migration".**


Compatibility
-------------

The versions 1.2.x (build from the master-branch) are used in Plone 5.

Version 1.1b5 and later are tested with Plone 4.3.x. The versions build from the branch 1.1.x will stay compatible with Plone 4.3.x.

For support of Plone 4.1 and 4.2 please use versions 1.0.x. Please note that they do not provide the full functionality.


Installation
------------

This package is included in Plone 5 and does not need installation.

To use plone.app.contenttypes in Plone 4.x add this line in the eggs section of your ``buildout.cfg``

.. code:: ini

    eggs =
        ...
        plone.app.contenttypes

If you have a Plone site with mixed Archetypes and Dexterity content use the extra requirement ``atrefs``.

.. code:: ini

    eggs =
        ...
        plone.app.contenttypes [atrefs]

This will also install the package `plone.app.referenceablebehavior <https://pypi.python.org/pypi/plone.app.referenceablebehavior>`_ that allows you to reference dexterity-based content from archetypes-based content. You will have to enable the behavior ``plone.app.referenceablebehavior.referenceable.IReferenceable`` for all types that need to be referenced by Archetypes-content.


What happens to existing content?
---------------------------------

If you install plone.app.contenttypes in a existing site all Archetypes-based content of the default types still exists and can be viewed but can't be edited. On installation plone.app.contenttypes removes the type-definitions for the old default-types like this:

.. code:: xml

    <object name="Document" remove="True" />

They are then replaced by new Definitions:

.. code:: xml

    <object meta_type="Dexterity FTI" name="Document" />

To make the existing content editable again you need to migrate it to Dexterity (please see the section on migration) or uninstall plone.app.contenttypes (see the section on uninstalling).

Archetypes-based content provided by add-ons (e.g. Products.PloneFormGen) will still work since only the default-types are replaced.

If you install plone.app.contenttypes on a fresh site (i.e. when no content has been edited or added) the usual default-content (Events, News, Members...) will be created as dexterity-content.


Uninstalling
------------

Uninstalling the default-types is not officially supported in Plone 5. If you really want to switch back to Archetypes-based types you have to to the following:

* Go to the ZMI
* In portal_types delete the default-types
* In portal_setup navigate to the tab 'import', select the profile 'Archetypes Content Types for Plone' and install all steps including dependencies.

Any content you created based on plone.app.contenttypes will no longer be editable until you reinstall plone.app.contenttypes.


Dependencies
------------

* ``plone.app.dexterity >= 2.0.7``. Dexterity is shipped with Plone 4.3.x. Version pins for Dexterity are included in Plone 4.2.x. For Plone 4.1.x you need to pin the right version for Dexterity in your buildout. See `Installing Dexterity on older versions of Plone <http://docs.plone.org/external/plone.app.dexterity/docs/install.html#installing-dexterity-on-older-versions-of-plone>`_.

* ``plone.dexterity >= 2.2.1``. Olders version of plone.dexterity break the rss-views because plone.app.contenttypes uses behaviors for the richtext-fields.

* ``plone.app.event >= 1.1.4``. This provides the behaviors used for the event-type.

* ``plone.app.portlets >= 2.5a1``. In older version the event-portlet will not work with the new event-type.

These are the version-pins for Plone 4.3.4:

.. code:: ini

    [buildout]
    versions = versions

    [versions]
    plone.app.event = 1.1.4

Plone 4.3.3 also needs ``plone.app.portlets = 2.5.2``

Plone-versions before 4.3.3 need to pin more packages:

.. code:: ini

    [buildout]
    versions = versions

    [versions]
    plone.dexterity = 2.2.1
    plone.app.dexterity = 2.0.11
    plone.schemaeditor = 1.3.5
    plone.app.event = 1.1b1
    plone.app.portlets = 2.5.1

For migrations to work you need at least ``Products.contentmigration = 2.1.9`` and ``plone.app.intid`` (part of Plone since Plone 4.1.0).


Migration
---------


Migrating the default-types
^^^^^^^^^^^^^^^^^^^^^^^^^^^

To migrate your existing content from Archetypes to Dexterity use the form at ``/@@atct_migrator``.


Migrating Archetypes-based default-types content to plone.app.contenttypes
``````````````````````````````````````````````````````````````````````````

`plone.app.contenttypes <https://pypi.python.org/pypi/plone.app.contenttypes/>`_ can migrate the following archetypes-based default types:

* Document
* Event
* File
* Folder
* Image
* Link
* News Item
* Collection
* Topic (old Collections)

The following non-default types will also be migrated:

* The AT-based Event-type provided by plone.app.event
* The DX-based Event-type provided by plone.app.event
* The Event-type provided by plone.app.contenttypes until version 1.0
* News Items with blobs (provided by https://github.com/plone/plone.app.blob/pull/2)
* Files and Images without blobs

The migration tries to keep most features (including portlets, comments, contentrules, local roles and local workflows).

**Warning:** Versions of content are not migrated. During migration you will lose all old revisions.


Migrating only certain types
````````````````````````````

There is also a view ``/@@pac_installer`` that allows you to install plone.app.contenttypes without replacing those archetypes-types with the dexterity-types of which there are existing objects in the site. Afterwards it redirects to the migration-form and only the types that you chose to migrate are installed. This allows you to keep certain types as archetypes while migrating others to dexterity (for example if you did heavy customizations of these types and do not have the time to reimplement these features in dexterity).


Migrating Topics
````````````````

Topics are migrated to Collections. However, the old type Topic had support for Subtopics, a feature that does not exit in Collections. Subtopics are nested Topics that inherited search terms from their parents. Since Collections are not folderish (i.e. they cannot contain content) Subtopics cannot be migrated unless Collections are made folderish (i.e. that they can contain content). Also the feature that search terms can be inherited from parents does not exist for Collections.

The migration-form will warn you if you have subtopics in your site and your Collections are not folderish. You then have several options:

1. You can delete all Subtopics before migrating and achieve their functionality in another way (e.g. using eea.facetednavigation).
2. You can choose to not migrate Topics by not selecting them. This will keep your old Topics functional. You can still add new Collections.
3. You can modify Collections to be folderish or create your own folderish content-type.   That type would need a base-class that inherits from ``plone.dexterity.content.Container`` instead of ``plone.dexterity.content.Item``:

   .. code-block:: python

      from plone.app.contenttypes.behaviors.collection import ICollection
      from plone.dexterity.content import Container
      from zope.interface import implementer

      @implementer(ICollection)
      class FolderishCollection(Container):
          pass

   You can either use a new Collection type or simply modify the default type to use this new base-class by overriding the klass-attribute of the default Collection. To override add a ``Collection.xml`` in your own package:

   .. code-block:: xml

      <?xml version="1.0"?>
      <object name="Collection" meta_type="Dexterity FTI">
       <property name="klass">my.package.content.FolderishCollection</property>
      </object>

   If you really need it you could add the functionality to inherit search terms to your own folderish Collections by extending the behavior like in the example at https://github.com/plone/plone.app.contenttypes/commit/366cc1a911c81954645ec6aabce925df4a297c63


Migrating content that is translated with LinguaPlone
`````````````````````````````````````````````````````

Since LinguaPlone does not support Dexterity you need to migrate from LinguaPlone to plone.app.multilingual (http://pypi.python.org/pypi/plone.app.multilingual). The migration from Products.LinguaPlone to plone.app.multilingual should happen **before** the migration from Archetypes to plone.app.contenttypes. For details on the migration see--
http://pypi.python.org/pypi/plone.app.multilingual#linguaplone-migration


Migrating default-content that was extended with archetypes.schemaextender
``````````````````````````````````````````````````````````````````````````


The migration-form warns you if any of your old types were extended with additional fields using `archetypes.schemaextender   <https://pypi.python.org/pypi/archetypes.schemaextender/>`_. The data contained in these fields will be lost during migration (with the exception of images added with collective.contentleadimage).

To keep the data you would need to write a custom migration for your types dexterity-behaviors for the functionality provided by the schemaextenders. This is an advanced development task and beyond the scope of this documentation.


Migrating images created with collective.contentleadimage
`````````````````````````````````````````````````````````

`collective.contentleadimage <https://pypi.python.org/pypi/collective.contentleadimage/>`_ was a popular addon that allows you to add images to any content in your site by extending the default types. To make sure these images are kept during migration you have to enable the behavior "Lead Image" on all those types where you want to migrate images added using collective.contentleadimage.

The old types that use leadimages are listed in the navigation-form with the comment *"extended fields: 'leadImage', 'leadImage_caption'"*. The migration-form informs you which new types have the behavior enabled and which do not. Depending on the way you installed plone.app.contenttypes you might have to first install these types by (re-)installing plone.app.contenttypes.


Migrating in code (e.g. in a upgrade-step)
``````````````````````````````````````````

You can run the migration in your own code by using the view `migrate_from_atct`. Here is an example of an upgrade-step that migrates all default content-types.

.. code-block:: python

    def migrate_to_pac(setup):
      portal = api.portal.get()
      request = getRequest()
      pac_migration = api.content.get_view('migrate_from_atct', portal, request)
      pac_migration(
          migrate=True,
          content_types='all',
          migrate_schemaextended_content=True,
          reindex_catalog=False)

With `content_types` you can also pass a list of types to be migrated. Make sure to use the key from the dictionary `plone.app.contenttypes.migration.vocabularies.ATCT_LIST` to identify the types.


Migrating custom content
^^^^^^^^^^^^^^^^^^^^^^^^

During migrations of the default types any custom content-types will not be migrated and will continue to work as expected.


Using the migration-form to migrate custom content
``````````````````````````````````````````````````

To help you migrating these types to Dexterity plone.app.contenttypes contains a migration form (``/@@custom_migration``) that allows you to migrate any (custom or default) Archetypes-type to any (custom or default) Dexterity-type. The only requirement is that the target-type (the Dexterity-type you want to migrate to) has to exist and that the class of the old type is still present. It makes no difference if the type you are migrating from is still registered in portal_types or is already removed or replaced by a dexterity-version using the same name.

In the form ``/@@custom_migration`` you can select a Dexterity-type for any Archetypes-types that exists in the portal. You can then map the source-types fields to the targets fields. You can also choose to ignore fields. You have to take care that the values can be migrated (since there is no validation for that), e.g. it would make no sense to migrate a ImageField to a TextField. There are build-in methods for most field-types, custom or rarely used fields might not migrate properly (you can create a issue if you miss a migration that is not yet supported).

After you map the fields you can test the configuration. During a test one item will be test-migrated and Plone checks if the migrated item will be accessible without throwing a errors. After the test any changes will be rolled back.

Migrating custom types in your own code
```````````````````````````````````````

It is recommended that you reuse the migration-code provided by plone.app.contenttypes in ``plone.app.contenttypes.migration.migration.migrateCustomAT`` for custom migrations.

To do this you have to simply pass a mapping of source- to target-fields to a migration-method for each type.

..  code-block:: python


    from plone.app.contenttypes.migration.migration import migrateCustomAT

    def my_custom_migration():
        fields_mapping = (
                {'AT_field_name': 'some_field',
                 'DX_field_name': 'description',
                 },

                # Migrate AT imagefield to DX imagefield using the mapping in
                # plone.app.contenttypes.migration.field_migrators.FIELDS_MAPPING
                {'AT_field_name': 'some_atimage',
                 'DX_field_name': 'some_dximage',
                 'DX_field_type': 'NamedBlobImage',
                 },
        )
        migrateCustomAT(
            fields_mapping,
            src_type='SomeATType',
            dst_type='SomeDXType')

A field-dict without a key ``DX_field_type`` from one of the migrators in ``plone.app.contenttypes.migration.field_migrators.FIELDS_MAPPING`` will always use ``plone.app.contenttypes.migration.field_migrators.migrate_simplefield`` as its migration-method. That can migrate most field-types where the value does not have to change (e.g. strings, lists, tuples, dicts etc.).

``plone.app.contenttypes.migration.field_migrators`` has special field migrators for the following field-types: ``RichText``, ``NamedBlobFile``, ``NamedBlobImage``, ``Datetime``, ``Date``. They transform values from the Archetypes-version of such fields to their Dexterity counterparts.


Custom field-migrators
``````````````````````

If you use rare or custom fields or want to apply special transforms to your data while migrating you can pass custom methods as ``field_migrator`` with the fields_mapping. This way you can migrate fields that are usually not migrateable.

Here is an example where this method is used to migrate a Richtext-Field into a Tuple-Field by passing the custom field-migrator ``some_field_migrator``. In such a custom migrator you can do just about anything you wish.


..  code-block:: python

    from plone.app.contenttypes.migration.migration import migrateCustomAT


    def some_field_migrator(src_obj, dst_obj, src_fieldname, dst_fieldname):
        """A simple example that transforms pipe-delimited richtext to a tuple.
        """
        field = src_obj.getField(src_fieldname)
        at_value = field.get(src_obj)
        at_value = at_value.replace('<p>', '').replace('</p>', '')
        dx_value = [safe_unicode(i) for i in at_value.split('|')]
        setattr(dst_obj, dst_fieldname, tuple(dx_value))


    def my_custom_migration():
        """
        """
        fields_mapping = (
                # Migrate using our custom migrator
                {'AT_field_name': 'some_richtext_field',
                 'DX_field_name': 'some_tuple_field',
                 'field_migrator': some_field_migrator},
        )
        migrateCustomAT(
            fields_mapping,
            src_type='SomeATType',
            dst_type='SomeDXType')

Alternatively you could also extends the mapping from ``plone.app.contenttypes.migration.field_migrators.FIELDS_MAPPING`` to add new or replace existing migrators for specific field-types.


Migrating from old versions of plone.app.contenttypes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before version 1.0a2 the content-items did not implement marker-interfaces. They will break in newer versions since the views are now registered for these interfaces (e.g. ``plone.app.contenttypes.interfaces.IDocument``). To fix this you can call the view ``/@@fix_base_classes`` on your site-root.

Since plone.app.contenttypes 1.1a1, the Collection type uses the new Collection behavior and the Event type utilizes behaviors from `plone.app.event <http://pypi.python.org/pypi/plone.app.event>`_. In order to upgrade:

1. First run the default profile (``plone.app.contenttypes:default``) or reinstall plone.app.contenttypes
2. Then run the upgrade steps.



Widgets
-------

When used in Plone 4.x plone.app.contenttypes uses the default z3c.form widgets. All widgets work as they used to with Archetypes except for the keywords-widget for which a simple linesfield is used. Replacing that with a nicer implementation is explained below.

It is also possible to use ``plone.app.widgets`` to switch to the widgets that are used in Plone 5.


How to override widgets
^^^^^^^^^^^^^^^^^^^^^^^^

To override the default keywords-widgets with a nicer widget you can use the package `collective.z3cform.widgets <https://pypi.python.org/pypi/collective.z3cform.widgets>`_.

Add ``collective.z3cform.widgets`` to your ``buildout`` and in your own package register the override in your ``configure.zcml``:

.. code:: xml

    <adapter factory=".subjects.SubjectsFieldWidget" />

Then add a file ``subjects.py``

.. code:: python

    # -*- coding: UTF-8 -*-
    from collective.z3cform.widgets.token_input_widget import TokenInputFieldWidget
    from plone.app.dexterity.behaviors.metadata import ICategorization
    from plone.app.z3cform.interfaces import IPloneFormLayer
    from z3c.form.interfaces import IFieldWidget
    from z3c.form.util import getSpecification
    from z3c.form.widget import FieldWidget
    from zope.component import adapter
    from zope.interface import implementer


    @adapter(getSpecification(ICategorization['subjects']), IPloneFormLayer)
    @implementer(IFieldWidget)
    def SubjectsFieldWidget(field, request):
        widget = FieldWidget(field, TokenInputFieldWidget(field, request))
        return widget

Once you install ``collective.z3cform.widgets`` in the quickinstaller, the new widget will then be used for all types.


Information for Addon-Developers
--------------------------------

Design decisions
^^^^^^^^^^^^^^^^

The schemata for the types File, Image and Link are defined in xml-files using ``plone.supermodel``. This allows the types to be editable trough the web. The types Document, News Item, Folder and Event have no schemata at all but only use behaviors to provide their fields.


Installation as a dependency from another product
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to add plone.app.contenttypes as a dependency from another products use the profile ``plone-content`` in your ``metadata.xml`` to have Plone populate a new site with DX-based default-content.

.. code:: xml

    <metadata>
      <version>1</version>
        <dependencies>
            <dependency>profile-plone.app.contenttypes:plone-content</dependency>
        </dependencies>
    </metadata>

If you use the profile ``default`` then the default-content in new sites will still be Archetypes-based. You'll then have to migrate that content using the migration-form ``@@atct_migrator`` or delete it by hand.


Using folderish types
^^^^^^^^^^^^^^^^^^^^^

At some point all default types will probably be folderish. If you want the default types to be folderish before that happens please look at https://pypi.python.org/pypi/collective.folderishtypes.


Changing the base class for existing objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you changed the base-class of existing types (e.g. because you changed them to be folderish) you also need to upgrade the base-class of existing objects. You can use the following form for this: ``@@base_class_migrator_form``.

This form lets you select classes to be updated and shows the number of objects for each class. This form can be used to change the base-class of any dexterity-types instances. The migration will also transform itemish content to folderish content if the new class is folderish. You might want to use the method ``plone.app.contenttypes.migration.dxmigration.migrate_base_class_to_new_class`` in your own upgrade-steps.


Extending the types
^^^^^^^^^^^^^^^^^^^

You have several options:

1. Extend the types through-the-web by adding new fields or behaviors in the types-controlpanel ``/@@dexterity-types``.

2. Extend the types with a custom type-profile that extends the existing profile with behaviors, or fields.

   You will first have to add the type to your ``[yourpackage]/profiles/default/types.xml``.

   .. code:: xml

    <?xml version="1.0"?>
    <object name="portal_types" meta_type="Plone Types Tool">
      <object name="Folder" meta_type="Dexterity FTI" />
    </object>

   Here is an example that enables the image-behavior for Folders in ``[yourpackage]/profiles/default/types/Folder.xml``:

   .. code:: xml

    <?xml version="1.0"?>
    <object name="Folder" meta_type="Dexterity FTI">
     <property name="behaviors" purge="False">
      <element value="plone.app.contenttypes.behaviors.leadimage.ILeadImage"/>
     </property>
    </object>

   By adding a schema-definition to the profile you can add fields.

   .. code:: xml

    <?xml version="1.0"?>
    <object name="Folder" meta_type="Dexterity FTI">
     <property name="model_file">your.package.content:folder.xml</property>
     <property name="behaviors" purge="False">
      <element value="plone.app.contenttypes.behaviors.leadimage.ILeadImage"/>
     </property>
    </object>

   Put the schema-xml in ``your/package/content/folder.xml`` (the folder ``content`` needs a ``__init__.py``)

   .. code:: xml

    <model xmlns:security="http://namespaces.plone.org/supermodel/security"
           xmlns:marshal="http://namespaces.plone.org/supermodel/marshal"
           xmlns:form="http://namespaces.plone.org/supermodel/form"
           xmlns="http://namespaces.plone.org/supermodel/schema">
      <schema>
        <field name="teaser_title" type="zope.schema.TextLine">
          <description/>
          <required>False</required>
          <title>Teaser title</title>
        </field>
        <field name="teaser_subtitle" type="zope.schema.Text">
          <description/>
          <required>False</required>
          <title>Teaser subtitle</title>
        </field>
        <field name="teaser_details" type="plone.app.textfield.RichText">
          <description/>
          <required>False</required>
          <title>Teaser details</title>
        </field>
      </schema>
    </model>

You could alternatively override the peroperty ``model_file`` of the type-definition with a empty string and use the property ``schema`` to provide your custom python-schema.

For more complex features you should always consider create custom behaviors and/or write your own content-types since that will most likely give you more flexibility and less problem when you want to upgrade to a newer version in the future.

For more information on custom dexterity-types and custom behaviors please read the `dexterity documentation <http://docs.plone.org/external/plone.app.dexterity/docs/>`_.


Differences to Products.ATContentTypes
--------------------------------------

- The image of the News Item is not a field on the contenttype but a behavior that can add a image to any contenttypes (similar to http://pypi.python.org/pypi/collective.contentleadimage)
- All richtext-fields are also provided by a reuseable behavior.
- The functionality to transform (rotate and flip) images has been removed.
- There is no more field ``Location``. If you need georeferenceable consider using ``collective.geo.behaviour``
- The link on the image of the newsitem triggers an overlay
- The link-type now allows the of the variables ``${navigation_root_url}`` and ``${portal_url}`` to construct relative urls.
- The ``getQuery()`` function now returns a list of dict instead of a list of CatalogContentListingObject;
  use of ``getRawQuery()`` is deprecated.
- The views for Folders and Collections changed their names and now share a common implementation (since version 1.2a8):

  - ``folder_listing_view`` (Folders) and ``collection_view`` (Collections) -> ``listing_view`` (Folders and Collections)
  - ``folder_summary_view`` (Folders) and ``summary_view`` (Collections) -> ``summary_view`` (Folders and Collections)
  - ``folder_tabular_view`` (Folders) and ``tabular_view`` (Collections) -> ``tabular_view`` (Folders and Collections)
  - ``folder_full_view`` (Folders) and ``all_content`` (Collections) -> ``full_view`` (Folders and Collections)
  - ``atct_album_view`` (Folders) and ``thumbnail_view`` (Collections) -> ``album_view`` (Folders and Collections)



Toubleshooting
--------------

Please report issues in the bugtracker at https://github.com/plone/plone.app.contenttypes/issues.

ValueError on installing
^^^^^^^^^^^^^^^^^^^^^^^^^

When you try to install plone.app.contenttypes < 1.1a1 in a existing site you might get the following error::

      (...)
      Module Products.GenericSetup.utils, line 509, in _importBody
      Module Products.CMFCore.exportimport.typeinfo, line 60, in _importNode
      Module Products.GenericSetup.utils, line 730, in _initProperties
    ValueError: undefined property 'schema'

Before installing plone.app.contenttypes you have to reinstall plone.app.collection to update collections to the version that uses Dexterity.


Branches
--------

The master-branch supports Plone 5 only. From this 1.2.x-releases will be cut.

The 1.1.x-branch supports Plone 4.3.x. From this 1.1.x-releases will be cut.


License
-------

GNU General Public License, version 2


Contributors
------------

* Philip Bauer <bauer@starzel.de>
* Michael Mulich <michael.mulich@gmail.com>
* Timo Stollenwerk <contact@timostollenwerk.net>
* Peter Holzer <hpeter@agitator.com>
* Patrick Gerken <gerken@starzel.de>
* Steffen Lindner <lindner@starzel.de>
* Daniel Widerin <daniel@widerin.net>
* Jens Klein <jens@bluedynamics.com>
* Joscha Krutzki <joka@jokasis.de>
* Mathias Leimgruber <m.leimgruber@4teamwork.ch>
* Matthias Broquet <mbroquet@atreal.fr>
* Wolfgang Thomas <thomas@syslab.com>
* Bo Simonsen <bo@geekworld.dk>
* Andrew Mleczko <andrew@mleczko.net>
* Roel Bruggink <roel@jaroel.nl>
* Carsten Senger <senger@rehfisch.de>
* Rafael Oliveira <rafaelbco@gmail.com>
* Martin Opstad Reistadbakk <martin@blaastolen.com>
* Nathan Van Gheem <vangheem@gmail.com>
* Johannes Raggam <raggam-nl@adm.at>
* Jamie Lentin <jm@lentin.co.uk>
* Maurits van Rees <maurits@vanrees.org>
* David Glick <david@glicksoftware.com>
* Kees Hink <keeshink@gmail.com>
* Roman Kozlovskyi <krzroman@gmail.com>
* Gauthier Bastien <gauthier.bastien@imio.be>
* Andrea Cecchi <andrea.cecchi@redturtle.it>
* Bogdan Girman <bogdan.girman@gmail.com>
* Martin Opstad Reistadbakk <martin@blaastolen.com>
* Florent Michon <fmichon@atreal.fr>
* Héctor Velarde <hector.velarde@gmail.com>


Changelog
=========

1.4.9 (2018-02-11)
------------------

New features:

- Members folder made permanently private. Fixes https://github.com/plone/Products.CMFPlone/issues/2259
  [mrsaicharan1]


1.4.8 (2018-02-05)
------------------

Bug fixes:

- Do not use ``portal_quickinstaller`` in the migration form.
  Use ``get_installer`` to check if ``plone.app.contenttypes`` is
  installed or installable.  Use ``portal_setup`` directly for
  blacklisting the ``type_info`` step when installing our profile.
  [maurits]

- Add Python 2 / 3 compatibility
  [pbauer]


1.4.7 (2017-12-14)
------------------

Bug fixes:

- Rename post_handlers. Fixes https://github.com/plone/Products.CMFPlone/issues/2238
  [pbauer]


1.4.6 (2017-11-26)
------------------

New features:

- Allow to patch searchableText index during migrations.
  [pbauer]

- Expose option to skip catalog-reindex after migration in form.
  [pbauer]

Bug fixes:

- Remove last use of ``atcontenttypes`` translation domain.
  Fixes `issue 37 <https://github.com/plone/plone.app.contenttypes/issues/37>`_.
  [maurits]

- Don't overwrite existing settings for Plone Site.
  [roel]


1.4.5 (2017-10-06)
------------------

Bug fixes:

- Do not install plone.app.discussion when installing plone.app.contenttypes.
  [timo]


1.4.4 (2017-10-02)
------------------

New features:

- Test SVG handling
  [tomgross]

- Use post_handler instead of import_steps.
  [pbauer]

Bug fixes:

- Do not use a default value in the form of ``http://`` for the link.
  The new link widget resolves that to the portal root object.
  Also, it's not a valid URL.
  Fixes: https://github.com/plone/Products.CMFPlone/issues/2163
  [thet]

- Remove obsolete HAS_MULTILINGUAL from utils.
  [pbauer]

- Clean up all ``__init__`` methods of the browser views to avoid unnecessary code execution.
  [thet]

- Make sure the effects of the robotframework REMOTE_LIBRARY_BUNDLE_FIXTURE
  fixture are not accidentally removed as part of tearing down the
  PLONE_APP_CONTENTTYPES_ROBOT_FIXTURE.
  [davisagli]


1.4.3 (2017-08-30)
------------------

Bug fixes:

- Disable queuing of indexing-operations (PLIP https://github.com/plone/Products.CMFPlone/issues/1343)
  during migration to Dexterity to prevent catalog-errors.
  [pbauer]


1.4.2 (2017-08-27)
------------------

New features:

- Index default values when indexing the file fails due to a missing binary.
  [pbauer]

- Allow to skip rebuilding the catalog when migrating at to dx in code.
  [pbauer]

Bug fixes:

- Add translation namesspace and i18n:translate to the dexterity schema
  definitions for the content types that have extra field defined on top of the
  behavior composition. Otherwise no translations can be picked up.
  [fredvd]

- Use original raw text and mimetype when indexing rich text.
  This avoids a double transform (raw source to output mimetype to plain text).
  Includes a reindex of the SearchableText index for Collections, Documents and News Items.
  `Issue 2066 <https://github.com/plone/Products.CMFPlone/issues/2066>`_.
  [maurits]

- Migrate the richtext-field 'text' when migrating ATTopics to Collections.
  [pbauer]

- Remove Language='all' from migration-query since it was removed from p.a.multilingual
  [pbauer]

- Actually migrate all migratable types when passing 'all' to at-dx migration.
  [pbauer]

- Remove plone.app.robotframework 'reload' extra.
  This allows to remove quite some other external dependencies that are not Python 3 compatible.
  [gforcada]

1.4.1 (2017-07-03)
------------------

New features:

- Integrate new link widget from plone.app.z3cform.
  [tomgross]

Bug fixes:

- Made sure the text field of Collections is searchable.
  `Issue 406 <https://github.com/plone/plone.app.contenttypes/issues/406>`_.
  [maurits]

- Fix issue preventing disabling icons and/or thumbs globally.
  [fgrcon]

1.4 (2017-06-03)
----------------


New features:

- New metadata catalog column MimeType
  https://github.com/plone/Products.CMFPlone/issues/1995
  [fgrcon]

- new behavior: IThumbIconHandling, supress thumbs /icons, adjust thumb size, templates adapted
  https://github.com/plone/Products.CMFPlone/issues/1734 (PLIP)

Bug fixes:

- fixed css-classes for thumb scales ...
  https://github.com/plone/Products.CMFPlone/issues/2077
  [fgrcon]

- Fix test for checking if TinyMCE is loaded which broke after https://github.com/plone/Products.CMFPlone/pull/2059
  [thet]

- Fix flaky test in test_indexes.
  [thet]

- removed unittest2 dependency
  [kakshay21]

- Fix issue where contentFilter could not be read from request
  [datakurre]


1.3.0 (2017-03-27)
------------------

New features:

- Make use of plone.namedfile's tag() function to generate img tags. Part of plip 1483.
  [didrix]

Bug fixes:

- Avoid failure during migration if relation is broken.
  [cedricmessiant]

- Fix import location for Products.ATContentTypes.interfaces.
  [thet]

1.2.22 (2017-02-20)
-------------------

Bug fixes:

- Add condition so custom folder migration does not fail if there is not
  an 'excludeFromNav'
  [cdw9]


1.2.21 (2017-02-05)
-------------------

New features:

- Remove browserlayer from listing views to allow overrides from other packages
  [agitator]

Bug fixes:

- Use helper method to retrieve all catalog brains in migration code, because Products.ZCatalog removed the ability to get all brains by calling the catalog without arguments.
  [thet, gogobd]

- Fix use of add_file in testbrowser tests. [davisagli]

- Render migration results without using Zope session. [davisagli]


1.2.20 (2017-01-20)
-------------------

Bug fixes:

- Use unicode string when .format() parameter is unicode for the field migrator
  [frapell]


1.2.19 (2016-12-02)
-------------------

Bug fixes:

- Fix SearchableText indexer, using textvalue.mimeType
  [agitator]

- Fix Mimetype icon path. With the removal of the skins folder in
  https://github.com/plone/Products.MimetypesRegistry/pull/8/commits/61acf8327e5c844bff9e5c5676170aaf0ee2c323
  we need the full resourcepath now
  [agitator]

- Show message for editors when viewing Link.
  Fixes `issue 375 <https://github.com/plone/plone.app.contenttypes/issues/375>`_.
  [maurits]

- Update code to follow Plone styleguide.
  [gforcada]

- Update File.xml view action url_expr to append /view
  Fixes 'issue 378' <https://github.com/plone/plone.app.contenttypes/issues/378>`_.
  [lbrannon]


1.2.18 (2016-09-14)
-------------------

Bug fixes:

- Correct the SearchableText base indexer: use mime type of RichText output
  (rather than raw) value in plaintext conversion. Fixes #357.
  [petri]


1.2.17 (2016-08-18)
-------------------

New features:

- Configure edit urls for locking support, where locking support is enabled.
  [thet]

- Add ``i18n:attribute`` properies to all action nodes for FTI types.
  [thet]

- added few pypi links in 'Migration' section
  [kkhan]

Bug fixes:

- Marked relative location criterion robot test as unstable.
  This needs further investigation, but must not block Plone development.
  See issue https://github.com/plone/plone.app.contenttypes/issues/362
  [maurits]

- Remove ``path`` index injection in "plone.collection" behaviors ``results`` method.
  It is a duplicate.
  Exactly the same is done already in the ``plone.app.querybuilder.querybuilder._makequery``,
  which is called by above ``results`` method.
  [jensens]

- Select all migratable types in migration-form by default. Fixes #193.
  [pbauer]

- Use zope.interface decorator.
  [gforcada]

- Mark robot test ``plone.app.contenttypes.tests.test_robot.RobotTestCase.Scenario Test Absolute Location Criterion`` as unstable.
  This needs further investigation, but must not block Plone development.
  [jensens]

- corrected typos in the documentation
  [kkhan]


1.2.16 (2016-06-12)
-------------------

Bug fixes:

- Wait longer to fix unstable robot tests.  [maurits]


1.2.15 (2016-06-06)
-------------------

Bug fixes:

- Fixed possible cross site scripting (XSS) attack in lead image caption.  [maurits]


1.2.14 (2016-05-25)
-------------------

Bug fixes:

- Encode the linked url for the Link type to allow for non ascii characters in the url.
  [martior]


1.2.13 (2016-05-12)
-------------------

Fixes:

- Deferred adapter lookup in collection view.
  This was looked up for contentmenu/toolbar at every authenticated request.
  It also had side effects if custom collection behaviors are used.
  [jensens]

- Fixed unstable robot test for location criterion.  [maurits]

- Don't fail for ``utils.replace_link_variables_by_paths``, if value is ``None``.
  The value can be ``None`` when creating a ``Link`` type with ``invokeFactory`` without ``remoteUrl`` set and calling the indexer before setting the URL.
  [thet]


1.2.12 (2016-04-13)
-------------------


New:

- assign shortnames to behaviors as supported by plone.behavior
  [thet]


1.2.11 (2016-03-31)
-------------------

New:

- WebDAV support for File and Image
  [ebrehault]

Fixes:

- Made xpath expression in test less restrictive.
  [maurits]

- Register explicitly plone.app.event dependency on configure.zcml.
  [hvelarde]


1.2.10 (2016-02-27)
-------------------

New:

- Added *listing* macro as found in ``listing.pt`` to
  ``listing_album.pt`` and ``listing_tabular.pt`` for
  a coherent customization.
  [tomgross]

Fixes:

- Check if there is a non-empty leadimage field for migration.
  [bsuttor]

- Make sure to have image scale before generating tag for album view.
  [vangheem]

- Also remove collections upon uninstalling.
  [pbauer]

- Various fixes while migrating custom contenttypes:

  - do not fail if source object does not have a 'excludeFromNav' field;
  - do not fail if source object field's label contains special characters;
  - do not try to migrate assigned portlets if source object is not
    portlet assignable.
    [gbastien]

- No longer try to install ATContentTypes-types on uninstalling.
  [pbauer]

- Enhancement: Split up migration test for modification date and references
  in two functions for easier debugging.
  [jensens]

- Simplify test in robot framework which fails in its newer version.
  [jensens]


1.2.9 (2016-01-08)
------------------

Fixes:

- Change all text getters on ``plone.app.textfield.value.RichTextValue``
  objects to ``output_relative_to`` with the current context. This correctly
  transforms relative links. See:
  https://github.com/plone/plone.app.textfield/issues/7
  [thet]


1.2.8 (2015-12-15)
------------------

Fixes:

- fix issue in migration where source or target uuid could not
  be found
  [vangheem]


1.2.7 (2015-11-28)
------------------

Fixes:

- Index subject field on the catalog so that is searchable.
  Fixes https://github.com/plone/plone.app.contenttypes/issues/194
  [gforcada]


1.2.6 (2015-11-25)
------------------

New:

- Allow to pass custom field_migrator methods with custom migrations.
  [pbauer]

Fixes:

- Create standard news/events collections with ``selection.any``.
  Issue https://github.com/plone/Products.CMFPlone/issues/1040
  [maurits]

- Avoid AttributeError from potential acquisition issues with folder listings
  [vangheem]

- Avoid AttributeError when trying to get the default_page of an item
  when migrating
  [frapell]

- Used html5 doctype in image_view_fullscreen.  Now it can be parsed
  correctly by for example i18ndude.
  [maurits]

- Use plone i18n domain in zcml.
  [vincentfretin]

- Do a ``IRichText`` text indexing on all registered SearchableText indexers by
  doing it as part of the base ``SearchableText`` function. Convert the text
  from the source mimetype to ``text/plain``.
  [thet]

- Add ``getRawQuery`` method to Collection content type for backward compatibility with Archetypes API.
  Fixes (partially) https://github.com/plone/plone.app.contenttypes/issues/283.
  [hvelarde]


1.2.5 (2015-10-28)
------------------

Fixes:

- Fix custom migration from and to types with spaces in the type-name.
  [pbauer]

- Fixed full_view when content is not IUUIDAware (like the portal).

- Cleanup and rework: contenttype-icons
  and showing thumbnails for images/leadimages in listings ...
  https://github.com/plone/Products.CMFPlone/issues/1226
  [fgrcon]

- Fix full_view when content is not IUUIDAware (like the portal).
  Fixes https://github.com/plone/Products.CMFPlone/issues/1109.
  [pbauer]

- Added plone.app.linkintegrity to dependencies due to test-issues.
  [pbauer]


1.2.4 (2015-09-27)
------------------

- Fixed full_view error when collection contains itself.
  [vangheem]

- test_content_profile: do not appy Products.CMFPlone:plone.
  [maurits]


1.2.3 (2015-09-20)
------------------

- Do not raise an exception for items where @@full_view_item throws an
  exception. Instead hide the object.
  [pbauer]

- Do not raise errors when IPrimaryFieldInfo(obj) fails (e.g. when the
  Schema-Cache is gone).
  Fixes https://github.com/plone/Products.CMFPlone/issues/839
  [pbauer]

- Fix an error with logging an exception on indexing SearchableText for files
  and concating utf-8 encoded strings.
  [thet]

- Make consistent use of LeadImage behavior everywhere. Related to
  plone/plone.app.contenttypes#1012. Contentleadimages no longer show up in
  full_view since they are a viewlet.
  [sneridagh, pbauer]

- Fixed the summary_view styling
  [sneridagh]
- redirect_links property has moved to the configuration registry.
- redirect_links, types_view_action_in_listings properies have moved to the
  configuration registry.
  [esteele]


1.2.2 (2015-09-15)
------------------

- Prevent negative ints and zero when limiting collection-results.
  [pbauer]


1.2.1 (2015-09-12)
------------------

- Migrate next-previous-navigation.
  Fix https://github.com/plone/plone.app.contenttypes/issues/267
  [pbauer]


1.2.0 (2015-09-07)
------------------

- Handle languages better for content that is create when site is generated
  [vangheem]

- In ``FolderView`` based views, don't include the ``portal_types`` query, if
  ``object_provides`` is set in the ``results`` method keyword arguments. Fixes
  a case, where no Album Images were shown, when portal_state's
  ``friendly_types`` didn't include the ``Image`` type.
  [thet]


1.2b4 (2015-08-22)
------------------

- Test Creator criterion with Any selection.
  [mvanrees]

- Selection criterion converter: allow selection.is alternative operation.
  [mvanrees]

- Fixed corner case in topic migration.
  [mvanrees]

- Use event_listung for /events/aggregator in new sites.
  [pbauer]

- Remove obsolete collections.css
  [pbauer]

- Add plone.app.querystring as a dependency (fixes collections migrated to p5
  and dexterity).
  [pbauer]

- Migrate layout of portal to use the new listing-views when migrating to dx.
  [pbauer]

- Migrate layout using the new listing-views when migrating folders,
  collections, topics.
  [pbauer]

- Update allowed view_methods of the site-root on installing or migrating.
  Fixes #25.
  [pbauer]

- Set default_view when updating view_methods. Fixes #250.
  [pbauer]

- Fix bug in reference-migrations where linkintegrity-relations were turned
  into relatedItems.
  [pbauer]

- Setup calendar and visible ids even when no default-content gets created.
  [pbauer]

- Remove upgrade-step that resets all behaviors. Fixes #246.
  [pbauer]

- Add convenience-view @@export_all_relations to export all relations.
  [pbauer]

- Add method link_items that allows to link any kind of item (AT/DX) with any
  kind of relationship.
  [pbauer]

- New implementation of reference-migrations.
  [pbauer]

- Fix i18n on custom_migration view.
  [vincentfretin]


1.2b3 (2015-07-18)
------------------

- Fix BlobNewsItemMigrator.
  [MrTango]

- Fix ATSelectionCriterionConverter to set the right operators.
  [MrTango]

- Fix @@custom_migraton when they type-name has a space (fixes #243).
  [pbauer]

- Get and set linkintegrity-setting with registry.
  [pbauer]

- Use generic field_migrators in all migrations.
  [pbauer]

- Remove superfluous 'for'. Fixes plone/Products.CMFPlone#669.
  [fulv]


1.2b2 (2015-06-05)
------------------

- Use modal pattern for news item image instead of jquery tools.
  [vangheem]


1.2b1 (2015-05-30)
------------------

- Keep additional view_methods when migrating to new view_methods. Fixes #231.
  [pbauer]

- Fix upgrade-step to use new view_methods.
  [pbauer]

- Fix possible error setting fields for tabular_view for
  collections.  Issue #209.
  [maurits]


1.2a9 (2015-05-13)
------------------

- Provide table of contents for document view.
  [vangheem]

- Default to using locking support on Page, Collection, Event and News Item types.
  [vangheem]

- Show the LeadImageViewlet only on default views.
  [thet]


1.2a8 (2015-05-04)
------------------

- Follow best practice for CHANGES.rst.
  [timo]

- Add migrations from custom AT types to available DX types (fix #133).
  [gbastien, cekk, tiazma, flohcim, pbauer]

- Fix ``contentFilter`` for collections.
  [thet]

- Don't batch the already batched collection results. Fixes #221.
  [thet]

- I18n fixes.
  [vincentfretin]

- Fix ``test_warning_for_uneditable_content`` to work with recent browser layer
  changes in ``plone.app.z3cform``.
  [thet]

- Update image_view_fullscreen.pt for mobile friendliness.
  [fulv]

- Removed dependency on CMFDefault
  [tomgross]


1.2a7 (2015-03-27)
------------------

- Re-relase 1.2a6. See https://github.com/plone/plone.app.contenttypes/commit/7cb74a2fcbf108acd43fe4ae3713f007db2073bf for details.
  [timo]


1.2a6 (2015-03-26)
------------------

- In the listing view, don't repeat on the ``article`` tag, which makes it
  impossible to override this structure. Instead, repeat on a unrendered
  ``tal`` tag and move the article tag within.
  [thet]

- Don't try to show IContentLeadImage images, if theree none. Use the "mini"
  scale as default scale for IContentLeadImage.
  [thet]

- Improve handling of Link types with other URL schemes than ``http://`` and
  ``https://``.
  [thet]

- When installing the default profile, restrict uninstalling of old types to
  old FTI based ones.
  [thet]

- Reformatted all templates for 2 space indentation, 4 space for attributes.
  [thet]

- Register folder and collection views under the same name. Old registrations
  are kept for BBB compatibility.
  [thet]

- Refactor full_view and incorporate fixes from collective.fullview to
  1) display the default views of it's items, 2) be recursively callable
  and 3) have the same templates for folder and collections.
  [thet]

- Refactor folder_listing, folder_summary_view, folder_tabular_view and
  folder_album_view for folders as well as standard_view (collection_view),
  summary_view, tabular_view and thumbnail_view for collections to use the same
  templates and base view class.
  [thet]

- In the file view, render HTML5 ``<audio>`` or ``<video>`` tags for audio
  respectively video file types. Ancient browsers, which do not support that,
  just don't render these tags.
  [thet]

- Define ``default_page_types`` in the ``propertiestool.xml`` profile.
  [thet]

- Add ``event_listing`` to available view methods for the Folder and Collection
  types.
  [thet]

- Add migration for images added with collective.contentleadimage.
  [pbauer]

- Add migration for contentrules.
  [pbauer]

- Fix folder_full_view_item and allow overriding with jbot (fix #162).
  [pbauer]

- Migrate comments created with plone.app.discussion.
  [gbastien, pbauer]

- Allow migrating Topics and Subtopics to folderish Collections.
  [pbauer]

- Add migration from Topics to Collections (fixes #131).
  [maurits, pbauer]

- Add helpers and a form to update object with changed base class. Also
  allows migrating from itemish to folderish.
  [bogdangi, pbauer]

- Keep portlets when migrating AT to DX (fixes #161)
  [frisi, gbastien, petschki]


1.2a5 (2014-10-23)
------------------

- Code modernization: sorted imports, use decorators, utf8 headers.
  [jensens]

- Fix: Added missing types to CMFDiffTool configuraion.
  [jensens]

- Integration of the new markup update and CSS for both Plone and Barceloneta
  theme. This is the work done in the GSOC Barceloneta theme project. Fix
  several templates.
  [albertcasado, sneridagh]


1.2a4 (2014-09-17)
------------------

- Include translated content into migration-information (see #170)
  [pbauer]

- Add simple confirmation to prevent unintentional migration.
  [pbauer]

- Don't remove custom behaviors on reinstalling.
  [pbauer]

- Add bbb getText view for content with IRichText-behavior
  [datakurre]

- Support ``custom_query`` parameter in the ``result`` method of the
  ``Collection`` behavior. This allows for run time customization of the
  stored query, e.g. by request parameters.
  [thet]

- Fix 'AttributeError: image' when NewsItem unused the lead image behavior.
  [jianaijun]

- Restore Plone 4.3 compatibility by depending on ``plone.app.event >= 2.0a4``.
  The previous release of p.a.c got an implicit Plone 5 dependency through a
  previous version of plone.app.event.
  [thet]

- Replace AT-fti with DX-fti when migrating a type.
  [esteele, pbauer]

- Only show migrateable types (fixes #155)
  [pbauer]

- Add logging during and after migration (fixes #156)
  [pbauer]

- When replacing the default news and events collections, reverse the
  sort order correctly.
  [maurits]


1.2a3 (2014-04-19)
------------------

- Adapt to changes of plone.app.event 2.0.
  [thet]

- Fix issue when mimetype can be None.
  [pbauer]


1.2a2 (2014-04-13)
------------------

- Enable IShortName for all default-types.
  [pbauer, mikejmets]

- Add form to install pac and forward to dx_migration
  after a successful migration to Plone 5
  [pbauer]

- Rename atct_album_view to folder_album_view.
  [pbauer]

- Do a better check, if LinguaPlone is installed, based on the presence of the
  "LinguaPlone" browser layer. Asking the quick installer tool might claim it's
  installed, where it's not.
  [thet]

- Register folderish views not for plone.app.contenttypes' IFolder but for
  plone.dexterity's IDexterityContainer. Now, these views can be used on any
  folderish Dexterity content.
  [thet]

- Add a ICustomMigrator interface to the migration framework, which can be used
  to register custom migrator adapters. This can be useful to add custom
  migrators to more than one or all content types. For example for
  schemaextenders, which are registered on a interface, which is provided by
  several content types.
  [thet]

- In the migration framework, fix queries for Archetype objects, where only
  interfaces are used to skip brains with no or Dexterity meta_type. In some
  cases Dexterity and Archetype objects might provide the same marker
  interfaces.
  [thet]

- Add logging messages to content migrator for more verbosity on what's
  happening while running the migration.
  [thet]

- Use Plone 4 based @@atct_migrator and @@atct_migrator_results template
  structure.
  [thet]


1.2a1 (2014-02-22)
------------------

- Fix viewlet warning about ineditable content (fixes #130)
  [pbauer]

- Reintroduce the removed schema-files and add upgrade-step to migrate to
  behavior-driven richtext-fields (fixes #127)
  [pbauer]

- Delete Archetypes Member-folder before creating new default-content
  (fixes #128)
  [pbauer]

- Remove outdated summary-behavior from event (fixes #129)
  [pbauer]


1.1b3 (2014-09-07)
------------------

- Include translated content into migration-information (see #170)
  [pbauer]

- Add simple confirmation to prevent unintentional migration.
  [pbauer]

- Don't remove custom behaviors on reinstalling.
  [pbauer]

- Remove enabling simple_publication_workflow from testing fixture.
  [timo]

- Only show migrateable types (fixes #155)
  [pbauer]

- Add logging during and after migration (fixes #156)
  [pbauer]

- Remove 'robot-test-folder' from p.a.contenttypes test setup. It is bad to
  add content to test layers, especially if those test layers are used by
  other packages.
  [timo]

- When replacing the default news and events collections, reverse the
  sort order correctly.
  [maurits]

- For plone.app.contenttypes 1.1.x, depend on plone.app.event < 1.1.999.
  Closes/Fixes #149.
  [khink, thet]


1.1b2 (2014-02-21)
------------------

- Fix viewlet warning about ineditable content (fixes #130)
  [pbauer]

- Reintroduce the removed schema-files and add upgrade-step to migrate to
  behavior-driven richtext-fields (fixes #127)
  [pbauer]

- Delete Archetypes Member-folder before creating new default-content
  (fixes #128)
  [pbauer]

- Remove outdated summary-behavior from event (fixes #129)
  [pbauer]


1.1b1 (2014-02-19)
------------------

- Add tests for collections and collection-migrations.
  [pbauer]

- Removed Plone 4.2 compatibility.
  [pbauer]

- Add migration of at-collections to the new collection-behavior.
  [pbauer]

- Display richtext in collection-views.
  [pbauer]

- Reorganize and improve documentation.
  [pbauer]

- Add a richtext-behavior and use it in for all types.
  [amleczko, pysailor]

- Improve the migration-results page (Fix #67).
  [pbauer]

- For uneditable content show a warning and hide the edit-link.
  [pbauer]

- Keep all modification-date during migration (Fix #62).
  [pbauer]

- Only attempt transforming files if valid content type.
  [vangheem]

- Make the collection behavior aware of INavigationRoot. Fixes #98
  [rafaelbco]

- Use unique URL provided by ``plone.app.imaging`` to show the large version
  of a news item's lead image. This allows use of a stronger caching policy.
  [rafaelbco]

- Fix URL for Link object on the navigation portlet if it
  contains variables (Fix #110).
  [rafaelbco]


1.1a1 (2013-11-22)
------------------

- Event content migration for Products.ATContentTypes ATEvent,
  plone.app.event's ATEvent and Dexterity example type and
  plone.app.contenttypes 1.0 Event to plone.app.contenttypes 1.1
  Event based on plone.app.event's Dexterity behaviors.
  [lentinj]

- Remove DL's from portal message templates.
  https://github.com/plone/Products.CMFPlone/issues/153
  [khink]

- Collection: get ``querybuilderresults`` view instead of using the
  ``QueryBuilder`` class directly.
  [maurits]

- Fix migration restoreReferencesOrder removes references
  [joka]

- Enable summary_view and all_content views for content types that
  have the collection behavior enabled.  Define collection_view for
  those types so you can view the results.  These simply show the
  results.  The normal view of such a type will just show all fields
  in the usual dexterity way.
  [maurits, kaselis]

- Add customViewFields to the Collection behavior.  This was available
  on old collections too.
  [maurits, kaselis]

- Change Collection to use a behavior.  Issue #65.
  [maurits, kaselis]

- Improved test coverage for test_migration
  [joka]

- Add tests for vocabularies used for the migration
  [maethu]

- Add migration-form /@@atct_migrate based on initial work by gborelli
  [pbauer, tiazma]

- Add ATBlob tests and use migration layer for test_migration
  [joka]

- Integrate plone.app.event.
  [thet]


1.0 (2013-10-08)
----------------

- Remove AT content and create DX-content when installing in a fresh site.
  [pbauer]

- Remove obsolete extra 'migrate_atct'.
  [pbauer]

- Add link and popup to the image of News Items.
  [pbauer]

- Use the default profile title for the example content profile.
  [timo]

- Unicode is expected, but ``obj.title`` and/or ``obj.description`` can be
  still be None in SearchableText indexer.
  [saily]


1.0rc1 (2013-09-24)
-------------------

- Implement a tearDownPloneSite method in testing.py to prevent test
  isolation problems.
  [timo]

- Its possible to upload non-image data into a newsitem. The view was broken
  then. Now it shows the uploaded file for download below the content. Its no
  longer broken.
  [jensens]

- Add contributor role as default for all add permissions in order to
  work together with the different plone worklfows, which assume it is
  set this way.
  [jensens]

- fix #60: File Type has no mimetype specific icon in catalog metadata.
  Also fixed for Image.
  [jensens]

- fix #58: Migration ignores "Exclude from Navigation".
  [jensens]

- disable LinkIntegrityNotifications during migrations, closes #40.
  [jensens]

- Fix Bug on SearchableText_file indexer when input stream contains
  characters not convertable in ASCII. Assumes now utf-8 and replaces
  all unknown. Even if search can not find the words with special
  characters in, indexer does not break completely on those items.
  [jensens]

- Remove dependency on plone.app.referenceablebehavior, as it depends on
  Products.Archetypes which installs the uid_catalog.
  [thet]

- Make collection syndicatable.
  [vangheem]

- Include the migration module not only when Products.ATContentTypes is
  installed but also archetypes.schemaextender. The schemaextender might not
  always be available.
  [thet]

- Add fulltext search of file objects.
  [do3cc]

- Fix link_redirect_view: Use index instead of template class var to
  let customization by ZCML of the template.
  [toutpt]

- Add a permission for each content types.
  [toutpt]


1.0b2 (2013-05-31)
------------------

- Fix translations to the plone domain, and some translations match existing
  translations in the plone domain. (ported from plone.app.collection)
  [bosim]

- Fix atct_album_view and don't use atctListAlbum.py.
  [pbauer]

- Add constrains for content create with the Content profile.
  [ericof]

- Add SearchableText indexer to Folder content type.
  [ericof]

- Fix atct_album_view.
  [pbauer]

- Removed dependency for collective.dexteritydiff since its features were
  merged into Products.CMFDiffTool.
  [pbauer]

- Add test for behavior table_of_contents.
  [pbauer]

- Add migration for blobnewsitems as proposed in
  https://github.com/plone/plone.app.blob/pull/2.
  [pbauer]

- Require cmf.ManagePortal for migration.
  [pbauer]

- Always migrate files and images to blob (fixes #26).
  [pbauer]

- Add table of contents-behavior for documents.
  [pbauer]

- Add versioning-behavior and it's dependencies.
  [pbauer]

- Remove image_view_fullscreen from the display-dropdown.
  [pbauer]

- Enable selecting addable types on folders by default.
  [pbauer]

- Fix reference-migrations if some objects were not migrated.
  [pbauer]

- Keep the order references when migrating.
  [pabo3000]

- Move templates into their own folder.
  [pbauer]

- Moved migration related code to specific module.
  [gborelli]

- Added migration Collection from app.collection to app.contenttypes.
  [kroman0]

- Add missing ``i18n:attributes`` to 'Edit' and 'View' actions of File type.
  [saily]

- Bind 'View' action to ``${object_url}/view`` instead of
  ``${object_url}`` as in ATCT for File and Image type.
  [saily]

- Fixed installation of p.a.relationfield together with p.a.contenttypes.
  [kroman0]

- Fixed creating aggregator of events on creating Plone site.
  [kroman0]

- Added titles for menuitems.
  [kroman0]

- Hide uninstall profile from @@plone-addsite.
  [kroman0]

- Fix 'ImportError: cannot import name Counter' for Python 2.6.
  http://github.com/plone/plone.app.contenttypes/issues/19
  [timo]

- Move XML schema definitions to schema folder.
  [timo]

- Prevent the importContent step from being run over and over again.
  [pysailor]

- Add build status image.
  [saily]

- Merge plone.app.collection (Tag: 2.0b5) into plone.app.contenttypes.
  [timo]

- Refactor p.a.collection robot framework tests.
  [timo]


1.0b1 (2013-01-27)
------------------

- Added mime type icon for file.
  [loechel]

- Lead image behavior added.
  [timo]

- Make NewsItem use the lead image behavior.
  [timo]

- SearchableText indexes added.
  [reinhardt]

- Set the text of front-page when creating a new Plone.
  [pbauer]

- Robot framework test added.
  [Gomez]


1.0a2 (unreleased)
------------------

- Move all templates from skins to browser views.
  [timo]

- User custom base classes for all content types.
  [timo]

- Migration view (@@fix_base_classes) added to migrate content objects that
  were created with version 1.0a1.
  [timo]

- Mime Type Icon added for File View.
  [loechel]


1.0a1 (unreleased)
------------------

- Initial implementation.
  [pbauer, timo, pumazi, agitator]


