.. _deploy:

*********
Wdrożenie
*********

Heroku
#############

Jedną z akceptowalnych form wdrożenia jest wykorzystanie Heroku. Wymaga to kilku prostych kroków.

Po peirwsze należy utworzyć aplikacje i ustalić wartość podstawowych zmiennych:

.. code-block:: bash

    $ heroku create app_name
    $ heroku config:set DJANGO_SETTINGS_MODULE=config.settings.production
    $ heroku config:set DJANGO_SECRET_KEY=$(random_pass)
    $ heroku config:set DJANGO_ADMIN_URL=admin/
    $ heroku config:set BUILDPACK_URL=https://github.com/ddollar/heroku-buildpack-multi.git

Następnie należy określić miejsce przechowywania załączników. Rekomenduje w tym zakresie wykorzystanie usługi e24files od `e24cloud <https://panel.e24cloud.com/referal/GuFfaD31>`_ , co pozwala na efektywne cenowe przechowywanie danych w Polsce:

.. code-block:: bash

    $ heroku config:set DJANGO_AWS_ACCESS_KEY_ID=**CUT**
    $ heroku config:set DJANGO_AWS_S3_HOST=e24files.com
    $ heroku config:set DJANGO_AWS_SECRET_ACCESS_KEY=**CUT**
    $ heroku config:set DJANGO_AWS_STORAGE_BUCKET_NAME=watchdog-kj-kultura

W kolejnym kroku należy wskazać dane operatora wiadomości e-mail. Wstępnie aplikacja jest skonfigurowana do obsługi Mailgun, zważywszy na swoją popularność:

.. code-block:: bash

    $ heroku config:set DJANGO_MAILGUN_API_KEY=key-xxxx
    $ heroku config:set MAILGUN_SENDER_DOMAIN=sandboxxx.mailgun.org

Wymagane jest również, aby wskazać dane dostępowe DSN do instancji Sentry:

.. code-block:: bash

    $ heroku config:set DJANGO_SENTRY_DSN=http://...:...@sentry.jawne.info.pl/16 

W tym miejscu dopiero warto umieścić kod źródłowy aplikacji na serwerze:

.. code-block:: bash

    $ git push heroku master

Potem należy stworzyć bazę danych i wprowadzić schemat bazy danych:

.. code-block:: bash

    $ heroku addons:create heroku-postgresql:hobby-dev
    $ heroku run python manage.py migrate

Należy także aktywować cache:

.. code-block:: bash

    $ heroku addons:create rediscloud:30

Jeżeli uruchamisz apliacje pod adresem innym niż ``kultura.kj.org.pl`` konieczne jest także zaakceptowanie domeny:

.. code-block:: bash

    $ heroku config:set DJANGO_ALLOWED_HOSTS="watchdog-kj-kultura.herokuapp.com"

Aby uruchomić wyszukiwarkę należy wywołać:

.. code-block:: bash

    $ heroku addons:create searchbox:starter
    $ SEARCHURL=$(heroku config:get SEARCHBOX_URL | sed 's/^http/elasticsearch/g')
    $ heroku config:set SEARCH_URL="$SEARCHURL/haystack"

Warto także utworzyć pierwszego użytkownika administracyjnego:

.. code-block:: bash

    $ heroku run python manage.py createsuperuser

Konieczne może się okazać także zamieszczenie plików statycznych na serwerze multimediów:

.. code-block:: bash

    $ heroku run python manage.py collectstatic

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

W przypadku Heroku należy wykorzystać :ref:`scheduler`, a następnie wykorzystać polecenie ``python manage.py update_index --age=1`` wywoływane co godzinę. Patrz także na szczegółową instrukcje dla `:ref:`Powiadomienia`. 
