HitchPostgres
=============

HitchPostgres is a plugin for the Hitch test framework that lets you run and
interact with Postgres in an isolated way as part of a test.

Before starting the service, it runs the initdb command to create all required
data files for a postgresql database in the .hitch directory. This means that
whatever you do, you will not interfere with the system postgres files. The
system postgres does not even have to be running.

After starting the service, it creates any users and databases specified that
may be required for your app to start.

During the test it provides convenience functions psql, pg_dump and pg_restore
so that you can interact with the database using IPython or in your test.


Use with Hitch
==============

Install like so::

    $ hitch install hitchpostgres


.. code-block:: python

        # Service definition in engine's setUp:
        postgres_user = hitchpostgres.PostgresUser("newpguser", "pguserpassword")

        self.services['Postgres'] = hitchpostgres.PostgresService(
            version="9.3.6",                                                            # Mandatory
            port=15432,                                                                 # Optional (default: 15432)
            postgres_installation=hitchpostgres.PostgresInstallation(                   # Optional (default: assumes postgres commands are on path)
                bin_directory = "/usr/lib/postgresql/9.3/bin/"
            ),
            users=[postgres_user, ],                                                    # Optional (default: no users)
            databases=[hitchpostgres.PostgresDatabase("databasename", newpguser), ]     # Optional (default: no databases)
            pgdata=None,                                                                # Optional location for pgdata dir (default: put in .hitch)
        )


        # Interact using psql:
        self.services['Postgres'].databases[0].psql("-c", "SELECT * FROM yourtable;").run()
        [ Prints output ]

        self.services['Postgres'].databases[0].psql().run()
        [ Launches into postgres shell ]


See this service in action in the DjangoRemindMe_ project.


Features
========

* Creates data files from scratch using initdb in the .hitch directory. Complete isolation of data from system postgres.
* Starts up on a separate thread in parallel with other services when running with HitchServe_, so that your integration tests run faster.
* Run the server on whatever port you like.
* Version set explicitly to prevent "works on my machine" screw ups caused by running different versions of Postgres.


.. _HitchServe: https://github.com/hitchtest/hitchserve
.. _DjangoRemindMe: https://github.com/hitchtest/django-remindme
