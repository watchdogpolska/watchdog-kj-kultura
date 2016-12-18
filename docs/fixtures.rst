.. _fixtures:

************
Dane testowe
************

W celu szybkiego rozruchu aplikacji możliwe jest wygenerowanie lub wczytanie pewnych danych początkowych. Szczegółowe instrukcje zostały przedstawione w modułach właściwych modułów.

.. _users_fixtures:

Użytkownicy
-----------

Dla bazy możliwe jest w środowisku deweloperskim dynamicznie wygenerowanych danych na temat użytkowników:

.. code-block:: bash

    $ python manage.py loadtestdata users.User:25

Warto także zwrócić uwagę na utworzenie konta administratora opisane w :ref:`deploy`.


