##########################
Heimdall - MySQL connector
##########################

.. image:: https://img.shields.io/badge/license-AGPL3.0-informational?logo=gnu&color=success
   :target: https://www.gnu.org/licenses/agpl-3.0.html
.. image:: https://www.repostatus.org/badges/latest/active.svg
   :target: https://www.repostatus.org/#project-statuses
.. image:: https://img.shields.io/pypi/v/pyheimdall-mysql
   :target: https://pypi.org/project/pyheimdall-mysql/
   :alt: PyPI Version
.. image:: https://img.shields.io/badge/documentation-api-green
   :target: https://datasphere.readthedocs.io/projects/heimdall/
.. image:: https://gitlab.huma-num.fr/datasphere/heimdall/connectors/mysql/badges/main/pipeline.svg
   :target: https://gitlab.huma-num.fr/datasphere/heimdall/connectors/mysql/pipelines/latest
.. image:: https://gitlab.huma-num.fr/datasphere/heimdall/connectors/mysql/badges/main/coverage.svg
   :target: https://datasphere.gitpages.huma-num.fr/heimdall/connectors/mysql/coverage/index.html


*************
What is this?
*************

`pyHeimdall <https://datasphere.readthedocs.io/projects/heimdall/>`_ is a tool for converting more easily one or more databases from one format to another.
It leverages modules called "connectors", responsible for conversion of data between specific databases schemas and the HERA format.

This repository implements a connector to retrieve data from a MySQL database.
The implementation doesn't need any intervention on pyHeimdall proper.


*****************
How can I use it?
*****************

Setup
=====

This MySQL pyHeimdall connector is available as a `PyPI package <https://pypi.org/project/pyheimdall-mysql/>`_ named ``pyheimdall-mysql``.
You can install it using the `pip <https://pip.pypa.io/en/stable/>`_ package manager:

.. code-block:: bash

   pip install pyheimdall-mysql

You can use `pip <https://pip.pypa.io/en/stable/>`_ to either upgrade or uninstall this connector, too:

.. code-block:: bash

   pip install --upgrade pyheimdall-mysql
   pip uninstall pyheimdall-mysql

Usage
=====

.. code-block:: python

   import heimdall

   tree = heimdall.getDatabase(
           format='sql:mysql',
           url='mysql://myusername:mypassword@myhost:myport/mydatabase',
           entities=('mytable', 'myothertable', ),
           )
   heimdall.createDatabase(tree, format='xml:hera', url='mydatabase.xml')

Please note that you don't need to use ``pyheimdall-mysql`` functions directly.
As long as the package is installed on your system, pyHeimdall will automatically discover its features and allow you to use them as long as any other `default <https://gitlab.huma-num.fr/datasphere/heimdall/python/-/tree/main/src/heimdall/connectors>`_ or `external <https://gitlab.huma-num.fr/datasphere/heimdall/connectors>`_ connector.


*************
Is it tested?
*************

Of course!
Here's `the coverage report <https://datasphere.gitpages.huma-num.fr/heimdall/connectors/mysql/coverage/index.html>`_.

| Please note, however, than this coverage report is produced by a continuous integration (CI).
  This CI relies in part on third party tools which are *not* MySQL, but `MariaDB <https://mariadb.org/>`_.
  At the time of writing, MySQL and MariaDB still have a lot in common, but this may not be the case when you'll read these lines.
| Moreover, as time goes by, the MySQL tools used by our CI will become outdated, and we don't plan to maintain them up to date as, still at the time of writing, it's becoming increasingly difficult to easily deploy MySQL instead of MariaDB, and the existing ways are subject to Oracle's whim.
| In other words, this connector *should* work on your MySQL database, but we can't guarantee it on the long term.
  If you detect an issue, and/or can provide a solution, feel free to contribute!


For an alternative, consider using MariaDB, and the connector ``pyheimdall-mariadb``.


*********************
How can I contribute?
*********************

This project welcomes any feedback or proposal.
Details can be accessed `here <https://gitlab.huma-num.fr/datasphere/heimdall/python/-/blob/main/CONTRIBUTING.rst>`_


*******
License
*******

`GNU Affero General Public License version 3.0 or later <https://choosealicense.com/licenses/agpl/>`_

This project is not affiliated, associated, authorized, endorsed by, or in any way officially connected with MySQL or Oracle, or any of its subsidiaries or its affiliates.
The official MySQL website can be found at https://www.mysql.com/.
The name MySQL as well as related names, marks, emblems and images, are registered trademarks of Oracle.
