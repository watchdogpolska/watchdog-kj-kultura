.. _static_pages:

**************************
Moduł podstron statycznych
**************************

Założenia
############

Ten moduł ma możliwość dodawania/edycje statycznych stron na portalu z poziomu panelu administracyjnego, a także wyświetlanie stron przez użytkownika. Wprowadzony mechanizm ma służyć prezentacji podstawowych informacji o projekcie, a także infografik i raportów.

Karta edycji podstron edycji zawiera nastepujące pola:

- Nazwa - Krótkie pole tekstowe, które określa tytuł strony
- Użytkownik - Pole wyboru, które określa użytkownika odpowiedzialnego za stronę.
- Rodzic - Opcjonalne pole wyboru, które określa stronę nadrzędną do edytowanej np. na potrzeby breadcrumbs,
- Treść - Duże pole tekstowe do wpisywania treści strony z edytorem WYSIWYG, a także obsługą mapy.
- Publiczna widoczność - Pole jednokrotnego zaznaczenia, które stwarza możliwość tymczasowego ukrycia stron.

Mechanizm podstron statycznych zapewnia:

* edycje wszystkich pól bazy ośrodka zgodnie z Karta tworzenia/edycji strony
* przycisk usunięcia podstrony z bazy
* możliwość tymczasowego ukrycia strony

Każdorazowo i automatycznie jest zapisywana data utworzenia i modyfikacja strony.

Dane testowe
############

Dla systemu stron statycznych możliwe jest w środowisku deweloperskim dynamicznie generowanych danych testowych. Wymagane jest wcześniejsze utworzenie użytkowników (zob. :ref:`users_fixtures` ). Następnie należy wywołać:

.. code-block:: bash

    $ python manage.py loadtestdata staticpages.Page:25

Architektura
############

Model
-----

.. automodule:: watchdog_kj_kultura.staticpages.models
   :members:

Znaczniki szablonów
-------------------

.. automodule:: watchdog_kj_kultura.staticpages.templatetags.staticpages_tags
   :members:

Widoki
------

.. automodule:: watchdog_kj_kultura.staticpages.views
   :members:

Panel administracyjny
---------------------

.. automodule:: watchdog_kj_kultura.staticpages.admin
   :members:
