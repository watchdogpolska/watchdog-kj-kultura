.. _installation:

******************
Instalacja
******************

Niniejsza aplikacja przedstawia uruchomienie aplikacji w środowisku deweloperskim. Nie obejmuje wdrożenia, co zostało przedstawione w sekcji :ref:`deploy` .

W niniejszej instrukcji został wykorzystany następujący ``Vagrantfile``:

.. code-block:: ruby

    Vagrant.configure("2") do |config|
      config.vm.box = "bento/xenial64"
      config.vm.hostname = "myprecise.box"
      config.vm.network :private_network, ip: "192.123.0.97"
      config.vm.network "forwarded_port", guest: 2000, host: 8080
    end

W pierwszej kolejności została uruchomie oficjalne repozytorium PostgreSQL zgodnie z `właściwa dokumentacją oprogramowania <https://wiki.postgresql.org/wiki/Apt>`_ :

.. code-block:: bash

    $ sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
    $ wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    $ sudo apt-get install update

Następnie dokonano instalacji poprawnych wersji oprogramowania:

.. code-block:: bash

    $ sudo apt-get install postgresql-9.5-postgis-2.2 postgresql-9.5 postgresql-server-dev-9.5

Została zainstalowana odpowiednia środowiska Python:

.. code-block:: bash

    $ sudo apt-get install python3.5-dev python3.5-dev python-pip virtualenv

Kod został pobrawny i wypakowany:

.. code-block:: bash

    $ wget https://github.com/watchdogpolska/watchdog-kj-kultura/archive/master.tar.gz
    $ tar xvzf master.tar.gz
    $ cd watchdog-kj-kultura-master

Zostało skonfigurowane wirtualne środowisko i zostały zainstalowane zależności:

.. code-block:: bash

    watchdog-kj-kultura-master$ virtualenv -p python3.5 env
    watchdog-kj-kultura-master$ source env/bin/activate;
    watchdog-kj-kultura-master$ pip install -r requirements/dev.txt;

Następnie została skonfigurowana baza danych odpowiednio:

.. code-block:: bash

    $ sudo -u postgres psql -c "create user $USER;"
    $ sudo -u postgres psql -c "create database watchdog_kj_kultura;"
    $ sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE watchdog_kj_kultura to $USER;"
    $ sudo -u postgres psql watchdog_kj_kultura -c "CREATE EXTENSION postgis;"
    watchdog-kj-kultura-master$ python manage.py migrate

Ostatecznie możliwe jest uruchomienie serwera WWW:

    watchdog-kj-kultura-master$ python manage.py 0.0.0.0:2000

Jest on dostępny po wywołaniu ``localhost:8080`` w przeglądarce.
