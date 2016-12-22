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

Akcje w panelu administracyjnym
###############################

W panelu administracyjnym bazy instytucji kultury są dostępne pewne szczególne operacje, które warto wyróżnić.

Geokodowanie
------------

W przypadku  :class:`watchdog_kj_kultura.organizations.models.MetaCategory` możliwe jest automatyczne uzupełnienie pola pozycji współrzędnych geograficznych. Operacja ta wykorzystuje zewnętrzne usługi, których konfiguracja została przedstawiona w `Ustawienia`_. Ilość usług zależy od konfiguracji aplikacji. Pomijane są instytucje, które mają wypełnione informacje o pozycji.

Szczegółowo proces automatycznego uzupełniania pola pozycji został przedstawiony w następującym materiale:

.. raw:: html

    <video width="100%" controls><source src="_static/geocoding.webm"></video>

Import i eksport
----------------

Możliwe jest wyeksportowanie i importowanie m. in. :class:`watchdog_kj_kultura.organizations.models.Organization`. Stanowi to realizacje wymaganego w dokumentacji modułu importowania danych związanego z bazą ośrodków.

Podczas procesu importu należy ściśle przestrzegać nazw kolumn wskazanych przez aplikacje. Zaleca się w celu przygotowanie importu wykorzystanie dowolnego pliku eksportu jako szablonu do którego zostaną przeniesione dane. Pozwala to także na dokonanie selekcji danych, które mają być zaktualizowane (wypełniona kolumna ID), a które mają być zaktualizowane, aby uniknąć powtórzeń instytucji.

Największą pewność poprawności wczytania danych i kompatybilność zapewnia format CSV.

Ustawienia
##########

Niniejszy moduł wykorzystuje szereg ustawień Django (zob. :ref:`django:django-settings-module`), które zapewniają klucze API na potrzeby mechanizmu `Geokodowanie`_. Wprowadzenie ich nie jest obowiązkowe. Nie wprowadzenie danego klucza oznacza, że dany usługodawca nie będzie dostępny.

Dostępne ustawienia to:

GEOCODE_BAIDU_API_KEY
    Klucz API dla Baidu Maps v2 API. Dokumentacja API jest dostępna na stronie http://developer.baidu.com/map/webservice-geocoding.htm . Klucze API są zarządzane przez konsolę (http://lbsyun.baidu.com/apiconsole/key)

GEOCODE_BING_API_KEY
    Klucz API dla Bing Maps Locations API. Dokumentacja API jest dostępna na https://msdn.microsoft.com/en-us/library/ff701715.aspx .

GEOCODE_GOOGLE_API_KEY
    Klucz API dla Google Maps v3 API. Dokumentacja API jest dostępna na https://developers.google.com/maps/documentation/geocoding/ . Zarządzanie kluczami odbywa się przez konsolę ( https://code.google.com/apis/console ).

GEOCODE_YANDEX_API_KEY
    Klucz API dla Yandex. Dokumentacja API jest dostępna na http://api.yandex.com/maps/doc/geocoder/desc/concepts/input_params.xml . Zarządzanie kluczami odbywa się przez konsolę http://api.yandex.ru/maps/form.xml .


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

Akcje panelu administracyjnego
------------------------------

.. automodule:: watchdog_kj_kultura.organizations.admin_actions
   :members:
