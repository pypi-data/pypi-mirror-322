|pypi| |actions| |coverage|

edc-list-data
-------------

Populate list data and other static model data on ``Django`` startup.

To install add ``edc_list_data.apps.AppConfig`` to your `INSTALLED_APPS`, then create a ``list_data.py`` in the root of your app.

Most commonly used to populate M2M data known here as ``list_data``. M2M field models should use the ``ListModelMixin``.

The list models are populated using a ``post_migrate`` signal. Once everything is configured
or after changes are made, you need to run ``python manage.py migrate``.

For example:

.. code-block:: python

	class Antibiotic(ListModelMixin, BaseUuidModel):

	    class Meta(ListModelMixin.Meta):
	        pass


An example ``list_data.py``:


.. code-block:: python

	from edc_constants.constants import OTHER

	list_data = {
	    'my_lists_app.antibiotic': [
	        ('flucloxacillin', 'Flucloxacillin'),
	        ('gentamicin', 'Gentamicin'),
	        ('ceftriaxone', 'Ceftriaxone'),
	        ('amoxicillin_ampicillin', 'Amoxicillin/Ampicillin'),
	        ('doxycycline', 'Doxycycline'),
	        ('erythromycin', 'Erythromycin'),
	        ('ciprofloxacin', 'Ciprofloxacin'),
	        (OTHER, 'Other, specify')
	    ],
	}

Now run:
    >>> python manage.py migrate


The list data will be populated in the order in which the list items are declared.

See also call to ``site_list_data.autodiscover`` and ``site_list_data.load_data`` called in ``edc_list_data.apps.AppConfig``
using a ``post_migrate`` signal.



.. |pypi| image:: https://img.shields.io/pypi/v/edc-list-data.svg
    :target: https://pypi.python.org/pypi/edc-list-data

.. |actions| image:: https://github.com/clinicedc/edc-list-data/actions/workflows/build.yml/badge.svg
  :target: https://github.com/clinicedc/edc-list-data/actions/workflows/build.yml

.. |coverage| image:: https://coveralls.io/repos/github/clinicedc/edc-list-data/badge.svg?branch=develop
    :target: https://coveralls.io/github/clinicedc/edc-list-data?branch=develop
