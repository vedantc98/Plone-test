Overview
========

Collections in Plone are the most powerful tool content editors and site
managers have to construct navigation and site sections.

This is a brand new implementation of collections for Plone, using
ajax/javascript to make a simpler, easier and streamlined user experience
for using collections. Having a more lightweight backend that does not depend
on many nested criteria types.

It's designed with simplicity and usability as a main focus, so content editors
and site managers can create complex search queries with ease.

Changelog
=========

1.2.6 (2018-02-04)
------------------

Bug fixes:

- Removed dependency on CMFQuickInstallerTool.  [maurits]


1.2.5 (2017-11-24)
------------------

Bug fixes:

- Hide uninstall from install screens.
  [jensens]


1.2.4 (2017-06-03)
------------------

Bug fixes:

- removed unittest2 dependency
  [kakshay21]

1.2.3 (2016-11-18)
------------------

Bug fixes:

- Add coding header to python files.
  [gforcada]

- Remove superfluos dependency on zope.formlib
  [jensens]


1.2.2 (2016-09-16)
------------------

Bug fixes:

- Fix summary view for results with Discussion Items
  [ichim-david]

- Check with getattr if item isPrincipiaFolderish as Comment does
  not have this attribute which would render an AttributeError
  [ichim-david]


1.2.1 (2016-08-15)
------------------

Bug fixes:

- Use zope.interface decorator.
  [gforcada]


1.2.0 (2016-05-18)
------------------

New:

- Added uninstall profile.  The Collection type is removed when you
  uninstall this package.  [maurits]


1.1.6 (2016-02-27)
------------------

Fixes:

- Fix test isolation problems.
  [gforcada]


1.1.5 (2016-02-11)
------------------

Fixes:

- Remove existing type information object (FTI) from portal_types when
  installing.  This might be a dexterity FTI, which would give an
  error when installing: ValueError: undefined property
  ``content_meta_type``.  [maurits]

- Pull typesUseViewActionInListings value from portal_registry.
  [esteele]


1.1.4 (2015-06-05)
------------------

- Remove plone.app.form dependency.
  [timo]


1.1.3 (2015-03-11)
------------------

- Read ``allow_anon_views_about`` setting from the registry, with fallback to
  portal properties (see https://github.com/plone/Products.CMFPlone/issues/216)
  [jcerjak]

- Support for import and export of collections using FTP, DAV and GenericSetup
  [matthewwilkes]


1.1.2 (2014-10-23)
------------------

- Add a ``custom_query`` parameter to the ``Collection`` class' ``results`` and
  ``queryCatalog`` methods, and pass it over to ``QueryField``. The
  ``custom_query`` parameter allows for run time customization of the stored
  query. This can be done for example by views using the ``contentFilter``
  dictionary, which can be build from request parameters.  custom_query as well
  as contentFilter are dictionaries of index names and their associated query
  values.
  [thet]


1.1.1 (2014-03-29)
------------------

- Make sure Products.ATContentTypes is installed when running the tests, so
  tests pass for Plone 5 as well.
  [timo]


1.1.0 (2014-02-22)
------------------

- Install Products.ATContentTypes on the test fixture because Plone 5 does
  not install ATContentTypes automatically any longer.
  [timo]

- Declare dependency on plone.app.querystring.
  [davisagli]

- Add dependency on plone.app.widgets and run the install steps. Also run
  import steps for plone.app.querystring, needed for the registry data to be
  there.
  [frapell]

- Remove archetypes.querywidget from the dependencies and bring the field it
  provides to this package.
  [frapell]


1.0.11 (2013-08-13)
-------------------

- Add CSS classes on tabular_view table headers and cells
  in order to easily customize them.
  [avoinea]

- Use 'structure value' for tabular_view field value in order to easily
  insert images, links or other HTML entities in this table
  [avoinea]


1.0.10 (2013-05-23)
-------------------

- Fix tabular view to show append /view onto files and images
  [vangheem]


1.0.9 (2013-04-06)
------------------

- Provide /RSS view for collection so we at least have an option
  for syndication before 4.3
  [vangheem]


1.0.8 (2013-03-05)
------------------

- fix album view if item does not have images
  [vangheem]


1.0.7 (2012-12-14)
------------------

- Check if item isPrincipiaFolderish instead of the hardcoded portal_type
  Folder when searching for images
  [ichimdav]

- Fix thumbnail_view so it works with any portal_atct image types not just
  with Image and News Items
  [ichimdav]

- properly show dates on tabular view, fixes #12907
  [maartenkling]


1.0.6 (2012-09-21)
------------------

- Avoid site error on thumbnail view if some scale generation have failed.
  [thomasdesvenain]

- Avoid site error on summary view if some scale generation have failed.
  [kroman0]

- Provide a synContentValues method for compatibility with syndication
  in Plone <= 4.2.
  [davisagli]

- Added a validator 'isInt' to field limit for the purpose avoid a exception
  [hersonrodrigues]

- Fix the limit of number of items to show in batch results
  see https://dev.plone.org/ticket/13129 [hersonrodrigues]

- Implement ISyndicatable for 4.3
  [vangheem]


1.0.5 (2012-08-27)
------------------

- Add an alias folder_summary_view pointing to summary_view. This allows
  existing installs to display results for news/aggregator and
  events/aggregator see http://dev.plone.org/ticket/13010 [ericof]

- Fix summary_view so shows thumbnails for contents with the image field,
  see http://dev.plone.org/ticket/13010 [ericof]

- Fix thumbnail_view so it works when Images or News Items are listed,
  see http://dev.plone.org/ticket/13010 [ericof]


1.0.4 (2012-06-08)
------------------

- Fix an ommission that prevented sorting from working.
  [erral]

- accessibility improvements for screen readers regarding "more" links,
  see http://dev.plone.org/ticket/11982
  [rmattb, applied by polyester and par117]


1.0.3 (2012-04-15)
------------------

- Remove the portlet, which duplicates functionality from
  plone.portlet.collection. The Assignment class is kept for
  backwards-compatibility.
  [davisagli]

- Support a 'queryCatalog' method for backwards-compatibility with ATTopic.
  [davisagli]

- Only display the batch navigation in tabular_view if there are items to
  display.
  [esteele]


1.0.2 (2012-02-09)
------------------

- Modified the description of the query field.
  [vincentfretin]


1.0.1 (2011-11-24)
------------------

- Fix i18n of query widget.
  [vincentfretin]


1.0 - (2011-07-19)
------------------

- Initial release

- Add MANIFEST.in.
  [WouterVH]


