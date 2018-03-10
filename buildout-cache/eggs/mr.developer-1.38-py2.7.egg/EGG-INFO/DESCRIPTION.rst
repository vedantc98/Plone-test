.. contents:: :depth: 1

Introduction
============

.. figure:: http://fschulze.github.com/mr.developer/xkcd-buildout.png
    :figwidth: image

    Let Mr. Developer help you win the everlasting buildout battle!

    (Remixed by Matt Hamilton, original from http://xkcd.com/303)

**mr.developer** is a `zc.buildout`_ extension that makes it easy to work with
buildouts containing lots of packages, of which you only want to develop some.
The basic idea comes from Wichert Akkerman's plonenext_ effort.

.. image:: https://secure.travis-ci.org/fschulze/mr.developer.png

.. _`zc.buildout`: http://pypi.python.org/pypi/zc.buildout
.. _plonenext: http://svn.plone.org/svn/plone/plonenext/3.3/README.txt

Usage
=====

Add ``mr.developer`` to the ``extensions`` entry in your ``[buildout]``
section::

  [buildout]
  extensions = mr.developer

This enables additional ``[buildout]`` options:

``sources``
  This specifies the name of a section which lists the repository
  information for your packages. Defaults to ``sources``.

``sources-dir``
  This specifies the default directory where your development packages will
  be placed. Defaults to ``src``.

``auto-checkout``
  This specifies the names of packages which should be checked out during
  buildout. Packages already checked out are skipped. You can use ``*`` as
  a wildcard for all packages in ``sources``.

``always-checkout``
  This defaults to ``false``. If it's ``true``, then all packages specified
  by ``auto-checkout`` and currently in develop mode are updated during each
  buildout run. If set to ``force``, then packages are updated even when
  they are dirty instead of asking interactively.

``update-git-submodules``
  This defaults to ``always``. If it's ``always``, then submodules present
  in each package in develompent will be registered and updated on checkout and
  new ones on updates via the develop command. If you don't want to initialize any submodule,
  set value to ``never``. If you set the value to ``checkout``,
  code inside submodules will be pulled only the first time, so the ``develop up`` command
  will leave the submodule empty. Note that update only initializes
  new submodules, it doesn't pull newest code from original submodule repo.

``always-accept-server-certificate``
  This defaults to ``false``. If it's ``true``, invalid server
  certificates are accepted without asking (for subversion repositories).

``mr.developer-threads``
  This sets the number of threads used for parallel checkouts. See
  `Lockups during checkouts and updates`_ why you might need this.

``git-clone-depth``
  This sets the git clone history size (git clone --depth parameter).
  Not really useful for development, but really useful on CI environments.
  The other big benefit is the speedup on cloning,
  as only few revisions are downloaded.
  Default is to get the full history.

The format of entries in the ``[sources]`` section is::

  [sources]
  name = kind url [key=value ...]

Where individual parts are:

``name``
  The package name.

``kind``
  The kind of repository. Currently supported are ``svn``,
  ``hg``, ``git``, ``bzr``, ``darcs``, ``cvs``, or ``fs``.

``url``
  The location of the repository. This value is specific to the version
  control system used.

``key=value``
  You can add options for each individual package with this. No whitespace is
  allowed in ``key``, ``value``, and around the equal sign. For a
  description of the options see below. (*Note*: don't surround your ``key=value``
  with square brackets: we only use ``[ ]`` here to indicate that it
  is optional to add options.)


The per-package options are:

Common options
  The ``path`` option allows you to set the base directory where the
  package will be checked out. The name of the package will be appended to
  the base path. If ``path`` is not set, ``sources-dir`` is used.

  With ``full-path`` you can set the directory where the package will be
  checked out. This is the actual destination, nothing will be added. As 
  an example::

    [sources]
    pkg = fs pkg full-path=/path/to/pkg

  The ``update`` option allows you to specify whether a package will be
  updated during buildout or not. If it's ``true``, then it will always be
  updated. If it's ``false``, then it will never be updated, even if the
  global ``always-checkout`` option is set.

  The ``egg`` option makes it possible to manage packages which are not
  eggs with ``egg=false``. All commands like ``update`` work as expected,
  but the package isn't added to the ``develop`` buildout option and the
  ``activate`` and ``deactivate`` commands skip the package.

  The ``newest_tag`` option allows you to checkout/update to the newest tag.
  Possible values of the option are "true" and "false".
  The ``newest_tag_prefix`` option allows you to limit the selection of tags to
  those which start with the prefix.
  These two options currently only work for ``cvs`` and ``hg``.

``svn``
  The ``url`` is one of the urls supported by subversion.

  You can specify a url with a revision pin, like
  ``http://example.com/trunk@123``.

  You can also set the ``rev`` or ``revision`` option, which is either a pin
  like with ``rev=123`` or a minimum revision like ``rev=>123`` or
  ``rev=>=123``. When you set a minimum revision, the repository is updated
  when the current revision is lower.

``git``
  The ``branch`` option allows you to use a specific branch instead of
  master.

  The ``rev`` option allows you to use a specific revision (usually a
  tag) instead of the HEAD.

  The ``pushurl`` options allows you to explicitly separate push url from pull
  url, configured by git config.

  The ``submodules`` option allows you to initialize existing submodules.
  Default value is controled by the buildout option ``update-git-submodules``.
  Possible values are the same described before in ``update-git-submodules`` option,

  The ``depth`` option allows to specify how much history you want to clone.
  This is the so called *shallow clones*.
  Note that this is mostly not useful at all for regular clones,
  on the other hand for one time usages (continuous integration for example) it makes clones much faster.
  This option overrides a general ``git-clone-depth`` value,
  so per-source depth can be specified.

  Note that the ``branch`` and ``rev`` option are mutually exclusive.

``hg``
  The ``branch`` option allows you to use a specific branch instead of
  default.

  The ``rev`` option allows you to force a specific revision
  (hash, tag, branch) to be checked out after buildout

``bzr``
  Currently no additional options.

``darcs``
  Currently no additional options.

``cvs``
  The ``cvs_root`` option can be used to override the setting of the $CVSROOT
  environment variable.
  The ``tag`` option forces checkout/update of the given tag instead of CVS
  HEAD.

  The ``tag_file`` option defines from which file tags will be read (in case of
  using ``newest_tag``).  Default value is "setup.py".

``fs``
  This allows you to add packages on the filesystem without a version
  control system, or with an unsupported one. You can activate and
  deactivate packages, but you don't get status info and can't update etc.

  The ``url`` needs to be the same as the ``name`` of the package.

Here's an example of how your ``buildout.cfg`` may look like::

  [buildout]
  extensions = mr.developer
  auto-checkout = my.package

  [sources]
  my.package = svn http://example.com/svn/my.package/trunk update=true
  some.other.package = git git://example.com/git/some.other.package.git

When you run buildout, the script ``bin/develop`` is created in your
buildout directory. With this script you can perform various actions on
packages, like checking out their source code, without the need to know where
the repositories are located.

For help on what the script can do, run ``bin/develop help``.

If you checked out the source code of a package, you must run buildout again.
The new package will then be marked as a development egg and have its version
pin cleared (if any). You can control the list of development eggs explicitely
with the ``activate`` and ``deactivate`` commands.

Any source where the path is a symlink is skipped during updates, as it is
assumed, that the developer handles it manually. It is basically treated like
a filesystem source.

Configuration
=============

You can add options to your global ``~/.buildout/mr.developer.cfg`` or local
``.mr.developer-options.cfg`` in your buildout. Don't ever edit
``.mr.developer.cfg`` in your buildout though, it's generated automatically.

In the ``[mr.developer]`` section you have the following options.

``threads``
  This sets the number of threads used for parallel checkouts. See
  `Lockups during checkouts and updates`_ why you might need this.

In the ``[rewrites]`` section you can setup rewrite rules for sources. This is
useful if you want to provide a buildout with sources to repositories which have
different URLs for repositories which are read only for anonymous users. In that
case developers can add a URL rewrite which automatically changes the URL to a
writable repository.

The rewrite rules can have multiple operators:

``=``
  Matches the exact string. Useful to only operated on sources of a certain kind
  and similar things. This doesn't rewrite anything, but limits the rule.

``~=``
  Matches with a regular expression. This doesn't rewrite anything, but limits
  the rule.

``~``
  This runs a regular expression substitution. The substitute is read from the
  next line. You can use groups in the expression and the backslash syntax in
  the substitute. See `re.sub`_ documentation.

.. _`re.sub`: http://docs.python.org/2/library/re.html#re.sub

The following are useful examples::

  [rewrites]

  plone_svn =
    url ~ ^http://svn.plone.org/svn/
    https://svn.plone.org/svn/

  github =
    url ~ ^https://github.com/
    git@github.com:
    kind = git

  my_mrdeveloper_fork =
    url ~ fschulze(/mr.developer.git)
    me\1

  my_mrdeveloper_fork_alternate =
    url ~= fschulze/mr.developer.git
    url ~ fschulze/
    me/

Extending
=========

You can extend mr.developer to teach it new types of Working Copies
and to add or modify existing commands.

Mr.developer uses entrypoints for this. TO see examples on how to create entry
points in detail, you can have a look at the existing entry points.

Adding support for a new working copy type
------------------------------------------
Add en entry to the entry point group ``mr.developer.workingcopytypes``.
They key of the entry is going to be used in the sources section of your
buildout file. The value should be a class.
The referenced class must implement the following methods::

    - __init__(self, source)
    - matches(self)
    - checkout(self, **kwargs)
    - status(self, verbose=False, **kwargs)
    - update(self, **kwargs)

The source is a dictionary like object. The source object provides the
attributes::

    - name
    - url
    - path

In addition it contains all key value pairs one can define on the source line
in buildout, and a methods ``exists`` that returns, whether the ``path``
already exists.

The matches method must return, if the checkout at the ``path`` matches the
repository at ``url``

The commands map to the commands mr.developer provides. To see the list of
potential arguments, check the documentation of the commands.
The commands ``checkout`` and update only return what they want to have printed
out on stdout, the ``status`` command must check the verbose flag. If the
verbose flag is set, it must return a tuple with what it wants to print out and
what the VCS commands generated as output.

All objects must have list ``_output`` which contains logging information.
Please refer to existing implementations for how to fill this information.

If your working copy Handler needs to throw an error, throw errors with
``mr.developer.common.WCError`` as a base clase.

If you need to add new functionality for new commands or change behavior of
something, try not to write a new working copy handler. Try your best your
changes generically useful and get them into mr.developer.

Adding a new command
--------------------
Add an entry to the entry point group ``mr.developer.commands``.
The key will be the name of the command itself.

The referenced class must implement the following methods::

    - __init__(self, develop)
    - __call__(self, args)

An inversion of control happens here. On initalization, you receive a develop
object that represents the class handling invocation of ``./bin/develop``
It is now your job to modify the attributes of the ``develop`` object to handle
argument parsing.
Create an ArgumentParser and add it to ``develop.parsers``.

Upon calling, you can perform your actions. It is a good idea to subclass from
``mr.developer.commands.Command``. It provides convenient helper methods::

    - get_workingcopies(self, sources)
    - get_packages(args, auto_checkout, develop, checked_out)

``get_workingcopies`` gives you a WorkingCopies object that will delegate all
your working copy actions to the right working copy handler.

``get_packages`` is a little helper to get sources filterd by the rules.
``args`` can be one or more regular expression filtr on source names, the other
attributes are boolean flags that by default are ``False``. False means _not_
to filter. Calling the method only with the ``arg`` '.' would thus return all
packges. THe returned object is a set containing only the names of the sources.

To perform an action, you get the package names via get_packages. then you get
the WorkingCopies object and call the action you want to perform on this
object. THe WorkingCopies object checks, which working copy is responsible for
the given package and delegates the action to this object. The WorkingCopies
object is also handling threading functionality.

The ``develop`` object has a ``config`` property. This object can be used to
store configuration of your actions. under ``config.develop`` a dictionary
resides which stores, whether the source with the given key is going to be used
from source checkout.


Troubleshooting
===============

Dirty SVN
---------

You get an error like::

  ERROR: Can't switch package 'foo' to 'https://example.com/svn/foo/trunk/' because it's dirty.

If you have not modified the package files under src/foo, then you can check
what's going on with ``status -v``. One common cause is a ``*.egg-info`` folder
which gets generated every time you run buildout and this shows up as an
untracked item in svn status.

You should add .egg-info to your global Subversion ignores in
``~/.subversion/config``, like this::

  global-ignores = *.o *.lo *.la *.al .libs *.so *.so.[0-9]* *.a *.pyc *.pyo *.rej *~ #*# .#* .*.swp .DS_Store *.egg-info

HTTPS Certificates
------------------

The best way to handle https certificates at the moment, is to accept them
permanently when checking out the source manually.

Mercurial reports mismatching URL
---------------------------------

This happens if you use lp:// URLs from launchpad. The problem is, that hg
reports the actual URL, not the lp shortcut.

Lockups during checkouts and updates
------------------------------------

Especially on multicore machines, there is an issue that you can get lockups
because of the parallel checkouts. You can configure the number of threads used
for this in ``.mr.developer.cfg`` in the buildout root of your project or
globally in ``~/.buildout/mr.developer.cfg`` through the ``threads`` option
in the ``[mr.developer]`` section or in your buildout in the ``buildout``
section with the ``mr.developer-threads`` option. Setting it to ``1`` should
fix these issues, but this disables parallel checkouts and makes the process a
bit slower.

Also, if you have `ControlPersist` in your local ssh config, and you
have a source checkout that uses ssh (for example
``git@github.com:...``) the checkout or update may work fine, but the
ssh connection may stay open and ``mr.developer`` cannot exit because
it waits for the ssh process to finish.


Commands
========

The following is a list of all commands and their options.

activate (a)
------------

::

    usage: develop activate [-h] [-a] [-c] [-d]
                            package-regexp [package-regexp ...]

    Add packages to the list of development packages.

    positional arguments:
      package-regexp       A regular expression to match package names.

    optional arguments:
      -h, --help           show this help message and exit
      -a, --auto-checkout  Only considers packages declared by auto-checkout. If
                           you don't specify a <package-regexps> then all declared
                           packages are processed.
      -c, --checked-out    Only considers packages currently checked out. If you
                           don't specify a <package-regexps> then all checked out
                           packages are processed.
      -d, --develop        Only considers packages currently in development mode.
                           If you don't specify a <package-regexps> then all
                           develop packages are processed.


arguments (args)
----------------

::

    usage: develop arguments [-h]

    Print arguments used by last buildout which will be used with the 'rebuild'
    command.

    optional arguments:
      -h, --help  show this help message and exit


checkout (co)
-------------

::

    usage: develop checkout [-h] [-a] [-v] package-regexp [package-regexp ...]

    Make a checkout of the packages matching the regular expressions and add them
    to the list of development packages.

    positional arguments:
      package-regexp       A regular expression to match package names.

    optional arguments:
      -h, --help           show this help message and exit
      -a, --auto-checkout  Only considers packages declared by auto-checkout. If
                           you don't specify a <package-regexps> then all declared
                           packages are processed.
      -v, --verbose        Show output of VCS command.


deactivate (d)
--------------

::

    usage: develop deactivate [-h] [-a] [-c] [-d]
                              package-regexp [package-regexp ...]

    Remove packages from the list of development packages.

    positional arguments:
      package-regexp       A regular expression to match package names.

    optional arguments:
      -h, --help           show this help message and exit
      -a, --auto-checkout  Only considers packages declared by auto-checkout. If
                           you don't specify a <package-regexps> then all declared
                           packages are processed.
      -c, --checked-out    Only considers packages currently checked out. If you
                           don't specify a <package-regexps> then all checked out
                           packages are processed.
      -d, --develop        Only considers packages currently in development mode.
                           If you don't specify a <package-regexps> then all
                           develop packages are processed.


help (h)
--------

::

    usage: develop help [-h] [--rst] [-z] [command]

    Show help on the given command or about the whole script if none given.

    positional arguments:
      command     The command you want to see the help of.

    optional arguments:
      -h, --help  show this help message and exit
      --rst       Print help for all commands in reStructuredText format.
      -z, --zsh   Print info for zsh autocompletion


info
----

::

    usage: develop info [-h] [-a] [-c] [-d] [--name] [-p] [--type] [--url]
                        [package-regexp [package-regexp ...]]

    Lists informations about packages.

    positional arguments:
      package-regexp       A regular expression to match package names.

    optional arguments:
      -h, --help           show this help message and exit
      -a, --auto-checkout  Only considers packages declared by auto-checkout. If
                           you don't specify a <package-regexps> then all declared
                           packages are processed.
      -c, --checked-out    Only considers packages currently checked out. If you
                           don't specify a <package-regexps> then all declared
                           packages are processed.
      -d, --develop        Only considers packages currently in development mode.
                           If you don't specify a <package-regexps> then all
                           declared packages are processed.

    Output options:
      The following options are used to print just the info you want, the order
      they are specified reflects the order in which the information will be
      printed.

      --name               Prints the name of the package.
      -p, --path           Prints the absolute path of the package.
      --type               Prints the repository type of the package.
      --url                Prints the URL of the package.


list (ls)
---------

::

    usage: develop list [-h] [-a] [-c] [-d] [-l] [-s]
                        [package-regexp [package-regexp ...]]

    Lists tracked packages.

    positional arguments:
      package-regexp       A regular expression to match package names.

    optional arguments:
      -h, --help           show this help message and exit
      -a, --auto-checkout  Only show packages in auto-checkout list.
      -c, --checked-out    Only considers packages currently checked out. If you
                           don't specify a <package-regexps> then all checked out
                           packages are processed.
      -d, --develop        Only considers packages currently in development mode.
                           If you don't specify a <package-regexps> then all
                           develop packages are processed.
      -l, --long           Show URL and kind of package.
      -s, --status         Show checkout status.
                           The first column in the output shows the checkout
                           status:
                               '#' available for checkout
                               ' ' in auto-checkout list and checked out
                               '~' not in auto-checkout list, but checked out
                               '!' in auto-checkout list, but not checked out
                               'C' the repository URL doesn't match


purge
-----

::

    usage: develop purge [-h] [-n] [-f] [package-regexp [package-regexp ...]]

    Remove checked out packages which aren't active anymore.

    Only 'svn' packages can be purged, because other repositories may contain
    unrecoverable files even when not marked as 'dirty'.

    positional arguments:
      package-regexp  A regular expression to match package names.

    optional arguments:
      -h, --help      show this help message and exit
      -n, --dry-run   Don't actually remove anything, just print the paths which
                      would be removed.
      -f, --force     Force purge even if the working copy is dirty or unknown
                      (non-svn).


rebuild (rb)
------------

::

    usage: develop rebuild [-h] [-n]

    Run buildout with the last used arguments.

    optional arguments:
      -h, --help     show this help message and exit
      -n, --dry-run  DEPRECATED: Use 'arguments' command instead. Don't actually
                     run buildout, just show the last used arguments.


reset
-----

::

    usage: develop reset [-h] [-a] [-c] [-d] [package-regexp [package-regexp ...]]

    Resets the packages develop status. This is useful when switching to a new
    buildout configuration.

    positional arguments:
      package-regexp       A regular expression to match package names.

    optional arguments:
      -h, --help           show this help message and exit
      -a, --auto-checkout  Only considers packages declared by auto-checkout. If
                           you don't specify a <package-regexps> then all declared
                           packages are processed.
      -c, --checked-out    Only considers packages currently checked out. If you
                           don't specify a <package-regexps> then all checked out
                           packages are processed.
      -d, --develop        Only considers packages currently in development mode.
                           If you don't specify a <package-regexps> then all
                           develop packages are processed.


status (stat, st)
-----------------

::

    usage: develop status [-h] [-a] [-c] [-d] [-v]
                          [package-regexp [package-regexp ...]]

    Shows the status of tracked packages, filtered if <package-regexps> is given.
    The first column in the output shows the checkout status:
        ' ' in auto-checkout list
        '~' not in auto-checkout list
        '!' in auto-checkout list, but not checked out
        'C' the repository URL doesn't match
        '?' unknown package (only reported when package-regexp is not specified)
    The second column shows the working copy status:
        ' ' no changes
        'M' local modifications or untracked files
        '>' your local branch is ahead of the remote one
    The third column shows the development status:
        ' ' activated
        '-' deactivated
        '!' deactivated, but the package is in the auto-checkout list
        'A' activated, but not in list of development packages (run buildout)
        'D' deactivated, but still in list of development packages (run buildout)

    positional arguments:
      package-regexp       A regular expression to match package names.

    optional arguments:
      -h, --help           show this help message and exit
      -a, --auto-checkout  Only considers packages declared by auto-checkout. If
                           you don't specify a <package-regexps> then all declared
                           packages are processed.
      -c, --checked-out    Only considers packages currently checked out. If you
                           don't specify a <package-regexps> then all checked out
                           packages are processed.
      -d, --develop        Only considers packages currently in development mode.
                           If you don't specify a <package-regexps> then all
                           develop packages are processed.
      -v, --verbose        Show output of VCS command.


update (up)
-----------

::

    usage: develop update [-h] [-a] [-d] [-f] [-v]
                          [package-regexp [package-regexp ...]]

    Updates all known packages currently checked out.

    positional arguments:
      package-regexp       A regular expression to match package names.

    optional arguments:
      -h, --help           show this help message and exit
      -a, --auto-checkout  Only considers packages declared by auto-checkout. If
                           you don't specify a <package-regexps> then all declared
                           packages are processed.
      -d, --develop        Only considers packages currently in development mode.
                           If you don't specify a <package-regexps> then all
                           develop packages are processed.
      -f, --force          Force update even if the working copy is dirty.
      -v, --verbose        Show output of VCS command.




Changelog
=========

1.38 (2017-03-17)
-----------------

* Use ``from __future__ import print_function`` to fix output of ``help --rst``.
  [fschulze]

* Set empty version pin for develop packages instead of removing the version
  pin from the section.
  [fschulze]


1.37 (2017-03-04)
-----------------

* Add more info on git operations, so one can see which repository is cloned
  and which branch is used.
  [fschulze]

* Fix git submodules with git 2.x.
  [fschulze]



1.36 (2017-03-01)
-----------------

* Add the buildout option mr.developer-verbose that enables showing
  the same out when running buildout as when running ./bin/develop up -v.
  [sunew]

* Respect the buildout -v setting for updates, just as it already does for checkouts.
  [sunew]


1.35 - 2017-02-01
-----------------

* Do not use the backport of configparser on Python2, to fix
  "Option values must be strings" exception on some commands.
  [MatthewWilkes]

* No longer test on Python 3.2.  [maurits]

* Improve error message when a directory isn't found in fs mode.
  [idgserpro]


1.34 - 2015-09-30
-----------------

* Remove support for python 2.4 and 2.5. Use python 2.6 or higher or python
  3.2 or higher.
  [reinout]

* Report missing executables (like 'hg') instead of reporting a too-generic
  "file not found" error.
  [reinout]

* Fix bug with assignments lacking the section.  According to
  buildout's documentation ``option=value`` is equivalent to
  ``buildout:option=value``.
  Fixes issue #151
  [mvaled]

* Fix switching to git branch from revision.  When currently you are
  not on a git branch (for example on a tag), running a develop update
  would try to pull and fail.  Now we simply fetch, and handle
  possible branch switching and merging the same as we always do.
  Fixes issue #162
  [maurits]

* Fix unpinning of eggs with a name containing characters not in [^A-Za-z0-9.]
  This means that to correctly unpin pkg.foo_bar we have to delete
  ``pkg.foo-bar`` from the buildout ``[version]`` section.
  [ale-rt (Alessandro Pisa)]

* Checkout branch when cloning a git repository.
  [gforcada]


1.33 - 2015-05-25
-----------------

* Fix git-clone-depth global option, it needs to be kept as a string and not
  converted to a number.
  [gforcada, fschulze]


1.32 - 2015-05-23
-----------------

* Add git-clone-depth global option and depth per source option to specify on
  git clones how much history wants to be cloned.
  [gforcada (Gil Forcada)]

* Add plugin interface for adding commands using entry points.
  [fschulze]

* Raise an exception if the sources section references a missing section.
  [icemac (Michael Howitz)]


1.31 - 2014-10-29
-----------------

* Fixed submodule matching for some git versions.
  [jod (Josip Delic), fschulze]

* Added compat.py for Python 3.
  [jod (Josip Delic)]

* More info when svn cannot switch because of dirty checkout.
  [gotcha]

* Git: try to switch to branch master when no branch has been
  specified.  Do not give an error in this case when master is not
  there.  Fixes issue #125
  [maurits]


1.30 - 2014-03-14
-----------------

* Fix regression from 1.29.
  [Trii (Josh Johnston)]


1.29 - 2014-03-14
-----------------

* Preserve order of eggs specified in ``develop`` option.
  [anjos (André Anjos)]


1.28 - 2014-01-23
-----------------

* Mercurial now checks if working copy is ahead of remote branch.
  [rafaelbco]

1.27 - 2014-01-10
-----------------

* Fix encoding issues during installation if the default encoding isn't
  properly set. Fixes issue #127
  [fschulze, jajadinimueter]

* Fix error message when listing of git branches fails. Fixes issue #124
  [toutpt (JeanMichel FRANCOIS), fschulze]

1.26 - 2013-09-10
-----------------

* Fixed branch option for git 1.6.0 until and including 1.6.2.
  Fixes issue #117.
  [maurits]

* Skip update of symlinked sources.
  [chaoflow (Florian Friesdorf)]

* Deprecate ``-n`` and ``--dry-run`` on ``rebuild`` command in favour of the
  new ``arguments`` command.

1.25 - 2013-03-15
-----------------

* Git submodules support.
  [sunbit]

* Added `newest_tag` option for mercurial and cvs.
  [kkujawinski, fschulze]

* Python 3 fixes.
  [fschulze, jajadinimueter (Florian Mueller)]

* Fix revision pinning. Refs #113
  [do3cc (Patrick Gerken)]

* Properly line up the output of ``status``.
  [fschulze]

1.24 - 2013-01-29
-----------------

* Mercurial now switches branches.
  [bubenkoff (Anatoly Bubenkov), fschulze]

* Fix gitsvn/gitify working copy type which was broken since 1.22.
  [rpatterson (Ross Patterson)]

* Fix deactivate command which was broken since 1.22. Refs #105
  [fschulze, icemac]

1.23 - 2012-11-28
-----------------

* Unit tests run with Python 2.4, 2.5, 2.6, 2.7 and 3.2 now.
  [fschulze]

* Officially added source rewrites. Refs #56
  [fschulze]

* Add additional optional config file ``.mr.developer-options.cfg`` which is
  read from the buildout directory for local version controllable options.
  [fschulze]

* Update all activated packages during buildout if ``always-checkout`` is true
  instead of only the ones in the ``auto-checkout`` list or with the ``update``
  option set. Refs #95
  [fschulze]

* Fix asking for password for svn with basic authentication. Refs #100
  [MordicusEtCubitus]

* Fixed regressions in svn module. Refs #37
  [fschulze, evilbungle (Alan Hoey)]

* Fixed branch checkout for git on Python 3.
  [mitchellrj]

* Fixed subversion checkout on Python 3.
  [mitchellrj]

1.22 - 2012-10-13
-----------------

* If you set threads to 1, then we don't use any separate thread anymore, the
  actions are now done in the main thread.
  [fschulze]

* Allow configuration of the number of threads used through the buildout config
  by setting the ``mr.developer-threads`` option in the ``buildout`` section.
  [fschulze]

* For git repositories the ``status`` command shows you when your local branch
  is ahead of the remote branch.
  [fschulze]

* Always make ``sources-dir`` option available in buildout, even if it's set
  to the default. Fixes #49
  [fschulze]

* Parse revision from url for all svn commands. Fixes #37
  [fschulze]

* Use entry points to allow adding and overwriting working copy types via
  addon packages.
  [fschulze]

* Fixed ValueError in verbose status for filesystem and gitsvn sources.
  [maurits]

* Fixed some exceptions occurring when using with Python 3.
  [icemac (Michael Howitz)]

* On Windows, use the PATHEXT environment variable to find the git executable.
  [kleist]

1.21 - 2012-04-11
-----------------

* Added ``threads`` option to ``[mr.developer]`` section to set number of
  threads used for running checkouts.
  [fschulze]

* Read a per user config file from ~/.buildout/mr.developer.cfg in addition to
  the regular .mr.developer.cfg in the current buildout base.
  [fschulze]

* Python 3 support by using 2to3.
  [mitchellrj (Richard Mitchell)]

1.20 - 2012-02-26
-----------------

* Git: Added ``pushurl`` option
  [iElectric (Domen Kožar)]

* Refactored thread locking.
  [shywolf9982]

* Refactored search for git executable and version handling.
  [shywolf9982]

* In the status command report unknown packages with '?' when no
  package-regexp has been given.
  [maurits]

* Added --force option to purge command.  Especially helpful in
  purging non-subversion packages, which otherwise we refuse to
  remove.  Fixes issue #71.
  [maurits]

* Do not depend on `elementtree` if there is `xml.etree` (Python >= 2.5).

* Don't set locale anymore when calling ``svn``. This may break if the output
  is localized instead of english, I couldn't reproduce that anymore though.
  [fschulze, rochecompaan (Roché Compaan)]

* Fix compatibility with mercurial v2.1
  [janjaapdriessen (Jan-Jaap Driessen)].

1.19 - 2011-09-22
-----------------

* Git: Don't stop buildout after renaming/adding git remotes, i.e. when
  actively working on a given package.
  [witsch (Andreas Zeidler)]

* Bugfix: Honhour buildout:develop parameters even if ending with slash.
  [lukenowak]

* Installation: Check presence of required modules instead of relying on
  version of python.
  [lukenowak (Łukasz Nowak)]

1.18 - 2011-08-16
-----------------

* Mercurial: Added support for branches.
  [posborne (Paul Osborne)]

* Git: Added support for the Windows msysGit.
  [canassa (Cesar Canassa)]

* Git: Added ``rev`` option that allows you to use a specific revision
  (usually a tag) instead of the HEAD.
  [maurits (Maurits van Rees)]

1.17 - 2011-01-26
-----------------

* Git: Default to branch ``master`` if no branch is given in the source.
  [stefan]

* Brush up the README.
  [stefan]

* Create the sources-dir if it is not present.
  [janjaapdriessen]

* Only require argparse with Python < 2.7.
  [dobe]

* Fixed issue #35 using bzr, similar to the fix #28 for hg in last version.
  [menesis]

* Pass branch to bzr pull.
  [menesis]

* Add support for darcs.
  [lelit, azazel]

1.16 - 2010-09-16
-----------------

* Fix ``NameError: global name 'source' is not defined`` when using gitsvn
  and running ``status`` command.
  [markvl]

* Add handling of new ``-s`` command line option of zc.buildout 1.5, this
  fixes issue #29.
  [fschulze]

* Don't pass the PYTHONPATH onwards to mercurial, this fixes issue #28
  [fschulze, Christian Zagrodnick]

* Fix saving buildout options on Windows. Issue #24
  [fschulze]

* Only warn if the svn version is too old.
  [fschulze]

1.15 - 2010-07-25
-----------------

* Use ``always-checkout`` option from buildout config for ``update`` command.
  This fixes issue #18.
  [fschulze]

* Fix ``OSError: [Errno 10] No child processes`` errors in Python 2.4 and 2.5.
  (Issue #12)
  [fschulze]

* Fix CVS update.
  [sargo]

1.14 - 2010-05-15
-----------------

* Added bzr support.
  [tseaver]

* Added git branch support.
  [shywolf9982, fschulze]

1.13 - 2010-04-11
-----------------

* Tell the user which packages are queued for update or checkout, so one can
  check which packages are still updating now that the output is only printed
  after everything is done due to parallel checkouts.
  [fschulze]

* Added ``always-accept-server-certificate`` option. When set in the
  ``[buildout]`` section, then invalid certificates are always accepted for
  subversion repositories.
  [fschulze]

* Added ``-v``/``--version`` option.
  [tomster, fschulze]

* Use the much nicer argparse library instead of optparse.
  [fschulze]

1.12 - 2010-03-15
-----------------

* Fix svn checkout.
  [fschulze]

1.11 - 2010-03-14
-----------------

* Handle untrusted server certificates by asking the user what to do.
  [fschulze]

* Properly handle user input for authorization by using locks to prevent
  problems with parallel checkouts.
  [fschulze]

* Only checkout/update packages in auto-checkout or with ``update = true``
  option when running buildout.
  [fschulze]

1.10 - 2010-02-06
-----------------

* Don't store the buildout options if they contain a command.
  [fschulze]

* Basic support for buildout offline mode (-o). Not all cases are handled yet.
  [fschulze]

* Added ``full-path`` package option.
  [fschulze]

* Added ``egg`` package option (Issue #6).
  [fschulze]

* By setting ``always-checkout = force``, all packages will be updated
  without asking when dirty.
  [fschulze]

* The ``[path]`` part of sources is replaced by ``path=PATH`` syntax and
  throws a warning when used.
  [fschulze]

* Per package options are now allowed before the URL.
  [fschulze]

* Check ``svn`` version and output helpful error messages if it's too old or
  can't be determined (Issue #13).
  [fschulze]

* Error messages instead of tracebacks when source definitions are wrong.
  [fschulze]

* Fix checkout of packages (Issues #9 and #11).
  [fschulze]

* Possibility to checkout/update tags instead of HEAD in CVS
  [sargo]

* Tests for CVS integration
  [sargo]

* Better checking of CVS package purity.
  [sargo]

1.9 - 2010-01-11
----------------

* Added dry-run option to ``purge`` command.
  [fschulze]

* Fix purging on windows.
  [kleist (Karl Johan Kleist)]

* Fix compatibility with Python < 2.6.
  [fschulze, vincentfretin]

* Fix `all` answer for ``update`` command.
  [fschulze]

1.8 - 2010-01-10
----------------

* Added threading for parallel checkouts.
  [fschulze, jensens]

* Ask whether to update dirty packages during checkout.
  [fschulze]

* When you answered `yes` when asked whether to update a dirty package, then
  all further questions had been answered with `yes` as well, this is now
  fixed.
  [fschulze]

* Added `all` option when asked to update dirty packages.
  [fschulze]

* Added help for all commands to PyPI description.
  [fschulze]

* Added option to ``help`` command which outputs the help for all commands in
  reStructuredText format.
  [fschulze]

* Don't abort after user answered `no` on whether to update a package, just
  skip that package.
  [fschulze]

1.7 - 2009-11-26
----------------

* Fix a problem where a package wasn't added to the develop packages on auto
  checkout.
  [fschulze]

1.6 - 2009-11-21
----------------

* Filter the packages gathered from ``buildout:develop`` to ones declared in
  sources, otherwise things like "develop = ." break.
  [fschulze]

* Added support for Concurrent Versions System (CVS).
  [sargo (Wojciech Lichota)]

1.5 - 2009-11-19
----------------

* Added global ``always-checkout`` and a per source ``update`` option.
  [fschulze]

* Added ``purge`` command.
  [fschulze]

* Ask user how to proceed when package is dirty.
  [fschulze]

* Refactored package matching and made the command options consistent.
  Now you can update only the packages currently in development with ``-d``
  and similar possibilities.
  [fschulze]

* Fix duplicate logging output.
  [fschulze]

* Fix parsing of buildout arguments when ``-t`` was used.
  [fschulze]

1.4 - 2009-11-16
----------------

* Allow to set a minimal revision for ``svn`` repositories. If the current
  revision is lower, then the package is updated.
  [fschulze]

1.3 - 2009-11-15
----------------

* Read the cfg used by last buildout run. This prevents unexpected behaviour,
  if you change mr.developer options like source declarations and don't run
  buildout. Such changes are now picked up immediately.
  [fschulze]

* Added tests and a buildout to run them easily.
  [fschulze]

1.2 - 2009-11-12
----------------

* If a package is removed from ``auto-checkout`` and wasn't explicitly
  activated, then it will be removed from the develop packages automatically.
  In existing buildouts with an older mr.developer, you have to ``reset`` the
  packages first.
  [fschulze]

* Added ``*`` wild card support for ``auto-checkout``.
  [fschulze]

* Don't bail on subversion URLs ending in a slash or a revision marker.
  [fschulze]

* Removed old way of specifying sources with ``sources-svn`` and
  ``sources-git``.
  [fschulze]

* Exit immediately when there are issues during checkout when running as
  extension.
  [fschulze]

* Use verbosity from buildout when running as extension.
  [fschulze]

* Fix buildout_dir in ``develop`` script, so it is properly escaped on
  Windows.
  [fschulze]

* Changed the output of ``list -s`` to match the one from ``status``.
  [fschulze]

* Added troubleshooting section to readme.
  [miohtama, fschulze]

* All commands have a ``-h`` and ``--help`` option now to show their help.
  [fschulze]

1.1 - 2009-08-07
----------------

* Use relative paths from the buildout directory for the ``develop`` option
  if possible. This fixes issues if your buildout path contains a space.
  [fschulze]

* Warn when trying to activate or deactivate a package which isn't checked out.
  [fschulze]

* Don't depend on elementree on Python >= 2.5, because it's builtin there.
  [fschulze]

* When checking out a source it will automatically be activated.
  [fschulze]

* Use 'sources' as the default section name for source information.
  [fschulze]

* Added support for filesystem packages without version control with the
  'fs' type.
  [fschulze]

1.0.1 - 2009-05-05
------------------

* Fixed case sensitivity of package names for several commands.
  [fschulze]

* SVN externals no longer cause a modified status.
  [fschulze]

1.0 - 2009-05-02
----------------

* Added ``info`` command to print various informations about packages.
  [fschulze]

* Added ``reset`` command to reset the develop state of packages. This is
  useful when switching to a new buildout configuration. During the next
  buildout run the develop state is determined the same way as in a clean
  buildout.
  [fschulze]

* Got rid of deprecation warning in Python 2.6 by removing unnecessary call
  of __init__ in working copy implementations.
  [fschulze]

0.15 - 2009-04-17
-----------------

* Added reminder to run buildout after activating or deactivating packages.
  [fschulze]

* Added ``rebuild`` command to rerun buildout with the last used arguments.
  [fschulze]

0.14 - 2009-04-16
-----------------

* Fixed verbose output of ``checkout`` command.
  [fschulze]

* Added ``-f`` option to ``update`` command to force updates even if the
  working copy is dirty.
  [fschulze]

0.13 - 2009-04-14
-----------------

* Added ``-a`` option to ``update`` command to only update the packages
  declared in the ``auto-checkout`` list.
  [fschulze]

* Added ``activate`` and ``deactivate`` commands. This allows to select which
  packages are added to the ``develop`` option of zc.buildout. Enhanced the
  ``status`` command to show the additional informations.
  [fschulze]

* Switched the meaning of ``~`` and ``C`` in status command.
  [fschulze]

0.12 - 2009-04-14
-----------------

* Added support for Mercurial (hg).
  [mj]

* Refactored working copy logic, so it's easier to add support for other
  version control systems.
  [fschulze]

* Added verbose flag to ``checkout`` and ``update`` commands.
  [fschulze]

0.11 - 2009-04-06
-----------------

* Removed the nice os.path.relpath usage, because it's only been introduced
  with Python 2.6.
  [fschulze]

0.10 - 2009-04-06
-----------------

* Added verbose flag to ``status`` command.
  [fschulze]

* Deprecated ``sources-svn`` and ``sources-git`` in favour of just ``sources``
  which allows more flexibility.
  [fschulze]

* Changed ``status`` command to only check known paths and not the whole
  ``sources-dir`` path.
  [fschulze]

* Add possibility to filter packages in ``update`` and ``status`` commands.
  [fschulze]

* Tell the user at the end of the buildout run whether there have been any
  errors during automatic checkout.
  [fschulze]

* Install the ``develop`` script as the first part instead of the last, so it
  can be used to fix problems.
  [fschulze]

0.9 - 2009-03-30
----------------

* When installed as just an egg, then the resulting ``develop`` script can be
  called from anywhere and will try to find the correct ``develop`` script
  from the current working directory and execute it.
  [fschulze]

* Fixed help text formatting.
  [fschulze]

0.8 - 2009-03-25
----------------

* Added authentication support to subversion commands.
  [fschulze]

* Added ``-a`` option to ``checkout`` command to limit matching to the
  packages declared by the ``auto-checkout`` option. If no further argument
  is given, then all the packages from ``auto-checkout`` are processed.
  [fschulze]

0.7 - 2009-03-24
----------------

* Added ``update`` command to ``checkout`` script.
  [fschulze]

* Added ``status`` command to ``checkout`` script.
  [fschulze]

* Added status flag to ``list`` command to indicate packages with wrong URL.
  [fschulze]

* If the working copy is clean, then checkout automatically switches svn
  packages.
  [fschulze]

* Skip on checkout errors during buildout, so the develop script is generated
  and you get a chance to inspect and fix the problems.
  [fschulze]

* Check remote url and stop checkout if it differs.
  [fschulze]

* Added various options to the ``list`` command.
  [fschulze]

* Instead of the ``checkout`` script, there is now a ``develop`` script with
  various commands.
  [fschulze]

0.6 - 2009-03-24
----------------

* Added custom logging formatter for nicer output in the checkout script.
  [fschulze]

* Removed the '-e' option, regular expression matching is the default now.
  [fschulze]

* Made it possible to specify more than one regular expression without the
  need to use a pipe symbol and quotes.
  [fschulze]

* Added help text for the checkout script to pypi page.
  [fschulze]

* Add a warning to rerun buildout after checkout.
  [fschulze]

0.5 - 2009-03-23
----------------

* Make sure that the updated versions are actually used.
  [fschulze]

0.4 - 2009-03-22
----------------

* Fixed logging, which fixes the info message output.
  [fschulze]

* Skip checkout of existing packages.
  [fschulze]

0.3 - 2009-03-22
----------------

* Fixed source distribution by adding a MANIFEST.in.
  [fschulze]

* Added -e and -l options to checkout script.
  [fschulze]

0.2 - 2009-03-22
----------------

* Added ``auto-checkout`` option (only works with subversion at the moment).
  [fschulze]

* Added support for git.
  [fschulze]

* Throw error when trying to checkout unknown package.
  [fschulze]

* Fixed target directory for checkouts.
  [fschulze]

0.1 - 2009-03-19
----------------

* Initial release


