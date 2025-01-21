#####################################
Heimdall - CollectiveAccess connector
#####################################

.. image:: https://img.shields.io/badge/license-AGPL3.0-informational?logo=gnu&color=success
   :target: https://www.gnu.org/licenses/agpl-3.0.html
.. image:: https://www.repostatus.org/badges/latest/suspended.svg
   :target: https://www.repostatus.org/#project-statuses
.. image:: https://img.shields.io/pypi/v/pyheimdall-collectiveaccess
   :target: https://pypi.org/project/pyheimdall-collectiveaccess/
   :alt: PyPI Version
.. image:: https://img.shields.io/badge/documentation-api-green
   :target: https://datasphere.readthedocs.io/projects/heimdall/
.. image:: https://gitlab.huma-num.fr/datasphere/heimdall/connectors/collectiveaccess/badges/main/pipeline.svg
   :target: https://gitlab.huma-num.fr/datasphere/heimdall/connectors/collectiveaccess/pipelines/latest
.. image:: https://gitlab.huma-num.fr/datasphere/heimdall/connectors/collectiveaccess/badges/main/coverage.svg
   :target: https://datasphere.gitpages.huma-num.fr/heimdall/connectors/collectiveaccess/coverage/index.html

*************
What is this?
*************

`Heimdall <https://datasphere.readthedocs.io/projects/heimdall/>`_ is a tool for converting more easily one or more databases from one format to another.
It leverages modules called "connectors", responsible for conversion of data between specific databases schemas and the HERA format.

This repository containes a connector to `CollectiveAccess <https://www.collectiveaccess.org/>`_ server sharing their data with the CollectiveAccess `Web Service API <https://manual.collectiveaccess.org/providence/developer/web_service_api.html>`_.



********************
Why should I use it?
********************

You can use this connector, along with the `pyheimdall software <https://gitlab.huma-num.fr/datasphere/heimdall/python>`_, to retrieve any data from a CollectiveAccess server.
You can then aggregate this data into your research corpus easily, for example using other Heimdall connectors.

| Take note, however that some legal restrictions might apply to data retrieved from CollectiveAccess.
| Plus, if at the end of your project, you share your data, please cite the original data properly (and reuploading it elsewhere is probably a bad idea, too).



*****************
How can I use it?
*****************

Setup
=====

This CollectiveAccess pyHeimdall connector is available as a `PyPI package <https://pypi.org/project/pyheimdall-collectiveaccess/>`_ named ``pyheimdall-colectiveaccess``.
You can install it using the `pip <https://pip.pypa.io/en/stable/>`_ package manager:

.. code-block:: bash

   pip install pyheimdall-collectiveaccess

You can use `pip <https://pip.pypa.io/en/stable/>`_ to either upgrade or uninstall this connector, too:

.. code-block:: bash

   pip install --upgrade pyheimdall-collectiveaccess
   pip uninstall pyheimdall-collectiveaccess

Usage
=====

.. code-block:: python

   import heimdall

   tree = heimdall.getDatabase(format='api:collectiveaccess', url=...)
   heimdall.createDatabase(tree, format=..., url=...)

Please note that you don't need to use ``pyheimdall-collectiveaccess`` functions directly.
As long as the package is installed on your system, pyHeimdall will automatically discover its features and allow you to use them as long as any other `default <https://gitlab.huma-num.fr/datasphere/heimdall/python/-/tree/main/src/heimdall/connectors>`_ or `external <https://gitlab.huma-num.fr/datasphere/heimdall/connectors>`_ connector.


*************
Is it tested?
*************

Of course!
Here's `the coverage report <https://datasphere.gitpages.huma-num.fr/heimdall/connectors/collectiveaccess/coverage/index.html>`_.


*********************
How can I contribute?
*********************

PyHeimdall welcomes any feedback or proposal.
Details can be accessed `here <https://gitlab.huma-num.fr/datasphere/heimdall/python/-/blob/main/CONTRIBUTING.rst>`_

*******
License
*******

`GNU Affero General Public License version 3.0 or later <https://choosealicense.com/licenses/agpl/>`_
