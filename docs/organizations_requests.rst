.. _organizations_requests:

****************************
System zapytań do instytucji 
****************************

Założenia
---------

Moduł zapewnia możliwość składania wniosków o informację publiczną i petycji za pomocą prostego generatora. Jak również zapewnia automatyczne przypomnienia o złożonych zapytaniach, które zostały wysłane z pomocą systemu. System został dostosowany także do samodzielnego określenia nowej kategorii pism i algorytmu powiadomień.

Moduł wykorzystuje dane pochodzące z :ref:`organizations` w celu zidentyfikowania organizacji, które mogą być adresatami petycji.

Administracja
-------------


Polecenia zarządzania
#####################

.. _send_requests_notifications:

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
