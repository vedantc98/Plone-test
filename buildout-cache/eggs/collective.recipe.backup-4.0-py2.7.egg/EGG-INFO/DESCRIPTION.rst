Easy Zope backup/restore recipe for buildout
********************************************

.. image:: https://travis-ci.org/collective/collective.recipe.backup.png
    :target: https://travis-ci.org/collective/collective.recipe.backup

.. contents::


Introduction
============

This recipe is mostly a wrapper around the ``bin/repozo`` script in
your Zope buildout.  It requires that this script is already made
available.  If this is not the case, you will get an error like this
when you run one of the scripts: ``bin/repozo: No such file or
directory``.  You should be fine when you are on Plone 3 or when you
are on Plone 4 and are using ``plone.recipe.zeoserver``.  If this is
not the case, the easiest way of getting a ``bin/repozo`` script is to
add a new section in your ``buildout.cfg`` (do not forget to add it in the
``parts`` directive)::

  [repozo]
  recipe = zc.recipe.egg
  eggs = ZODB
  # or this for an older version:
  # eggs = ZODB3
  scripts = repozo
  dependent-scripts = true

``bin/repozo`` is a Zope script to make backups of your ``Data.fs``.
Looking up the settings can be a chore. And you have to pick a
directory where to put the backups. This recipe provides **sensible
defaults** for your common backup tasks. Making backups a piece of
cake is important!

- ``bin/backup`` makes an incremental backup.

- ``bin/fullbackup`` always makes a full backup, in the same directory
  as the normal backups.  You can enable this by setting the
  ``enable_fullbackup`` option to true.

- ``bin/restore`` restores the latest backup, created by the backup or
  fullbackup script.

- ``bin/snapshotbackup`` makes a full snapshot backup, separate from the
  regular backups. Handy right before a big change in the site.

- ``bin/snapshotrestore`` restores the latest full snapshot backup.

- ``bin/zipbackup`` makes a zip backup.  This zips the Data.fs and the
  blobstorage, handy for copying production data to your local
  machine, especially the blobstorage with its many files.  *Note*:
  the Data.fs and blobstorage (or other storages) are *not* combined
  in one file; you need to download multiple files.  Enable this
  script by using the ``enable_zipbackup`` option.

- ``bin/ziprestore`` restores the latest zipbackup.


Compatibility
=============

The recipe is tested with Python 2.6, 2.7, and 3.6.
In Plone terms it works fine on Plone 4 and 5.

Note that the integration with ``plone.recipe.zope2instance`` is not tested on Python 3.6.
There is not yet a Python 3 compatible version of this recipe and its ``mailinglogger`` dependency.


Development
===========

- Code repository: https://github.com/collective/collective.recipe.backup

- Issue tracker: https://github.com/collective/collective.recipe.backup/issues

- Obvious fixes, like fixing typos, are fine on master.
  For larger changes or if you are unsure, please create a branch or a pull request.

- The code comes with a ``buildout.cfg``.  Please bootstrap the
  buildout and run the created ``bin/test`` to see if the tests still
  pass.  Please try to add tests if you add code.

- The long description of this package (as shown on PyPI), used to
  contain a big file with lots of test code that showed how to use the
  recipe.  This grew too large, so we left it out.  It is probably
  still good reading if you are wondering about the effect some
  options have.  See ``src/collective/recipe/backup/tests/*.txt``.

- We are tested on Travis:
  https://travis-ci.org/collective/collective.recipe.backup

- Questions and comments to https://community.plone.org or to
  `Maurits van Rees <mailto:maurits@vanrees.org>`_.


Example usage
=============

The simplest way to use this recipe is to add a part in ``buildout.cfg`` like this::

    [buildout]
    parts = backup

    [backup]
    recipe = collective.recipe.backup

You can set lots of extra options, but the recipe authors like to
think they have created sane defaults, so this single line stating the
recipe name should be enough in most cases.

Running the buildout adds the ``backup``, ``fullbackup``,
``snapshotbackup``, ``zipbackup``, ``restore``, ``snapshotrestore``
and ``ziprestore`` scripts to the ``bin/`` directory of the buildout.
Some are not added by default, others can be switched off.


Backed up data
==============

Which data does this recipe backup?

- The Zope Object DataBase (ZODB) filestorage, by default located at
  ``var/filestorage/Data.fs``.

- Possibly additional filestorages, see the
  ``additional_filestorages`` option.

- The blobstorage (since version 2.0) if your buildout uses it, by
  default located at ``var/blobstorage``.


Data that is *not* backed up
============================

Which data does this recipe *not* backup?  Everything else of course,
but specifically:

- Data stored in ``RelStorage`` will *not* be backed up.  (You could
  still use this recipe to back up the filesystem blobstorage,
  possibly with the ``only_blobs`` option.)

- Other data stored in SQL, perhaps via SQLAlchemy, will *not* be
  backed up.

- It does *not* create a backup of your entire buildout directory.


Is your backup backed up?
=========================

Note that the backups are by default created in the ``var`` directory
of the buildout, so if you accidentally remove the entire buildout,
you also lose your backups.  It should be standard practice to use the
``location`` option to specify a backup location in for example the
home directory of the user.  You should also arrange to copy that
backup to a different machine/country/continent/planet.


Backup
======

Calling ``bin/backup`` results in a normal incremental repozo backup
that creates a backup of the ``Data.fs`` in ``var/backups``.  When you
have a blob storage it is by default backed up to
``var/blobstoragebackups``.


Full backup
===========

Calling ``bin/fullbackup`` results in a normal FULL repozo backup
that creates a backup of the ``Data.fs`` in ``var/backups``.  When you
have a blob storage it is by default backed up to
``var/blobstoragebackups``.  This script is provided so that you can
set different cron jobs for full and incremental backups.  You may
want to have incrementals done daily, with full backups done weekly.
Now you can!

Since version 4.0, the fullbackup script is not created by default.
Enable it by setting ``enable_fullbackup`` to ``true``

You should normally do a ``bin/zeopack`` regularly, say once a week,
to remove unused objects from your Zope ``Data.fs``.  The next time
``bin/backup`` is called, a complete fresh backup is made, because an
incremental backup is not possible anymore.  This is standard
``bin/repozo`` behaviour.  So you might not need the
``bin/fullbackup`` script.


Snapshots
=========

A quick backup just before updating the production server is a good
idea.  But you may not want to interfere with the regular backup
regime.  For that, the ``bin/snapshotbackup`` is great. It places a
full backup in, by default, ``var/snapshotbackups``.


Zipbackups
==========

For quickly grabbing the current state of a production database so you
can download it to your development laptop, you want a full and zipped
backup.  The zipped part is important for the blobstorage, because you
do not want to use ``scp`` to recursively copy over all those blob
files: downloading one tarball is faster.

You can use the ``bin/zipbackup`` script for this.  This script
overrides a few settings, ignoring whatever is set in the buildout
config section:

- ``gzip`` is explicitly turned on for the filestorage (this is
  already the default, but we make sure).

- ``archive_blob`` is turned on.

- ``keep`` is set to 1 to avoid keeping lots of needless backups.

- ``keep_blob_days`` is ignored because it is a full backup.

The script places a full backup in, by default, ``var/zipbackups`` and
it puts a tarball of the blobstorage in ``var/blobstoragezips``.

This script is not created by default.
You can enable it by setting the ``enable_zipbackup`` option to true.
Also, if ``backup_blobs`` is false, the scripts are useless, so we do not create them, even when you have enabled them explicitly.


Restore
=======

Calling ``bin/restore`` restores the very latest normal incremental
``repozo`` backup and restores the blobstorage if you have that.

You can restore the very latest snapshotbackup with ``bin/snapshotrestore``.

You can restore the zipbackup with ``bin/ziprestore``.

You can also restore the backup as of a certain date. Just pass a date argument.
According to ``repozo``: specify UTC (not local) time.
The format is ``yyyy-mm-dd[-hh[-mm[-ss]]]``.
So as a simple example, restore to 25 december 1972::

    bin/restore 1972-12-25

or to that same date, at 2,03 seconds past 1::

    bin/restore 1972-12-25-01-02-03

Since version 2.3 this also works for restoring blobs.
We restore the directory from the first backup at or before the specified date.
(Note that before version 4.0 we restored the directory from the first backup after the specified date,
which should be fine as long as you did not do a database pack in between.)

Since version 2.0, the restore scripts ask for confirmation before
starting the restore, as this is a potentially dangerous command.
("Oops, I have restored the live site but I meant to restore the test
site.")  You need to explicitly type 'yes'::

    This will replace the filestorage (Data.fs).
    This will replace the blobstorage.
    Are you sure? (yes/No)?

Note that for large filestorages and blobstorages **it may take long to restore**.
You should do a test restore and check how long it takes.
Seconds?  Minutes?  Hours?
Is that time acceptable or should you take other measures?

Names of created scripts
========================

A backup part will normally be called ``[backup]``, leading to a
``bin/backup`` and ``bin/snapshotbackup``.  Should you name your part
something else,  the script names will also be different, as will the created
``var/`` directories (since version 1.2)::

    [buildout]
    parts = plonebackup

    [plonebackup]
    recipe = collective.recipe.backup
    enable_zipbackup = true

That buildout snippet will create these scripts::

    bin/plonebackup
    bin/plonebackup-full
    bin/plonebackup-zip
    bin/plonebackup-snapshot
    bin/plonebackup-restore
    bin/plonebackup-ziprestore
    bin/plonebackup-snapshotrestore


Supported options
=================

The recipe supports the following options, none of which are needed by
default. The most common ones to change are ``location`` and
``blobbackuplocation``, as those allow you to place your backups in
some system-wide directory like ``/var/zopebackups/instancename/`` and
``/var/zopebackups/instancename-blobs/``.

.. Note: keep this in alphabetical order please.

``additional_filestorages``
    Advanced option, only needed when you have split for instance a
    ``catalog.fs`` out of the regular ``Data.fs``.
    Use it to specify the extra filestorages.
    (See `Advanced usage: multiple Data.fs files`_).

``archive_blob``
    Use ``tar`` archiving functionality. ``false`` by default. Set it to ``true``
    and backup/restore will be done with ``tar`` command. Note that ``tar``
    command must be available on machine if this option is set to ``true``.
    This option also works with snapshot backup/restore commands. As this
    counts as a full backup ``keep_blob_days`` is ignored.
    See the ``compress_blob`` option if you want to compress the archive.

``alternative_restore_sources``
    You can restore from an alternative source.  Use case: first make
    a backup of your production site, then go to the testing or
    staging server and restore the production data there.  See
    `Alternative restore sources`_

``backup_blobs``
    Backup the blob storage.  Default is ``True`` on Python 2.6 (Plone
    4) and higher, and ``False`` otherwise.  This requires the
    ``blob_storage`` location to be set.  If no ``blob_storage``
    location has been set and we cannot find one by looking in the
    other buildout parts, we quit with an error (since version 2.22).
    If ``backup_blobs`` is false, ``enable_zipbackup`` cannot be true,
    because the ``zipbackup`` script is not useful then.

``blob_storage``
    Location of the directory where the blobs (binary large objects)
    are stored.  This is used in Plone 4 and higher, or on Plone 3 if
    you use ``plone.app.blob``.  This option is ignored if backup_blobs is
    ``false``.  The location is not set by default.  When there is a part
    using ``plone.recipe.zeoserver``, ``plone.recipe.zope2instance`` or
    ``plone.recipe.zope2zeoserver``, we check if that has a
    blob-storage option and use that as default.  Note that we pick
    the first one that has this option and we do not care about
    shared-blob settings, so there are probably corner cases where we
    do not make the best decision here.  Use this option to override
    it in that case.

``blob-storage``
    Alternative spelling for the preferred ``blob_storage``, as
    ``plone.recipe.zope2instance`` spells it as ``blob-storage`` and we are
    using underscores in all the other options.  Pick one.

``blob_timestamps``
    New in version 4.0.  Default is false.
    By default we create ``blobstorage.0``.
    The next time, we rotate this to ``blobstorage.1`` and create a new ``blobstorage.0``.
    With ``blob_timestamps = true``, we create stable directories that we do not rotate.
    They get a timestamp, the same timestamp that the ZODB filestorage backup gets.
    For example: ``blobstorage.1972-12-25-01-02-03``.
    Or with ``archive_blob = true``: ``blobstorage.1972-12-25-01-02-03.tar.gz``.

``blobbackuplocation``
    Directory where the blob storage will be backed up to.  Defaults
    to ``var/blobstoragebackups`` inside the buildout directory.

``blobsnapshotlocation``
    Directory where the blob storage snapshots will be created.
    Defaults to ``var/blobstoragesnapshots`` inside the buildout
    directory.

``blobziplocation``
    Directory where the blob storage zipbackups will be created.
    Defaults to ``var/blobstoragezips`` inside the buildout
    directory.

``compress_blob``
    New in version 4.0.  Default is false.
    This is only used when the ``archive_blob`` option is true.
    When switched on, it will compress the archive,
    resulting in a ``.tar.gz`` instead of a ``tar`` file.
    When restoring, we always look for both compressed and normal archives.
    We used to always compress them, but in most cases it hardly decreases the size
    and it takes a long time anyway.  I have seen archiving take 15 seconds,
    and compressing take an additional 45 seconds.
    The result was an archive of 5.0 GB instead of 5.1 GB.

``datafs``
    In case the ``Data.fs`` isn't in the default ``var/filestorage/Data.fs``
    location, this option can overwrite it.

``debug``
    In rare cases when you want to know exactly what's going on, set debug to
    ``true`` to get debug level logging of the recipe itself. ``repozo`` is also run
    with ``--verbose`` if this option is enabled.

``enable_fullbackup``
    Create ``fullbackup`` script.  Default: false (changed in 4.0).

``enable_snapshotrestore``
    Having a ``snapshotrestore`` script is very useful in development
    environments, but can be harmful in a production buildout. The
    script restores the latest snapshot directly to your filestorage
    and it used to do this without asking any questions whatsoever
    (this has been changed to require an explicit ``yes`` as answer).
    If you don't want a ``snapshotrestore`` script, set this option to false.

``enable_zipbackup``
    Create ``zipbackup`` and ``ziprestore`` scripts.  Default: false.
    If ``backup_blobs`` is not on, these scripts are always disabled,
    because they are not useful then.

``full``
    By default, incremental backups are made. If this option is set to ``true``,
    ``bin/backup`` will always make a full backup.  This option is (obviously)
    the default when using the ``fullbackup`` script.

``gzip``
    Use repozo's zipping functionality. ``true`` by default. Set it to ``false``
    and repozo will not gzip its files. Note that gzipped databases are called
    ``*.fsz``, not ``*.fs.gz``. **Changed in 0.8**: the default used to be
    false, but it so totally makes sense to gzip your backups that we changed
    the default.

``gzip_blob``
    Backwards compatibility alias for ``archive_blob`` option.

``incremental_blobs``
    New in version 4.0.  Default is false.
    When switched on, it will use the ``--listed-incremental`` option of ``tar``.
    Note: this only works with the GNU version of ``tar``.
    It will create a metadata or `snapshot file <https://www.gnu.org/software/tar/manual/html_node/Incremental-Dumps.html>`_
    so that a second call to the backup script will create a second tarball with only the differences.
    For some reason, all directories always end up in the second tarball,
    even when there are no changes; this may depend on the used file system.
    This option is ignored when the ``archive_blob`` option is false.
    This option *requires* the ``blob_timestamps`` option to be true,
    because it needs the tarball names to be stable, instead of getting rotated.
    If you have explicitly set ``blob_timestamps`` to false, buildout will exit with an error.
    For large blobstorages it may take long to restore, so do test it out.
    But that is wise in all cases.
    Essentially, this feature seems to trade off storage space reduction with restore time.

``keep``
    Number of full backups to keep. Defaults to ``2``, which means that the
    current and the previous full backup are kept. Older backups are removed,
    including their incremental backups. Set it to ``0`` to keep all backups.

``keep_blob_days``
    Number of *days* of blob backups to keep.  Defaults to ``14``, so
    two weeks.  This is **only** used for partial (full=False)
    backups, so this is what gets used normally when you do a
    ``bin/backup``.  This option has been added in 2.2.  For full
    backups (snapshots) we just use the ``keep`` option.  Recommended
    is to keep these values in sync with how often you do a ``zeopack`` on
    the ``Data.fs``, according to the formula ``keep *
    days_between_zeopacks = keep_blob_days``.  The default matches one
    zeopack per seven days (``2*7=14``).
    Since version 4.0, this option is ignored unless ``only_blobs`` is true.
    Instead, we remove the blob backups that have no matching filestorage backup.

``location``
    Location where backups are stored. Defaults to ``var/backups`` inside the
    buildout directory.

``locationprefix``
    Location of the folder where all other backup and snapshot folders will
    be created. Defaults to ``var/``.
    Note that this does not influence where we look for a source filestorage or blobstorage.

``only_blobs``
    Only backup the blobstorage, not the ``Data.fs`` filestorage.  False
    by default.  May be a useful option if for example you want to
    create one ``bin/filestoragebackup`` script and one
    ``bin/blobstoragebackup`` script, using ``only_blobs`` in one and
    ``backup_blobs`` in the other.

``post_command``
    Command to execute after the backup has finished.  One use case
    would be to unmount the remote file system that you mounted
    earlier using the ``pre_command``.  See that ``pre_command`` above for
    more info.

``pre_command``
    Command to execute before starting the backup.  One use case would
    be to mount a remote file system using NFS or sshfs and put the
    backup there.  Any output will be printed.  If you do not like
    that, you can always redirect output somewhere else (``mycommand >
    /dev/null`` on Unix).  Refer to your local Unix guru for more
    information.  If the command fails, the backup script quits with
    an error.  You can specify multiple commands.

``quick``
    Call ``repozo`` with the ``--quick`` option.  This option was
    introduced to ``collective.recipe.backup`` in version 2.19, with
    **default value true**.  Due to all the checksums that the repozo
    default non-quick behavior does, an amount of data is read that is
    three to four times as much as is in the actual filestorage.  With
    the quick option it could easily be just a few kilobytes.
    Theoretically the quick option is less safe, but it looks like it
    can only go wrong when someone edits the ``.dat`` file in the
    repository or removes a ``.deltafs`` file.

    The ``quick`` option only influences the created ``bin/backup``
    script.  It has no effect on the snapshot or restore scripts.

    The repozo help says about this option: "Verify via md5 checksum
    only the last incremental written.  This significantly reduces the
    disk i/o at the (theoretical) cost of inconsistency.  This is a
    probabilistic way of determining whether a full backup is
    necessary."

``rsync_options``
    Add extra options to the default ``rsync -a`` command. Default is no
    extra parameters. This can be useful for example when you want to restore
    a backup from a symlinked directory, in which case
    ``rsync_options = --no-l -k`` does the trick.

``snapshotlocation``
    Location where snapshot backups of the filestorage are stored. Defaults to
    ``var/snapshotbackups`` inside the buildout directory.

``use_rsync``
    Use ``rsync`` with hard links for backing up the blobs.  Default is
    true.  ``rsync`` is probably not available on all machines though, and
    I guess hard links will not work on Windows.  When you set this to
    false, we fall back to a simple copy (``shutil.copytree`` from
    Python in fact).

``ziplocation``
    Location where zip backups of the filestorage are stored. Defaults to
    ``var/zipbackups`` inside the buildout directory.


An example buildout snippet using various options, would look like this::

    [backup]
    recipe = collective.recipe.backup
    location = ${buildout:directory}/myproject
    keep = 2
    datafs = subfolder/myproject.fs
    full = true
    debug = true
    snapshotlocation = snap/my
    gzip = false
    enable_snapshotrestore = true
    pre_command = echo 'Can I have a backup?'
    post_command =
        echo 'Thanks a lot for the backup.'
        echo 'We are done.'

Paths in directories or files can use relative (``../``) paths, and
``~`` (home dir) and ``$BACKUP``-style environment variables are
expanded.


Cron job integration
====================

``bin/backup`` is of course ideal to put in your cronjob instead of a whole
``bin/repozo ....`` line. But you don't want the "INFO" level logging that you
get, as you'll get that in your mailbox. In your cronjob, just add ``-q`` or
``--quiet``, and ``bin/backup`` will shut up unless there's a problem.
This option ignores the debug variable, if set to true in buildout.

Speaking of cron jobs?  Take a look at `zc.recipe.usercrontab
<http://pypi.python.org/pypi/z3c.recipe.usercrontab>`_ if you want to handle
cronjobs from within your buildout.  For example::

    [backupcronjob]
    recipe = z3c.recipe.usercrontab
    times = 0 12 * * *
    command = ${buildout:directory}/bin/backup


Advanced usage: multiple Data.fs files
======================================

Sometimes, a filestorage is split into several files. Most common reason is to
have a regular ``Data.fs`` and a ``catalog.fs`` which contains the
``portal_catalog``. This is supported with the ``additional_filestorages``
option::

    [backup]
    recipe = collective.recipe.backup
    additional_filestorages =
        catalog
        another

This means that, with the standard ``Data.fs``, the ``bin/backup``
script will now backup three filestorages::

    var/filestorage/Data.fs
    var/filestorage/catalog.fs
    var/filestorage/another.fs

The additional backups have to be stored separate from the ``Data.fs``
backup. That's done by appending the file's name and creating extra backup
directories named that way::

    var/backups_catalog
    var/snapshotbackups_catalog
    var/backups_another
    var/snapshotbackups_another

The various backups are done one after the other. They cannot be done at the
same time with ``repozo``. So they are not completely in sync. The "other"
databases are backed up first as a small difference in the catalog is just
mildly irritating, but the other way around users can get real errors.

In the ``additional_filestorages`` option you can define different
filestorages using this syntax::

    additional_filestorages =
        storagename1 [datafs1_path [blobdir1]]
        storagename2 [datafs2_path [blobdir2]]
        ...

So if you want more control over the filestorage source path, you can
explicitly set it, with or without the blobstorage path.  For
example::

    [backup]
    recipe = collective.recipe.backup
    additional_filestorages =
        foo ${buildout:directory}/var/filestorage/foo/foo.fs ${buildout:directory}/var/blobstorage-foo
        bar ${buildout:directory}/var/filestorage/bar/bar.fs

If the ``datafs_path`` is missing, then the default value will be used
(``var/filestorage/storagename1.fs``).  If you do not specify a
``blobdir``, then this means no blobs will be backed up for that
storage.  Note that if you specify ``blobdir`` you must specify
``datafs_path`` as well.

Note that ``collective.recipe.filestorage`` creates additional
filestorages in a slightly different location, but you can explictly define the
paths of filestorage and blobstorage for all the ``parts`` defined in the recipe.
Work is in progress to improve this.


Blob storage
============

Added in version 2.0.

We can backup the blob storage.  Plone 4 uses a blob storage to store
files (Binary Large OBjects) on the file system.  In Plone 3 this is
optional.  When this is used, it should be backed up of course.  You
must specify the source blob_storage directory where Plone (or Zope)
stores its blobs.  As indicated earlier, when we do not set it
specifically, we try to get the location from other parts, for example
the ``plone.recipe.zope2instance`` recipe::

    [buildout]
    parts = instance backup

    [instance]
    recipe = plone.recipe.zope2instance
    user = admin:admin
    blob-storage = ${buildout:directory}/var/somewhere

    [backup]
    recipe = collective.recipe.backup

If needed, we can tell buildout that we *only* want to backup blobs or
specifically do *not* want to backup the blobs.  Specifying this using
the ``backup_blobs`` and ``only_blobs`` options might be useful in
case you want to separate this into several scripts::

    [buildout]
    newest = false
    parts = filebackup blobbackup

    [filebackup]
    recipe = collective.recipe.backup
    backup_blobs = false

    [blobbackup]
    recipe = collective.recipe.backup
    blob_storage = ${buildout:directory}/var/blobstorage
    only_blobs = true

With this setup ``bin/filebackup`` now only backs up the filestorage
and ``bin/blobbackup`` only backs up the blobstorage.

New in version 4.0: you may want to specify ``blob_timestamps = true``.
Then we create stable directories that we do not rotate.
For example: ``blobstorage.1972-12-25-01-02-03`` instead of ``blobstorage.0``.


rsync
=====

By default we use ``rsync`` to create backups.  We create hard links
with this tool, to save disk space and still have incremental backups.
This probably requires a unixy (Linux, Mac OS X) operating system.
It is based on this article by Mike Rubel:
http://www.mikerubel.org/computers/rsync_snapshots/

We have not tried this on Windows.  Reports are welcome, but best is
probably to set the ``use_rsync = false`` option in the backup part.
Then we simply copy the blobstorage directory.


Alternative restore sources
===========================

Added in version 2.17.

You can restore from an alternative source.  Use case: first make a
backup of your production site, then go to the testing or staging
server and restore the production data there.

In the ``alternative_restore_sources`` option you can define different
filestorage and blobstorage backup source directories using this
syntax::

    alternative_restore_sources =
        storagename1 datafs1_backup [blobdir1_backup]
        storagename2 datafs2_backup [blobdir2_backup]
        ...

The storagenames *must* be the same as in the additional_filestorages
option, plus a key ``Data`` (or ``1``) for the standard ``Data.fs``
and optionally its blobstorage.

The result is a ``bin/altrestore`` script.

This will work for a standard buildout with a single filestorage and
blobstorage::

    [backup]
    recipe = collective.recipe.backup
    alternative_restore_sources =
        Data /path/to/production/var/backups /path/to/production/var/blobstoragebackups

The above configuration uses ``repozo`` to restore the Data.fs from
the ``/path/to/production/var/backups`` repository to the standard
``var/filestorage/Data.fs`` location.  It copies the most recent
blobstorage backup from
``/path/to/production/var/blobstoragebackups/`` to the standard
``var/blobstorage`` location.

Calling the script with a specific date is supported just like the
normal restore script::

    bin/altrestore 2000-12-31-23-59

If you have additional filestorages, it would be like this::

    [backup]
    recipe = collective.recipe.backup
    additional_filestorages =
        foo ${buildout:directory}/var/filestorage/foo/foo.fs ${buildout:directory}/var/blobstorage-foo
        bar ${buildout:directory}/var/filestorage/bar/bar.fs
    alternative_restore_sources =
        Data /path/to/production/var/backups /path/to/production/var/blobstoragebackups
        foo /path/to/production/var/backups_foo /path/to/production/var/blobstoragebackups_foo
        bar /path/to/production/var/backups_bar

The recipe will fail if the alternative sources do not match the
standard filestorage, blobstorage and additional storages.  For
example, you get an error when the ``alternative_restore_sources`` is
missing the ``Data`` key, when it has extra or missing keys, when a
key has no paths, when a key has an extra or missing blobstorage.

During install of the recipe, so during the ``bin/buildout`` run, it
does not check if the sources exist: you might have the production
backups on a different server and need to setup a remote shared
directory, or you copy the data over manually.

Note that the script takes the ``archive_blob`` and ``use_rsync`` options
into account.  So if the alternative restore source contains a blob
backup that was made with ``archive_blob = true``, you need an
``altrestore`` script that also uses this setting.

Contributors
************

collective.recipe.backup is basically a port of ye olde instancemanager_'s
backup functionality. That backup functionality was coded mostly by Reinout
van Rees and Maurits van Rees, both from `Zest software`_

Creating the buildout recipe was done by Reinout_ with some fixes by Maurits_, who is now the main developer and maintainer.

The snapshotrestore script was added by Nejc Zupan (niteoweb_).

The fullbackup script was added by `Tom 'Spanky' Kapanka`_.

Archive blob backups feature added by `Matej Cotman`_ (niteoweb_).


Sponsorship
===========

Work on collective.recipe.backup has been made possible by Ghent University, or UGent.
See https://www.ugent.be.
Ghent University is a top 100 university and one of the major universities in Belgium.

.. Links used above.

.. _Zest software: http://zestsoftware.nl/

.. _Reinout: http://reinout.vanrees.org/

.. _Maurits: http://maurits.vanrees.org/

.. _instancemanager: https://pypi.python.org/pypi/instancemanager

.. _`Tom 'Spanky' Kapanka`: https://github.com/spanktar

.. _`Sylvain Bouchard`: https://github.com/bouchardsyl

.. _`Matej Cotman`: https://github.com/matejc

.. _niteoweb: http://www.niteoweb.com

Change history
**************

4.0 (2017-12-22)
================

- Updated readme and added sponsorship note.  [maurits]


4.0b5 (2017-11-17)
==================

- Added ``incremental_blobs`` option.
  This creates tarballs with only the changes compared to the previous blob backups.
  This option is ignored when the ``archive_blob`` option is false.
  [maurits]

- Improved code quality, reducing complexity.  [maurits]

- Refactored the main functions to not have so much code duplication.
  The normal, full, snapshot and zip backups had almost the same code.
  This made it hard to add new options.
  [maurits]


4.0b4 (2017-08-18)
==================

- Test Python 3.6 (and 2.6 and 2.7) on Travis from now on.  [maurits]

- Ignore the zope2instance recipe integration tests on Python 3.
  They would need a compatible ``mailinglogger`` package.
  See `issue #31 <https://github.com/collective/collective.recipe.backup/issues/31>`_. [maurits]

- Tests: use cleaner way to check the mock repozo output.
  Share this setup between tests.
  This makes the output order the same on Python 2 and 3.
  See `issue #31 <https://github.com/collective/collective.recipe.backup/issues/31>`_. [maurits]


4.0b3 (2017-07-05)
==================

- Added basic Python 3 support.  We do not test with it yet,
  but you should not get NameErrors anymore.
  See `issue #31 <https://github.com/collective/collective.recipe.backup/issues/31>`_. [maurits]


4.0b2 (2017-06-26)
==================

- No longer create the ``fullbackup`` script by default.
  You can still enable it by setting ``enable_fullbackup`` to ``true``.
  [maurits]

- Without explicit ``blob-storage`` option, default to ``var/blobstorage``.
  Take the ``var`` option from zeoserver/client recipes into account.
  Fixes `issue #27 <https://github.com/collective/collective.recipe.backup/issues/27>`_.
  [maurits]

- Do not create hidden backup ``.0`` when blob_storage ends with a slash.
  Fixes `issue #26 <https://github.com/collective/collective.recipe.backup/issues/26>`_.
  [maurits]


4.0b1 (2017-05-31)
==================

- Make custom backup locations relative to the ``locationprefix`` option or the ``var`` directory.
  Until now, the ``locationprefix`` option was only used if you did not set custom locations.
  Custom location would be relative to the buildout directory.
  Now they are relative to the ``locationprefix`` option, with the ``var`` directory as default.
  So if you used a relative path, your backups may end up in a different path.
  Absolute paths are not affected: they ignore the locationprefix.
  [maurits]

- When log level is DEBUG, show time stamps in the log.  [maurits]

- Added ``compress_blob`` option.  Default is false.
  This is only used when the ``archive_blob`` option is true.
  When switched on, it will compress the archive,
  resulting in a ``.tar.gz`` instead of a ``tar`` file.
  When restoring, we always look for both compressed and normal archives.
  We used to always compress them, but in most cases it hardly decreases the size
  and it takes a long time anyway.  I have seen archiving take 15 seconds,
  and compressing take an additional 45 seconds.
  The result was an archive of 5.0 GB instead of 5.1 GB.
  [maurits]

- Renamed ``gzip_blob`` option to ``archive_blob``.
  Kept the old name as alias for backwards compatibility.
  This makes room for letting this create an archive without zipping it.
  [maurits]

- Automatically remove old blobs backups that have no corresponding filestorage backup.
  We compare the timestamp of the oldest filestorage backup with the timestamps of the
  blob backups.  This can be the name, if you use ``blob_timestamps = true``,
  or the modification date of the blob backup.
  This means that the ``keep_blob_days`` option is ignored, unless you use ``only_blobs = true``.
  [maurits]

- When backing up a blobstorage, use the timestamp of the latest filestorage backup.
  If a blob backup with that name is already there, then there were no database changes,
  so we do not make a backup.
  This is only done when you use the new ``blob_timestamps = true`` option.
  [maurits]

- When restoring to a specific date, find the first blob backup at or before
  the specified date.  Otherwise fail.  The repozo script does the same.
  We used to pick the first blob backup *after* the specified date,
  because we assumed that the user would specify the exact date that is
  in the filestorage backup.
  Note that the timestamp of the filestorage and blobstorage backups may be
  a few seconds apart, unless you use the ``blob_timestamps == true`` option.
  In the new situation, the user should pick the date of the blob backup
  or slightly later.
  [maurits]

- Added ``blob_timestamps`` option.  Default is false.
  By default we create ``blobstorage.0``.
  The next time, we rotate this to ``blobstorage.1`` and create a new ``blobstorage.0``.
  With ``blob_timestamps = true``, we create stable directories that we do not rotate.
  They get a timestamp, the same timestamp that the ZODB filestorage backup gets.
  For example: ``blobstorage.1972-12-25-01-02-03``.
  [maurits]

- When restoring, first run checks for all filestorages and blobstorages.
  When one of the backups is missing, we quit with an error.
  This avoids restoring a filestorage and then getting into trouble
  due to a missing blobstorage backup.  [maurits]


3.1 (2017-02-24)
================

- Add a ``locationprefix`` option to configure a folder where all other
  backup and snapshot folders will be created [erral]

- Only claim compatibility with Python 2.6 and 2.7.  [maurits]

- Updated test buildout to use most recent versions.  [maurits]


3.0.0 (2015-12-31)
==================

- Refactored the init and install methods of this recipe.  During the
  init phase we were reading the buildout configuration, but during
  this phase the configuration is still being build.  So differences
  could occur, especially in the order of execution of parts.  This
  was not good.  Most code is now moved from the init to the install
  (and update) method.  This has less possible problems.  Downside:
  some configuration errors are caught later.
  [maurits]

- Read ``zeo-var``, ``var``, ``file-storage`` from buildout sections.
  Update default backup and Data.fs locations based on this.
  [maurits]


2.22 (2015-12-30)
=================

- Do not accept ``backup_blobs`` false and ``enable_zipbackup`` true.
  The zipbackup script is useless without blobs.
  [maurits]

- Set default ``backup_blobs`` to true on Python 2.6 (Plone 4) and
  higher.  Otherwise false.  If no ``blob_storage`` can be found, we
  quit with an error.
  [maurits]

- Accept ``true``, ``yes``, ``on``, ``1``, in lower, upper or mixed
  case as true value.  Treat all other values in the buildout options
  as false.
  [maurits]

- Find plone.recipe.zope2instance recipes also when they are not
  completely lower case.  The zope2instance recipe itself works fine
  when it has mixed case, so we should accept this too.
  [maurits]


2.21 (2015-10-06)
=================

- When restoring, create ``var/filestorage`` if needed.
  Fixes #23.
  [maurits]


2.20 (2014-11-11)
=================

- Add ``enable_fullbackup`` option.  Default: true, so no change
  compared to previous version.
  [maurits]

- Create backup/snapshot/zipbackup directories only when needed.
  Running the backup script should not create the snapshot
  directories.
  [maurits]

- Add zipbackup and ziprestore scripts when ``enable_zipbackup = true``.
  [maurits]


2.19 (2014-06-16)
=================

- Call repozo with ``--quick`` when making an incremental backup.
  This is a lot faster.  Theoretically it lead to inconsistency if
  someone is messing in your backup directory.  You can return to the
  previous behavior by specifying ``quick = false`` in the backup
  recipe part in your buildout config.
  [maurits]

- check and create folders now happens after pre_commands is run
  [@djay]


2.18 (2014-04-29)
=================

- Add ``rsync_options`` option.  These are added to the default
  ``rsync -a`` command. Default is no extra parameters. This can be
  useful for example when you want to restore a backup from a
  symlinked directory, in which case ``rsync_options = --no-l -k``
  does the trick.
  [fiterbek]



2.17 (2014-02-07)
=================

- Add ``alternative_restore_sources`` option.  This creates a
  ``bin/altrestore`` script that restores from an alternative backup
  location, specified by that option.  You can use this to restore a
  backup of the production data to your testing or staging server.
  [maurits]

- When checking if the backup script will be able to create a path,
  remove all created directories.  Until now, only the final directory
  was removed, and not any created parent directories.
  [maurits]

- Testing: split the single big doctest file into multiple files, to
  make the automated tests less dependent on one another, making it
  easier to change them and add new ones.
  [maurits]

- No longer test with Python 2.4, because Travis does not support it
  out of the box.  Should still work fine.
  [maurits]


2.16 (2014-01-14)
=================

- Do not create blob backup dirs when not backing up blobs.
  Do not create filestorage backup dirs when not backing up filestorage.
  Fixes https://github.com/collective/collective.recipe.backup/issues/17
  [maurits]


2.15 (2013-09-16)
=================

- Restore compatibility with Python 2.4 (Plone 3).
  [maurits]


2.14 (2013-09-09)
=================

- Archive blob backups with buildout option ``gzip_blob``.
  [matejc]


2.13 (2013-07-15)
=================

- When printing that we halt the execution due to an error running
  repozo, actually halt the execution.
  [maurits]


2.12 (2013-06-28)
=================

- Backup directories are now created when we launch ``backup`` or
  ``fullbackup`` or ``snapshotbackup`` scripts, no more during
  initialization.
  [bsuttor]


2.11 (2013-05-06)
=================

- Print the names of filestorages and blobstorages that will be
  restored.  Issue #8.
  [maurits]

- Added a new command-line argument : ``--no-prompt`` disables user
  input when restoring a backup or snapshot. Useful for shell scripts.
  [bouchardsyl]

- Fixed command-line behavior with many arguments and not only a date.
  [bouchardsyl]


2.10 (2013-03-30)
=================

- Added ``fullbackup`` script that defaults to ``full=true``.  This
  could have been handled by making a new part, but it seemed like
  overkill to have to generate a complete new set of backup scripts,
  just to get one for full.
  [spanky]


2.9 (2013-03-06)
================

- Fixed possible KeyError: ``blob_snapshot_location``.
  [gforcada]



2.8 (2012-11-13)
================

- Fixed possible KeyError: ``blob_backup_location``.
  https://github.com/collective/collective.recipe.backup/issues/3
  [maurits]


2.7 (2012-09-27)
================

- additional_filestorages improved: blob support and custom location.
  [mamico]


2.6 (2012-08-29)
================

- Added pre_command and post_command options.  See the documentation.
  [maurits]


2.5 (2012-08-08)
================

- Moved code to github:
  https://github.com/collective/collective.recipe.backup
  [maurits]


2.4 (2011-12-20)
================

- Fixed silly indentation error that prevented old blob backups from
  being deleted when older than ``keep_blob_days`` days.
  [maurits]


2.3 (2011-10-05)
================

- Quit the rest of the backup or restore when a repozo call gives an
  error.  Main use case: when restoring to a specific date repozo will
  quit with an error when no files can be found, so we should also not
  try to restore blobs then.
  [maurits]

- Allow restoring the blobs to the specified date as well.
  [maurits]


2.2 (2011-09-14)
================

- Refactored script generation to make a split between initialization
  code and script arguments.  This restores compatibility with
  zc.buildout 1.5 for system pythons.  Actually we no longer create so
  called 'site package safe scripts' but just normal scripts that work
  for all zc.buildout versions.
  [maurits]

- Added option ``keep_blob_days``, which by default specifies that
  only for partial backups we keep 14 days of backups.  See the
  documentation.
  [maurits]

- Remove old blob backups when doing a snapshot backup.
  [maurits]


2.1 (2011-09-01)
================

- Raise an error when the four backup location options
  (blobbackuplocation, blobsnapshotlocation, location and
  snapshotlocation) are not four distinct locations (or empty
  strings).
  [maurits]

- Fixed possible TypeError: 'Option values must be strings'.
  Found by Alex Clark, thanks.
  [maurits]


2.0 (2011-08-26)
================

- Backup and restore blobs, using rsync.
  [maurits]

- Ask if the user is sure before doing a restore.
  [maurits]


1.7 (2010-12-10)
================

- Fix generated repozo commands to work also
  when recipe is configured to have a non **Data.fs**
  main db plus additional filestorages.
  e.g.:
  datafs= var/filestorage/main.fs
  additional = catalog
  [hplocher]


1.6 (2010-09-21)
================

- Added the option enable_snapshotrestore so that the creation of the
  script can be removed. Backwards compatible, if you don't specify it
  the script will still be created. Rationale: you may not want this
  script in a production buildout where mistakenly using
  snapshotrestore instead of snapshotbackup could hurt.
  [fredvd]


1.5 (2010-09-08)
================

- Fix: when running buildout with a config in a separate directory
  (like ``bin/buildout -c conf/prod.cfg``) the default backup
  directories are no longer created inside that separate directory.
  If you previously manually specified one of the location,
  snapshotlocation, or datafs parameters to work around this, you can
  probably remove those lines.  So: slightly saner defaults.
  [maurits]


1.4 (2010-08-06)
================

- Added documentation about how to get the required bin/repozo script
  in your buildout if for some reason you do not have it yet (like on
  Plone 4 when you do not have a zeo setup).
  Thanks to Vincent Fretin for the extra buildout lines.
  [maurits]


1.3 (2009-12-08)
================

- Added snapshotrestore script.  [Nejc Zupan]


1.2 (2009-10-26)
================

- The part name is now reflected in the created scripts and var/ directories.
  Originally bin/backup, bin/snapshotbackup, bin/restore and var/backups
  plus var/snapshotbackups were hardcoded.  Those are still there when you
  name your part ``[backup]``.  With a part named ``[NAME]``, you get
  bin/NAME, bin/NAME-snapshot, bin/NAME-restore and var/NAMEs plus
  var/NAME-snapshots.  Request by aclark for plone.org.  [reinout]


1.1 (2009-08-21)
================

- Run the cleanup script (removing too old backups that we no longer
  want to keep) for additional file storages as well.
  Fixes https://bugs.launchpad.net/collective.buildout/+bug/408224
  [maurits]

- Moved everything into a src/ subdirectory to ease testing on buildbot (which
  would grab all egss in the eggs/ dir that buildbot's mechanism creates.
  [reinout]


1.0 (2009-02-06)
================

- Quote all paths and arguments so that it works on paths that contain
  spaces (specially on Windows). [sidnei]


0.9 (2008-12-05)
================

- Windows path compatibility fix.  [Juan A. Diaz]


0.8 (2008-09-23)
================

- Changed the default for gzipping to True. Adding ``gzip = true`` to all our
  server deployment configs gets tired pretty quickly, so doing it by default
  is the best default. Stuff like this needs to be changed **before** a 1.0
  release :-) [reinout]

- Backup of additional databases (if you have configured them) now takes place
  before the backup of the main database (same with restore). [reinout]


0.7 (2008-09-19)
================

- Added $BACKUP-style enviroment variable subsitution in addition to the tilde
  expansion offered by 0.6. [reinout, idea by Fred van Dijk]


0.6 (2008-09-19)
================

- Fixed the test setup so both bin/test and python setup.py test
  work. [reinout+maurits]

- Added support for ~ in path names. And fixed a bug at the same time that
  would occur if you call the backup script from a different location than
  your buildout directory in combination with a non-absolute backup
  location. [reinout]


0.5 (2008-09-18)
================

- Added support for additional_filestorages option, needed for for instance a
  split-out catalog.fs. [reinout]

- Test setup fixes. [reinout+maurits]


0.4 (2008-08-19)
================

- Allowed the user to make the script more quiet (say in a cronjob)
  by using 'bin/backup -q' (or --quiet).  [maurits]

- Refactored initialization template so it is easier to change.  [maurits]


0.3.1 (2008-07-04)
==================

- Added 'gzip' option, including changes to the cleanup functionality that
  treats .fsz also as a full backup like .fs. [reinout]

- Fixed typo: repoze is now repozo everywhere... [reinout]


0.2 (2008-07-03)
================

- Extra tests and documentation change for 'keep': the default is to keep 2
  backups instead of all backups. [reinout]

- If debug=true, then repozo is also run in --verbose mode. [reinout]


0.1 (2008-07-03)
================

- Added bin/restore. [reinout]

- Added snapshot backups. [reinout]

- Enabled cleaning up of older backups. [reinout]

- First working version that runs repozo and that creates a backup dir if
  needed. [reinout]

- Started project based on zopeskel template. [reinout]


