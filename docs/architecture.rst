************
Architektura
************

Aplikacja została wykonana zaimplentowana w języku Python 3.5 z wsparciem frameworku `Django 1.10`_. Została zaprojektowania do wykorzystania bazy danych `PostgreSQL 9.5`_ z modułem PostGIS i silnika pełnotekstowej wyszukiwarki `Elasticsearch`_

.. _`Django 1.10`: https://docs.djangoproject.com/en/1.10/
.. _`PostgreSQL 9.5`: https://wiki.postgresql.org/wiki/What's_new_in_PostgreSQL_9.5
.. _`Elasticsearch`: https://www.elastic.co/

Zestawienie bibliotek Python wykorzystanych w projekcie:

.. literalinclude:: ../requirements/base.txt

Ponadto podczas pracy deweloperskiej są wykorzystane następujące biblioteki:

.. literalinclude:: ../requirements/dev.txt
