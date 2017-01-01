.. _deploy:

*********
Wdrożenie
*********

Heroku
#############

Jedną z akceptowalnych form wdrożenia jest wykorzystanie Heroku. Wymaga to kilku prostych kroków, które są szczegółowo przedstawione poniżej.

1. Utworzenie aplikacji
-----------------------

Po pierwsze należy utworzyć aplikacje i ustalić wartość podstawowych zmiennych:

.. code-block:: bash

    $ heroku create app_name
    $ heroku config:set DJANGO_SETTINGS_MODULE=config.settings.production
    $ heroku config:set DJANGO_SECRET_KEY=$(random_pass)
    $ heroku config:set DJANGO_ADMIN_URL=admin/
    $ heroku config:set BUILDPACK_URL=https://github.com/ddollar/heroku-buildpack-multi.git

2. API plików statycznych
----------------------------------

Następnie należy określić miejsce przechowywania plików statycznych (załączników itd.). Rekomenduje w tym zakresie wykorzystanie usługi e24files od `e24cloud <https://panel.e24cloud.com/referal/GuFfaD31>`_ , co pozwala na efektywne cenowe przechowywanie danych w Polsce:

.. code-block:: bash

    $ heroku config:set DJANGO_AWS_ACCESS_KEY_ID=**CUT**
    $ heroku config:set AWS_S3_ENDPOINT_URL="https://e24files.com/""
    $ heroku config:set AWS_S3_SIGNATURE_VERSION="s3"
    $ heroku config:set AWS_S3_CUSTOM_DOMAIN="**CUT**.e24files.com"
    $ heroku config:set DJANGO_AWS_SECRET_ACCESS_KEY=**CUT**
    $ heroku config:set DJANGO_AWS_STORAGE_BUCKET_NAME=watchdog-kj-kultura

Możliwe jest także wykorzystanie zwyczajnego Amazon S3 z wykorzystaniem ustawień

.. code-block:: bash

    $ heroku config:set DJANGO_AWS_ACCESS_KEY_ID=**CUT**
    $ heroku config:set AWS_S3_CUSTOM_DOMAIN="**CUT**.s3.eu-central-1.amazonaws.com"
    $ heroku config:set AWS_S3_ENDPOINT_URL=http://s3.amazonaws.com
    $ heroku config:set AWS_S3_REGION_NAME=eu-central-1
    $ heroku config:set AWS_S3_SIGNATURE_VERSION="s3v4"
    $ heroku config:set DJANGO_AWS_SECRET_ACCESS_KEY=**CUT**
    $ heroku config:set DJANGO_AWS_STORAGE_BUCKET_NAME=watchdog-kj-kultura

3. API wiadomości e-mail
------------------------

W kolejnym kroku należy wskazać dane operatora wiadomości e-mail. Wstępnie aplikacja jest skonfigurowana do obsługi Mailgun, zważywszy na swoją popularność:

.. code-block:: bash

    $ heroku config:set DJANGO_MAILGUN_API_KEY=key-xxxx
    $ heroku config:set MAILGUN_SENDER_DOMAIN=sandboxxx.mailgun.org

4. API monitorowania wyjątków
-----------------------------

Wymagane jest również, aby wskazać dane dostępowe DSN do instancji Sentry:

.. code-block:: bash

    $ heroku config:set DJANGO_SENTRY_DSN=http://...:...@sentry.jawne.info.pl/16 

5. Publikacja kodu
------------------

W tym miejscu dopiero warto umieścić kod źródłowy aplikacji na serwerze:

.. code-block:: bash

    $ git push heroku master

6. Baza danych
--------------

Potem należy stworzyć bazę danych i wprowadzić schemat bazy danych:

.. code-block:: bash

    $ heroku addons:create heroku-postgresql:hobby-dev
    $ heroku run python manage.py migrate

7. Cache
--------

Należy także aktywować cache:

.. code-block:: bash

    $ heroku addons:create rediscloud:30

8. Adres WWW
-------------

Jeżeli uruchamisz apliacje pod adresem innym niż ``kultura.kj.org.pl`` konieczne jest także zaakceptowanie domeny:

.. code-block:: bash

    $ heroku config:set DJANGO_ALLOWED_HOSTS="watchdog-kj-kultura.herokuapp.com"

9. Wyszukiwarka
---------------

Aby uruchomić wyszukiwarkę należy wywołać:

.. code-block:: bash

    $ heroku addons:create searchbox:starter
    $ heroku run python manage.py rebuild_index

10. Administrator aplikacji
---------------------------

Warto także utworzyć pierwszego użytkownika administracyjnego:

.. code-block:: bash

    $ heroku run python manage.py createsuperuser

.. _scheduler:

Planista
########

Niektóre komponenty powinny być uruchamiane cyklicznie niezależnie od interakcji użytkownika. W przypadku Heroku należy w takiej sytuacji wykorzystać:

.. code-block:: bash

    $ heroku addons:create scheduler:standard

W systemach Unix można wykorzystać program cron odpowiednio. Pamiętać należy jednak o ustawieniu odpowiednich zmiennych środowiskowych.

Powiadomienia
#############

W celu zapewnienia powiadomień z komponentu :ref:`organizations_requests` konieczne jest skonfigurowanie cyklicznego wywołania polecenia :ref:`send_requests_notifications`. Wystarczające winno być powiadomienie raz dziennie.

W Heroku wywołać:

.. code-block:: bash

    $ heroku addons:open scheduler

W nowo otwartym oknie wprowadzić następujące ustawienia:

.. figure:: _images/heroku_scheduler.png

Wyszukiwarka
############

W celu zapewnienia sprawnego wyszukiwania konieczne jest skonfigurowanie cyklicznej aktualizacji indeksu wyszukiwarki. Wystarczające powinno być indeksowanie co godzinę.

W przypadku Heroku należy wykorzystać :ref:`scheduler` z poleceniem ``python manage.py update_index --age=1`` wywoływanym co godzinę. Patrz także na szczegółową instrukcje dla `:ref:`Powiadomienia`. 
