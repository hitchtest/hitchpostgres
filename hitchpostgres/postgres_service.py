from hitchserve import Service, HitchException
from os.path import join
import signal
import shutil
import sys


# TODO: Add list of versions

class PostgresInstallation(object):
    def __init__(self, bin_directory=None, exec_initdb="initdb", exec_postgres="postgres", exec_psql="psql", exec_pgdump="pg_dump", exec_pgrestore="pg_restore"):
        if bin_directory is None:
            self.exec_initdb = exec_initdb
            self.exec_postgres = exec_postgres
            self.exec_psql = exec_psql
            self.exec_pgdump = exec_pgdump
            self.exec_pgrestore = exec_pgrestore
        else:
            self.exec_initdb = join(bin_directory, exec_initdb)
            self.exec_postgres = join(bin_directory, exec_postgres)
            self.exec_psql = join(bin_directory, exec_psql)
            self.exec_pgdump = join(bin_directory, exec_pgdump)
            self.exec_pgrestore = join(bin_directory, exec_pgrestore)

class PostgresDatabase(object):
    def __init__(self, name, owner, dump=None):
        self.name = name
        self.owner = owner
        self.dump = dump

    def psql(self, command=None):
        """Run PSQL command on this database."""
        return self.database_of.psql(command=command, database=self.name)

    def pg_dump(self, filename=None):
        """Dump this database to 'filename'."""
        return self.database_of.pg_dump(filename, database=self.name)

    @property
    def database_of(self):
        return self._database_of

    @database_of.setter
    def database_of(self, value):
        self._database_of = value

class PostgresUser(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

class PostgresService(Service):
    stop_signal = signal.SIGQUIT

    def __init__(self, version, port=15432, encoding='UTF-8', locale='en_US', pgdata=None, postgres_installation=None, users=None, databases=None, **kwargs):
        self.version = version
        self.encoding = encoding
        self.locale = locale
        self.port = port
        self.pg_installation = PostgresInstallation() if None else postgres_installation
        self.users = users
        self.databases = databases
        self.pgdata = pgdata
        kwargs['log_line_ready_checker'] = lambda line: "database system is ready to accept connections" in line
        super(PostgresService, self).__init__(**kwargs)

    @property
    def databases(self):
        return self._databases

    @databases.setter
    def databases(self, value):
        self._databases = value
        if self.databases is not None:
            for database in self._databases:
                database.database_of = self

    @property
    def pgdata(self):
        if self._pgdata is None:
            return join(self.service_group.hitch_dir.hitch_dir, 'pgdata')
        else:
            return self._pgdata

    @pgdata.setter
    def pgdata(self, value):
        self._pgdata = value

    @Service.command.getter
    def command(self):
        if self._command is None:
            return [self.pg_installation.exec_postgres,
                '-p', str(self.port),
                '-D', self.pgdata,
                '--unix_socket_directories=' + self.pgdata,
                "--log_destination=stderr",]
        else:
            return self._command

    def setup(self):
        self.log("Checking postgresql version...")
        version_output = self.subcommand(self.pg_installation.exec_postgres, "--version").run(check_output=True)
        if self.version not in version_output:
            raise HitchException("Postgres version needed is {}, output is: {}.".format(self.version, version_output))
        self.log("Initializing postgresql database...")
        shutil.rmtree(self.pgdata, ignore_errors=True)
        # TODO : Put back encoding + locale
        self.subcommand(self.pg_installation.exec_initdb, self.pgdata).run()

    def poststart(self):
        self.log("Creating users and databases...")
        for user in self.users:
            self.psql(
                """create user {} with password '{}';""".format(user.username, user.password)
            ).run()
        for database in self.databases:
            self.psql(
                """create database {} with owner {};""".format(
                    database.name, database.owner.username
                )
            ).run()
            if database.dump is not None:
                self.psql(database=database.name, filename=database.dump).run()

    def psql(self, command=None, database="template1", filename=None):
        """Run PSQL command."""
        fullcmd = [
            self.pg_installation.exec_psql, "-d", database, "-p", str(self.port), "--host", self.pgdata,
        ]
        if command is not None:
            fullcmd = fullcmd + ["-c", command, ]
        if filename is not None:
            fullcmd = fullcmd + ["-f", filename, ]
        return self.subcommand(*fullcmd)

    def pg_dump(self, filename=None, database="template1"):
        """Dump a database."""
        fullcmd = [
            self.pg_installation.exec_pgdump, "-d", database, "-p",
            str(self.port), "--host", self.pgdata,
        ]
        if filename is not None:
            fullcmd = fullcmd + ["-f", filename, ]
        return self.subcommand(*fullcmd)

    def pg_restore(self, filename, database="template1"):
        """Restore a database."""
        fullcmd = [
            self.pg_installation.exec_pgrestore, "-d", database, "-p",
            str(self.port), "--host", self.pgdata, filename
        ]
        return self.subcommand(*fullcmd)
