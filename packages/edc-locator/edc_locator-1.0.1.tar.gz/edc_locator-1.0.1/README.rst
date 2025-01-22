|pypi| |actions| |codecov| |downloads|

edc-locator
-----------

Base classes for participant locator form and processes

Other edc modules will use ``get_locator_model`` and ``get_locator_model_cls`` to access the
subject locator model class. ``get_locator_model`` defaults to ``edc_locator.subject_locator``.
If you declare a custom locator model, add the name of the model to ``settings``
in label_lower format::

    # settings.py
    SUBJECT_LOCATOR_MODEL="myapp.subject_locator"

When declaring a custom locator model, you may only need to declare a ``proxy`` model class.

For example:

.. code-block:: python

    # models.py
    from edc_locator.models import SubjectLocator as BaseModel


    class SubjectLocator(BaseModel):
        class Meta:
            proxy = True
            verbose_name = "Subject Locator"
            verbose_name_plural = "Subject Locators"

.. code-block:: python

    # forms.py
    # use the form class from edc_locator

Use the modeladmin mixin class ``SubjectLocatorModelAdminMixin``.  Since you only want one
subject locator model accessible through admin in your EDC, unregister the default subject locator
before registering your custom modeladmin class.

.. code-block:: python

    # admin.py
    edc_locator_admin.unregister(DefaultSubjectLocator)

    @admin.register(SubjectLocator, site=intecomm_prn_admin)
    class SubjectLocatorAdmin(
        SubjectLocatorModelAdminMixin,
        SiteModelAdminMixin,
        ModelAdminSubjectDashboardMixin,
        SimpleHistoryAdmin,
    ):
        pass


.. |pypi| image:: https://img.shields.io/pypi/v/edc-locator.svg
    :target: https://pypi.python.org/pypi/edc-locator

.. |actions| image:: https://github.com/clinicedc/edc-locator/action/workflows/build.yml/badge.svg
  :target: https://github.com/clinicedc/edc-locator/action/workflows/build.yml

.. |codecov| image:: https://codecov.io/gh/clinicedc/edc-locator/branch/develop/graph/badge.svg
  :target: https://codecov.io/gh/clinicedc/edc-locator

.. |downloads| image:: https://pepy.tech/badge/edc-locator
   :target: https://pepy.tech/project/edc-locator
