.. _calingen-cookbook-modify-templates-label:

################
Modify Templates
################

While **django-calingen** provides all relevant templates to make the app work
in a Django project, the templates are most likely not suitable for real
applications.

.. note::
  The templates were created during the development process and are meant to
  enable development in a minimal setup, as described in
  :ref:`calingen-dev-doc-setup-label`.

However, the app's templates can easily be overridden as described in the
official documentation:
:djangodoc:`How to override templates <howto/overriding-templates/>`.


.. _calingen-cookbook-modify-templates-overview-label:

*************************
URLs, Views and Templates
*************************

The following table provides a reference of the app's views, with their
corresponding URLs, the URL-names as specified in :mod:`calingen.urls` and the
template to be used.

.. include:: ../includes/templates_table.rst.txt
