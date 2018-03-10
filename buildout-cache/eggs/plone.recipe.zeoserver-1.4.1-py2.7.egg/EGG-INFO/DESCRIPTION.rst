Overview
========

This recipe creates and configures a ZEO server in parts. It also installs a
control script in the bin/ directory. The name of the control script is the
name of the part in buildout.

You can use it with a part like this::

  [zeo]
  recipe = plone.recipe.zeoserver
  zeo-address = 8100

This will create a control script ``bin/zeo``.

You can either start the database in foreground mode via ``bin/zeo fg`` or use
the built-in zdaemon process control and use the ``start/stop/restart/status``
commands. The foreground mode is suitable for running the process under general
process control software like supervisord.

Note: Windows support for this recipe is currently limited.

Options
-------

The following options all affect the generated zeo.conf. If you want to have
full control over the configuration file, see the ``zeo-conf`` option in the
advanced options.

Process
-------

zeo-address
  Give a port for the ZEO server (either specify the port number only (with
  '127.0.0.1' as default) or you use the format ``host:port``).
  Defaults to ``8100``.

effective-user
  The name of the effective user for the ZEO process. Defaults to not setting
  an effective user. This causes the process to run under the user account the
  process has been started with.

socket-name
  The filename where ZEO will write its socket file.
  Defaults to ``var/zeo.zdsock``.

Storage
-------

storage-number
  The number used to identify a storage. Defaults to ``1``.

file-storage
  The filename where the ZODB data file will be stored.
  Defaults to ``var/filestorage/Data.fs``.

blob-storage
  The folder where the ZODB blob data files will be stored.
  Defaults to ``var/blobstorage``.

Logging
-------

zeo-log
  The filename of the ZEO log file. Defaults to ``var/log/${partname}.log``.

zeo-log-level
  Control the logging level in the eventlog. Defaults to ``info``.

zeo-log-max-size
  Maximum size of ZEO log file. Enables log rotation.

zeo-log-old-files
  Number of previous log files to retain when log rotation is enabled. Defaults to ``1``.

zeo-log-format
  Format of logfile entries. Defaults to ``%(asctime)s %(message)s``.

zeo-log-custom
  A custom section for the eventlog, to be able to use another
  event logger than ``logfile``. ``zeo-log`` is still used to set the logfile
  value in the runner section.

Authentication
--------------

authentication-database
  The filename for a authentication database. Only accounts listed in this
  database will be allowed to access the ZEO server.

  The format of the database file is::

    realm <realm>
    <username>:<hash>

  Where the hash is generated via::

    import sha
    string = "%s:%s:%s" % (username, realm, password)
    sha.new(string).hexdigest()

authentication-realm
  The authentication realm. Defaults to ``ZEO``.

Packing
-------

pack-days
  How many days of history should the zeopack script retain. Defaults to
  one day.

pack-gc
  Can be set to ``false`` to disable garbage collection as part of the pack.
  Defaults to ``true``.

pack-keep-old
  Can be set to ``false`` to disable the creation of ``*.fs.old`` files before
  the pack is run. Defaults to ``true``.

pack-user
  If the ZEO server uses authentication, this is the username used by the
  zeopack script to connect to the ZEO server.

pack-password
  If the ZEO server uses authentication, this is the password used by the
  zeopack script to connect to the ZEO server.


ZRS
---

First off, you'll need to specify the recipe to install zc.zrs. To do so,
just slightly change the way the recipe option is specified in your zeoserver
buildout part::

    [zeoserver]
    recipe = plone.recipe.zeoserver[zrs]
    ...


replicate-to
    host:port combination this ZRS should liston to as a primary.
    ZRS Secondaries connect here to get replication data.

replicate-from
    host:port combination of a ZRS primary this ZRS should connect to as a secondary.
    This ZRS replicates the data it gets from the primary.

keep-alive-delay
    In some network configurations, TCP connections are broken after extended
    periods of inactivity. This may even be done in a way that a client doesn't
    detect the disconnection. To prevent this, you can use the keep-alive-delay
    option to cause the secondary storage to send periodic no-operation
    messages to the server.


Monitoring
----------

monitor-address
  The address at which the monitor server should listen. The monitor server
  provides server statistics in a simple text format.

Performance
-----------

invalidation-queue-size
  The invalidation-queue-size used for the ZEO server. Defaults to ``100``.

Customization
-------------

var
  Used to configure the base directory for all things going into var.
  Defaults to ${buildout:directory}/var.

zeo-conf-additional
  Give additional lines to zeo.conf. Make sure you indent any lines after
  the one with the parameter. This allows you to use generated zeo.conf file
  but add some minor additional lines to it.

eggs
  Set if you need to include other packages as eggs e.g. for making
  application code available on the ZEO server side for performing
  conflict resolution (through the _p_resolveConflict() handler).

extra-paths
  Specify additional directories which should be available to the control
  scripts. Use this only for non-eggified Python packages.

zeo-conf
  A relative or absolute path to a zeo.conf file. This lets you provide a
  completely custom configuration file and ignore most of the options in
  this recipe.

repozo
  The path to the repozo.py backup script. A wrapper for this will be
  generated in bin/repozo, which sets up the appropriate environment for
  running this. Defaults to using the repozo script from the ZODB3 egg.
  Set this to an empty value if you do not want this script to be generated.

repozo-script-name
  The name of the wrapper script to generate in `bin/`. Defaults to `repozo`.
  Change this option if you have more than one instance of this recipe in
  the one buildout to create separate scripts and avoid any one script being
  overwritten.

zeopack
  The path to the zeopack.py backup script. A wrapper for this will be
  generated in bin/zeopack (unless you change `zeopack-script-name`), which
  sets up the appropriate environment to run this. Defaults to using the zeopack
  script from the ZODB3 egg.  Set this option to an empty value if you do not
  want this script to be generated.

zeopack-script-name
  The name of the wrapper script to generate in `bin/`. Defaults to `zeopack`.
  Change this option if you have more than one instance of this recipe in
  the one buildout to create separate scripts and avoid any one script being
  overwritten.

relative-paths
  Set this to `true` to make the generated scripts use relative
  paths. You can also enable this in the `[buildout]` section.

read-only
  Set zeoserver to run in read-only mode


Usage
-----

zeopack
  A zeopack script will be generated for you in the buildout bin directory,
  unless you change the `zeopack-script-name` option, in which case the script
  will be called the name you specify. If you'd like to use this script to pack
  a different mount point, you'll need to specify `-S mount_name`. You can also
  specify a `-B` option to not use the default blob directory.
  You may override the pack-days by adding "-D #" to the command line where
  "#" is the number of days to keep.


Reporting bugs or asking questions
----------------------------------

We have a bugtracker and help desk on Github:
https://github.com/plone/plone.recipe.zeoserver/issues

Changelog
=========

1.4.1 (2018-02-05)
------------------

Bug fixes:

- Fixed Travis tests by installing the ``hyperlink`` package.  [maurits]

- Fixed zeopack script for ZEO >= 5 (backport from original ZEO's script) [mamico]


1.4.0 (2017-06-16)
------------------

New features:

- Requires zope.mkzeoistance > 4.0 in order to work cleanly with latest ZODB.
  [jensens]

Bug fixes:

- Cleanup: utf8 headers, isort, pep8.
  [jensens]


1.3.1 (2017-04-08)
------------------

Bug fixes:

- Fix tests to run with current Twisted version.


1.3 (2017-02-15)
----------------

New features:

- Add support for log rotation.
  [hvelarde]

Bug fixes:

- Typo in documentation. [ale-rt]


1.2.9 (2016-05-26)
------------------

Fixes:

- Updated documentation.  [mamico, gforcada]


1.2.8 (2015-04-18)
------------------

- Add default storage number in zeopack script
  [mamico]


1.2.7 (2015-01-05)
------------------

- Postpone computation of working set until recipe is ran
  [gotcha]

- Add support for initialization in main script.
  [mamico]

- Add support for Pip-installed Buildout
  [aclark]

- Add "-D" argument to zopepack options to allow override of pack days.
  [smcmahon]


1.2.6 (2013-06-04)
------------------

- add support for setting zeoserver as read only
  [vangheem]

- Add integration with ZRS
  [vangheem]


1.2.5 (2013-05-23)
------------------

- Nothing changed yet.


1.2.4 (2013-04-06)
------------------

- Adding ability to control output script name for repozo. Use the
  ``repozo-script-name`` option to change the script name.
  [do3cc]


1.2.3 (2012-10-03)
------------------

- Adding ability to control output script name for zeopack. Use the
  ``zeopack-script-name`` option to change the script name.
  [davidjb]

- Fix zeopack connection handling. The previous fix to abort after a failed
  connection attempt only worked by chance and caused zeopack to exit before
  the packing finished. Now failed connections are correctly detected and
  zeopack waits until the packing is finished.
  [gaudenz]

1.2.2 (2011-11-24)
------------------

- Fix custom zeo.conf support under windows.
  [rossp]


1.2.1 - 2011-09-12
------------------

- When the zeoserver is not running, the zeopack script cannot do
  anything.  So when zeopack cannot connect, it now quits with an
  error message.  Formerly it would wait forever.
  [maurits]

- Added 'var' option like it is in plone.recipe.zope2instance.
  [garbas]

1.2.0 - 2010-10-18
------------------

- Only require a ``nt_svcutils`` distribution on Windows.
  [hannosch]

1.1.1 - 2010-07-20
------------------

- Fixed -B option being required for along with the -S option.
  [vangheem]

- Added documentation for using the zeopack script with mount points.
  [vangheem]

1.1 - 2010-07-18
----------------

- No changes.

1.1b1 - 2010-07-02
------------------

- Implemented Windows support and support for running ZEO as a Windows service.
  We depend on the new nt_svcutils distribution to provide this support.
  [baijum, hannosch]

- The FileStorage component of ZODB 3.9 now supports blobs natively,
  so no need to use BlobStorage proxy for it anymore.
  [baijum, hannosch]

- Added ``extra-paths`` option to add additional modules paths.
  [baijum]

- Fixed ZEO packing of mounted storage.
  [vangheem]

- Added -B option to the ``zeopack`` script to specify the location of the
  blob storage.
  [vangheem]

1.1a2 - 2010-05-10
------------------

- Added support for the ``pack-keep-old`` option introduced in ZODB 3.9.
  [hannosch]

1.1a1 - 2010-04-27
------------------

- Added support for the ``pack-gc`` option introduced in ZODB 3.9.
  [hannosch]

- Always create a blob-storage by default.
  [hannosch]

- Require at least ZODB 3.8 and simplify the ``zeopack`` script.
  [hannosch]

- Various documentation updates.
  [hannosch]

- Use the new ``zope.mkzeoinstance`` package, which makes the recipe compatible
  with ZODB 3.9.5+.
  [hannosch]

- Removed unmaintained win32 specific tests and old zope2 test mockups.
  [hannosch]

- Removed testing dependency on ``zope.testing`` and refactored testing setup.
  [hannosch]

1.0 - 2010-04-05
----------------

- Depend on and always include ZopeUndo. While it's only needed for Zope 2, the
  distribution is so tiny, it doesn't hurt for non-Zope 2 ZEO servers.
  [hannosch]

1.0b1 - 2010-03-19
------------------

- Fixed issue with egg paths for the zeopack script.
  [davisagli]

- Added support for setting ZEO log level.
  [baijum]

1.0a2 - 2009-12-03
------------------

* Set up logging configuration that is needed by ZODB.blob.
  [davisagli]

* Set shared_blob_dir to True when initializing the ClientStorage used
  by the pack script, since it will be using the same blob directory
  as the ZEO server.
  [davisagli]

1.0a1 - 2009-12-03
------------------

* Updated and cleaned up after renaming.
  [hannosch]

* Added compatibility with eggified Zopes (Zope >= 2.12).
  [davisagli]

* Initial implementation based on plone.recipe.zope2zeoserver.
  [plone]


