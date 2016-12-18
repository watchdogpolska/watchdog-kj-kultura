.. _organizations:

**************************
Baza instytucji kultury
**************************

Założenia
#########

Moduł stanowi bazę grupująca ośrodki kultury. Zapewnia możliwości prezentacji, zapoznania się z listą oraz wyszukiwania istniejących w Polsce publicznych instytucji i ośrodków kultury finansowanych z środków publicznych, jak również danych adresowych i kontaktowych do ok. 9000 instytucji kultury w Polsce, danych dotyczących finansowania i zatrudnienia pozyskanych w ramach projektu dotąd od kilkuset podmiotów.

Moduł stanowi także źródło danych dla :ref:`organizations_requests`.

Dostępne są karty edycji dla:

* organizacji, która określa instytucje kultury, która będzie prezentowana na stronie,
* metakategorii, która definiuje rodzaj metadanych na temat organizacji,
* kategorii, która umożliwia ustalenie kategorii, którymi mogą być opisane organizacje.
  
Należy wyjaśnić, że dla każdej nowej metakategorii dostępne są pola:

- Nazwa - Określenie nazwy pola z metadanymi

- Klucz - Określenie unikalnego klucza, który będzie wykorzystywany podczas odwołania do tych metadanch w aplikacji z wykorzystaniem np. ``{{object.meta.KLUCZ}}``

- Użytkownik - Osoba odpowiedzialna za kryterium

Dla każdej organizacji wymagane są przez aplikacje następujące pola:

- Nazwa - Określenie nazwy organizacji

- E-mail - Określenie adresu e-mail instytucji, który będzie wykorzystywany m. in. w :ref:`organizations_requests`

- Jednostka podziału terytorialnego - Określenie jednostki podziału terytorialnego wykorzystanej w nawigacji według :ref:`teryt_tree`

- Użytkownik - Osoba odpowiedzialna za organizacje

Każdorazowo i automatycznie jest zapisywana data utworzenia i modyfikacja wpisu.

Dla każdej organizacji możliwe jest ustalenie metadanych. Wymaga to pierw wprowadzenia obiektu typu :class:`watchdog_kj_kultura.organizations.models.MetaCategory`, a wówczas podczas edycji organizacji pojawi się dodatkowe pole odpowiadające wartości metadanych. 

W celu wykorzystania danych zgromadzonych w polu metadanych należy dokonać edcji szablonów w kodzie źródłowym aplikacji poprzez zmiany w pliku ``/watchdog_kj_kultura/organizations/templates/organizations/organization_detail.html``. Podczas edycji odwołać się do metadanej wykorzystaniem np. ``{{object.meta.KLUCZ}}``. Możesz wykorzystać w tym celu język szablonów Django - :ref:`django:template-language-intro`.

.. _organizations_fixtures:

Dane testowe
############

Dla bazy instytucji kultury możliwe jest w środowisku deweloperskim dynamicznie generowanych danych testowych. Wymagane jest wcześniejsze utworzenie użytkowników (zob. :ref:`users_fixtures` ) i podziału terytorialnego (zob. :ref:`teryt_tree_fixtures`). Następnie należy wywołać:

.. code-block:: bash

    $ python manage.py loadtestdata organizations.Category:5 organizations.Organization:100

Należy odnotować, że tak utworzone dane pozbawione są informacji na temat obiektów :class:`watchdog_kj_kultura.organizations.models.MetaCategory`, a zatem także pola ``meta`` w :class:`watchdog_kj_kultura.organizations.models.Organization`. Organizacje są także prawdopodobnie ukryte.

Architektura
############

Model
-----

.. automodule:: watchdog_kj_kultura.organizations.models
   :members:

Formularze
----------

.. automodule:: watchdog_kj_kultura.organizations.forms
   :members:

Widoki
------

.. automodule:: watchdog_kj_kultura.organizations.views
   :members:

Panel administracyjny
---------------------

.. automodule:: watchdog_kj_kultura.organizations.admin
   :members:
