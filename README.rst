plasticscm
==========

Python package providing access to the PlasticSCM client API.

Overview
========

TBD...

`PyPI record`_.

`Documentation`_.

Requirements
============

- | It is a fully independent package.
  | All necessary things are installed during the normal installation process.
- ATTENTION: currently works and tested only for Windows.

Installation
============

Prerequisites:

+ Python 3.9 or higher

  * https://www.python.org/

+ pip and setuptools

  * https://pypi.org/project/pip/
  * https://pypi.org/project/setuptools/

To install run:

  .. parsed-literal::

    python -m pip install --upgrade |package|

Development
===========

Prerequisites:

+ Development is strictly based on *tox*. To install it run::

    python -m pip install --upgrade tox

Visit `Development page`_.

Installation from sources:

clone the sources:

  .. parsed-literal::

    git clone |respository| |package|

and run:

  .. parsed-literal::

    python -m pip install ./|package|

or on development mode:

  .. parsed-literal::

    python -m pip install --editable ./|package|

License
=======

  | |copyright|
  | Licensed under the zlib/libpng License
  | https://opensource.org/license/zlib
  | Please refer to the accompanying LICENSE file.

Authors
=======

* Adam Karpierz <adam@karpierz.net>

.. |package| replace:: plasticscm
.. |package_bold| replace:: **plasticscm**
.. |copyright| replace:: Copyright (c) 2019-2024 Adam Karpierz
.. |respository| replace:: https://github.com/karpierz/plasticscm.git
.. _Development page: https://github.com/karpierz/plasticscm/
.. _PyPI record: https://pypi.org/project/plasticscm/
.. _Documentation: https://plasticscm.readthedocs.io/
