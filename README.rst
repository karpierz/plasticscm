plasticscm
==========

Python package providing access to the PlasticSCM client API.

Overview
========

TBD...

Requirements
============

- | It is a fully independent package.
  | All necessary things are installed during the normal installation process.
- ATTENTION: currently works and tested only for Windows.

Installation
============

Prerequisites:

+ Python 3.6 or higher

  * https://www.python.org/
  * 3.7 is a primary test environment.

+ pip and setuptools

  * https://pypi.org/project/pip/
  * https://pypi.org/project/setuptools/

To install run:

.. parsed-literal::

    python -m pip install --upgrade |package|

Development
===========

Visit `development page`_.

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

Prerequisites:

+ Development is strictly based on *tox*. To install it run::

    python -m pip install --upgrade tox

License
=======

  | Copyright (c) 2019-2020 Adam Karpierz
  |
  | Licensed under the zlib/libpng License
  | https://opensource.org/licenses/zlib
  | Please refer to the accompanying LICENSE file.

Authors
=======

* Adam Karpierz <adam@karpierz.net>

.. |package| replace:: plasticscm
.. |package_bold| replace:: **plasticscm**
.. |respository| replace:: https://github.com/karpierz/plasticscm.git
.. _development page: https://github.com/karpierz/plasticscm/
