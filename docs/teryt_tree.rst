.. _teryt_tree:

********************
Podział terytorialny
********************


.. _teryt_tree_fixtures:

Dane testowe
------------
Dostępna jest rządowa baza danych podziału terytorialnego. Aby ją wczytać należy - zgodnie z dokumentacją biblioteki `django-teryt-tree`_  - wywołać:

.. code-block:: bash

    wget "http://www.stat.gov.pl/broker/access/prefile/downloadPreFile.jspa?id=1110" -O TERC.xml.zip
    unzip TERC.xml.zip
    pip install lxml
    python manage.py load_teryt TERC.xml
    rm TERC.xml*

.. _`django-teryt-tree`: https://github.com/ad-m/django-teryt-tree
