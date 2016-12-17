.. _main:

******************
Moduł podstawowy
******************

Założenia
#########

Moduł stanowi zbiór zróżnicowanych podstawowych komponentów. Zapewnia zarówno integracje dedykowanych komponentów z zewnętrznych, jak również bazę dla komponentów wbudowanych. Moduł zapewnia również możliwośc ustalenia ustawień dla stron działających z wykorzystaniem aplikacji.

Dostępna jest karta edycji ustawień, która określa ustawienia danej strony działającej z wykorzystaniem aplikacji. 

Dla każdej nowego obiektu ustawień dostępne są obecnie pola:

- Treść strony głównej - Duże pole tekstowe, które określa tekst powitalny występujący w nagłówku strony głównej.

Architektura
############

Model
-----

.. automodule:: watchdog_kj_kultura.main.models
   :members:

Widoki
------

.. automodule:: watchdog_kj_kultura.main.views
   :members:

Panel administracyjny
---------------------

.. automodule:: watchdog_kj_kultura.main.admin
   :members:

Procesorzy kontekstu
--------------------

.. automodule:: watchdog_kj_kultura.main.context_processors
   :members:
