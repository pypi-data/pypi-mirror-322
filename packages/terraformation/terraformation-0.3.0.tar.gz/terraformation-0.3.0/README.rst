tf
##

.. image:: https://git.shore.co.il/nimrod/tf/badges/main/pipeline.svg
    :target: https://git.shore.co.il/nimrod/tf/-/commits/main
    :alt: pipeline status

A simple Terraform wrapper to use variable definition files if they match the
workspace name.

Rationale
---------

With workspaces, one can use the same module in different environments with
minor changes like different domain name, size of a cluster, instance type.
One can use variable definition files to store the values for each workspace in
a dedicated file. This wrapper replaces the following:

.. code:: shell

   terraform workspace select prod
   terraform plan -var-files=prod.tfvars -out tfplan

to:

.. code:: shell

   terraform workspace select prod
   tf plan -out tfplan

Installation
------------

.. code:: shell

   python3 -m pip install terraformation

The wrapper is a single Python3 script with no external dependencies. If you
prefer, you can download the :code:`tf.py` and use that instead.

Usage
-----

Replace :code:`terraform` with :code:`tf`. In case there's a variable
definitions file (that ends with :code:`.tfvars`) that matches the current
workspace name (if the current workspace name is :code:`prod` and a file named
:code:`prod.tfvars` exists) than a :code:`-var-file=prod.tfvars` argument is
added to the relevant commands (like :code:`plan` and :code:`import`). All
other arguments are kept as they were. Similarly, if a directory exists with
the same name as the workspace, for all the files inside that directory that
end with :code:`.tfvars`, a :code:`-var-file` argument is added. For example:
:code:`-var-file=prod/a.tfvars` and :code:`-var-file=prod/b.tfvars`.

By default :code:`tf` invokes :code:`terraform`, but if you're using a
different tool (like `OpenTofu <https://opentofu.org/>`_ you can set the
:code:`TF_CLI` environment variable to that tool name. If you wish to know the
exact command :code:`tf` is running set the :code:`TF_DEBUG` environment
variable to :code:`1` and the command will printed before the it's invoked.

License
-------

This software is licensed under the MIT license (see the :code:`LICENSE.txt`
file).

Author
------

Nimrod Adar, `contact me <nimrod@shore.co.il>`_ or visit my `website
<https://www.shore.co.il/>`_. Patches are welcome via `git send-email
<http://git-scm.com/book/en/v2/Git-Commands-Email>`_. The repository is located
at: https://git.shore.co.il/nimrod/.
