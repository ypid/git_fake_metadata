git_fake_metadata
=================

Status: Pre-alpha POC

A tool which can wrap around `git` commands and fake meta data along the way.

Git is awesome. Unfortunately it tracks quite a bit of meta data. Things like
commit time give someone analyzing that meta data quite a few insights.  If you
understand German then you might want to watch the talk `DS2010: Wir wissen was
du letzte Nacht getan hast`_ (I know what you did last night) as an example
what can be concluded from such an analysis.

So what can you do? One way would be to just set the time of your commits to
1970 but that would be too obvious. Also, you need to deal with OpenPGP
signatures from GnuPG (you are signing your git tags, right?).
So you will need to give git some meta data you just don’t necessarily want
that meta data to be authentic. That is why this tool is being written. The
idea is to fake various bits of meta data in an plausible and consistent way.

With such a tool in existence the reliability of git meta data needs to be
questioned more seriously by anyone intending to draw conclusions from it which
is the main goal of this project.

Current state
-------------

I have been hacking on this a couple of hours but ended in an unfinished
refactoring. This project is currently on hold until a working gpg version
enters Debian Stable so that ypid could actually make use of this tool.

Unfortunately, `git` seems to not provide a way to pass CLI options to GnuPG,
so a wrapper around GPG would be needed which can be configured in git config.

Note that this repository is subject to history rewriting until the tool is
able to fake the meta data of its one repo in an consistent way obviously ;)

Planned features
----------------

* Fake git commit and author time
* Fake git commit signature time using GnuPG (this could only be tested with
  gpg2 2.1.11 from Debian Stretch because in previous versions,
  `--faked-system-time` was broken )
* Compatibility with `Qubes Split GPG`_
* Flexible configuration
* Plausible and consistent metadata across `git` repositories
* Support for the `opening hours syntax from OSM`_ to specify the time ranges
  in which faked times should be.

Advanced topics
---------------

* Support `git rebase`.

Git meta data analysis tools
----------------------------

* digger_ (used in `DS2010: Wir wissen was du letzte Nacht getan hast`_)

.. _Qubes Split GPG: https://www.qubes-os.org/doc/split-gpg/
.. _opening hours syntax from OSM: https://wiki.openstreetmap.org/wiki/Key:opening_hours
.. _`DS2010: Wir wissen was du letzte Nacht getan hast`: https://pentamedia.org/datenspuren/ds10-videomitschnitte-komplett/ds2010_4050.mp4
.. _digger: https://github.com/thammi/digger
