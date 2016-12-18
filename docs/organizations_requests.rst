.. _organizations_requests:

****************************
System zapytań do instytucji 
****************************

Założenia
---------

Moduł zapewnia możliwość składania wniosków o informację publiczną i petycji za pomocą prostego generatora. Jak również zapewnia automatyczne przypomnienia o złożonych zapytaniach, które zostały wysłane z pomocą systemu. System został dostosowany także do samodzielnego określenia nowej kategorii pism i algorytmu powiadomień.

Moduł wykorzystuje dane pochodzące z :ref:`organizations` w celu zidentyfikowania organizacji, które mogą być adresatami petycji.

.. _organizations_requests_fixtures:

Dane testowe
-------------

Dla systemu zapytań do instytucji możliwe jest w środowisku deweloperskim dynamicznie generowanych danych testowych. Wymagane jest wcześniejsze utworzenie użytkowników (zob. :ref:`users_fixtures` ),  podziału terytorialnego (zob. :ref:`teryt_tree_fixtures`), a także organizacji (zob. :ref:`organizations_requests_fixtures` ). Następnie należy wywołać:

.. code-block:: bash

    $ python manage.py loadtestdata organizations_requests.Template:5 organizations_requests.Request:50

Należy odnotować, że brak jest możliwości wygenerowania automatycznych danych dla powiadomień. Należy w tym zakresie wykorzystać panel administracyjny.

Administracja
-------------

.. _send_requests_notifications:

Polecenia zarządzania
#####################

Dostępne jest `polecenie zarządzania Django`_, które odpowiada za mechanizm automatycznego powiadomienia o sprawach, które są dostępne. Aby zapewnić prawidłowe wysyłanie powiadomień konieczne jego cykliczne wywołanie. Zaleca się wywołanie nie rzadziej niż raz dziennie.

.. _`polecenie zarządzania Django`: https://docs.djangoproject.com/en/1.10/howto/custom-management-commands/

Użytkowanie zostało przedstawione poniżej:

.. program-output:: python ../manage.py send_requests_notifications -h

Architektura
------------

Model
#####

.. automodule:: watchdog_kj_kultura.organizations_requests.models
   :members:

Formularze
##########

.. automodule:: watchdog_kj_kultura.organizations_requests.forms
   :members:

Widoki
######

.. automodule:: watchdog_kj_kultura.organizations_requests.views
   :members:

Panel administracyjny
#####################

.. automodule:: watchdog_kj_kultura.organizations_requests.admin
   :members:

Moduły ekranu zarządzania
#########################

Dostępne są moduły kompatybilne z :ref:`grappelli:dashboard_api`.

.. automodule:: watchdog_kj_kultura.organizations_requests.dashboardmodules
   :members:
