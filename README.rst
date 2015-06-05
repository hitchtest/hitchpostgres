HitchPostgres
=============

HitchPostgres is a plugin for the Hitch test framework that lets you run and
interact with Postgres in an isolated way (this does not interfere with
system postgres) as part of a test.


Use with Hitch
==============

Install like so::

    $ hitch install hitchpostgres


.. code-block:: python

        # Service definition in setup.py's setUp:
        postgres_user = services.PostgresUser("newpguser", "pguserpassword")

        self.services['Postgres'] = services.PostgresService(
            version="9.3.6",
            postgres_installation=services.PostgresInstallation(
                bin_directory = "/usr/lib/postgresql/9.3/bin/"
            ),
            users=[postgres_user, ],
            databases=[services.PostgresDatabase("databasename", newpguser), ]
        )


        # Interact using psql:
        self.services['Postgres'].databases[0].psql("-c", "SELECT * FROM yourtable;").run()
        [ Prints output ]

        self.services['Postgres'].databases[0].psql().run()
        [ Launches into postgres shell ]


See this service in action at the DjangoRemindMe_ project.


Features
========

* Creates data files from *scratch* using initdb in the .hitch directory. Complete isolation!
* Starts up on a separate thread in parallel with other serviecs when running with HitchServe_, so that your integration tests run faster.
* Run the server on whatever port you like.
* Version must be set explicitly to prevent "works on my machine" screw ups caused by different versions of Postgres being installed.


.. _HitchServe: https://github.com/crdoconnor/hitchserve
