from hitchtest import HitchPackage, utils
from hitchtest.environment import checks
from subprocess import check_output, call
from os.path import join, exists
from os import makedirs, chdir
import hitchpostgres


ISSUES_URL = "http://github.com/hitchtest/hitchpostgres/issues"

class PostgresPackage(HitchPackage):
    VERSIONS = [
        "9.5.0",
        "9.4.5", "9.4.4", "9.4.3", "9.4.2", "9.4.1", "9.4.0",
        "9.3.9", "9.3.8", "9.3.7", "9.3.6", "9.3.5", "9.3.4", "9.3.3", "9.3.2", "9.3.1", "9.3.0",
        "9.2.13", "9.2.12", "9.2.11", "9.2.10", "9.2.9", "9.2.8", "9.2.7", "9.2.6", "9.2.5", "9.2.4", "9.2.3", "9.2.2", "9.2.1", "9.2.0",
        "9.1.18", "9.1.17", "9.1.16", "9.1.15", "9.1.14", "9.1.13", "9.1.12", "9.1.11", "9.1.10",
        "9.1.9", "9.1.8", "9.1.7", "9.1.6", "9.1.5", "9.1.4", "9.1.3", "9.1.2", "9.1.1", "9.1.0",
        "9.0.22", "9.0.21", "9.0.20", "9.0.19", "9.0.18", "9.0.17", "9.0.16", "9.0.15", "9.0.14", "9.0.13", "9.0.12", "9.0.11",
        "9.0.10", "9.0.9", "9.0.8", "9.0.7", "9.0.6", "9.0.5", "9.0.4", "9.0.3", "9.0.2", "9.0.1", "9.0.0", "8.4.22", "8.4.21",
        "8.4.20", "8.4.19", "8.4.18", "8.4.17", "8.4.16", "8.4.15", "8.4.14", "8.4.13", "8.4.12", "8.4.11", "8.4.10",
        "8.4.9", "8.4.8", "8.4.7", "8.4.6", "8.4.5", "8.4.4", "8.4.3", "8.4.2", "8.4.1", "8.4.0", "8.3.23", "8.3.22", "8.3.21",
        "8.3.20", "8.3.19", "8.3.18", "8.3.17", "8.3.16", "8.3.15", "8.3.14", "8.3.13", "8.3.12", "8.3.11",
        "8.3.10", "8.3.9", "8.3.8", "8.3.7", "8.3.6", "8.3.5", "8.3.4", "8.3.3", "8.3.1", "8.3.0",
        "8.2.23", "8.2.22", "8.2.21", "8.2.20", "8.2.19", "8.2.18", "8.2.17", "8.2.16", "8.2.15", "8.2.14", "8.2.13", "8.2.12", "8.2.11", "8.2.10",
        "8.2.9", "8.2.7", "8.2.6", "8.2.5", "8.2.4", "8.2.3", "8.2.2", "8.2.1", "8.2.0",
        "8.1.23", "8.1.22", "8.1.21", "8.1.20", "8.1.19", "8.1.18", "8.1.17", "8.1.16", "8.1.15", "8.1.14", "8.1.13", "8.1.11", "8.1.10",
        "8.1.9", "8.1.8", "8.1.7", "8.1.6", "8.1.5", "8.1.4", "8.1.3", "8.1.2", "8.1.1", "8.1.0",
        "8.0.26", "8.0.25", "8.0.24", "8.0.23", "8.0.22", "8.0.21", "8.0.20", "8.0.19", "8.0.18", "8.0.17", "8.0.15", "8.0.14", "8.0.13", "8.0.12", "8.0.11", "8.0.10",
        "8.0.9", "8.0.8", "8.0.7", "8.0.6", "8.0.5", "8.0.4", "8.0.3", "8.0.2", "8.0.1", "8.0",
        "7.4.30", "7.4.29", "7.4.28", "7.4.27", "7.4.26", "7.4.25", "7.4.24", "7.4.23", "7.4.22", "7.4.21",
        "7.4.19", "7.4.18", "7.4.17", "7.4.16", "7.4.15", "7.4.14", "7.4.13", "7.4.12", "7.4.11", "7.4.10",
        "7.4.9", "7.4.8", "7.4.7", "7.4.6", "7.4.5", "7.4.4", "7.4.3", "7.4.2", "7.4.1", "7.4",
        "7.3.21", "7.3.20", "7.3.19", "7.3.18", "7.3.17", "7.3.16", "7.3.15", "7.3.14", "7.3.13", "7.3.12", "7.3.11", "7.3.10",\
        "7.3.9", "7.3.8", "7.3.7", "7.3.6", "7.3.5", "7.3.4", "7.3.3", "7.3.2", "7.3.1", "7.3",
        "7.2.8", "7.2.7", "7.2.6", "7.2.5", "7.2.4", "7.2.3", "7.2.2", "7.2.1", "7.2",
        "7.1.3", "7.1.2", "7.1.1", "7.1",
        "7.0.3", "7.0.2", "7.0.1", "7.0", "6.5", "6.4", "6.3", "6.2", "6.1", "6.0", "1.09", "1.08",
    ]

    name = "Postgres"

    def __init__(self, version="9.5.0", directory=None, bin_directory=None):
        super(PostgresPackage, self).__init__()
        self.version = self.check_version(version, self.VERSIONS, ISSUES_URL)

        if directory is None:
            self.directory = join(self.get_build_directory(), "postgresql-{}".format(self.version))
        else:
            self.directory = directory
        self.bin_directory = bin_directory

        checks.i_am_root(False)

        checks.packages(hitchpostgres.UNIXPACKAGES)

    def verify(self):
        version_output = check_output([self.postgres, "--version"]).decode('utf8')
        if self.version not in version_output:
            raise RuntimeError("Postgres version needed is {}, output is: {}.".format(self.version, version_output))

    def build(self):
        download_to = join(self.get_downloads_directory(), "postgresql-{}.tar.gz".format(self.version))
        utils.download_file(download_to, "https://ftp.postgresql.org/pub/source/v{0}/postgresql-{0}.tar.gz".format(self.version))
        if not exists(self.directory):
            makedirs(self.directory)
            utils.extract_archive(download_to, self.directory)
            full_directory = join(self.directory, "postgresql-{}".format(self.version))
            chdir(full_directory)
            call(["./configure", "--prefix={}".format(full_directory)])
            call(["make"])
            call(["make", "install"])
        self.bin_directory = join(self.directory, "postgresql-{}".format(self.version), "bin")

    @property
    def postgres(self):
        if self.bin_directory is None:
            raise RuntimeError("bin_directory not set.")
        return join(self.bin_directory, "postgres")

    @property
    def psql(self):
        if self.bin_directory is None:
            raise RuntimeError("bin_directory not set.")
        return join(self.bin_directory, "psql")

    @property
    def pg_dump(self):
        if self.bin_directory is None:
            raise RuntimeError("bin_directory not set.")
        return join(self.bin_directory, "pg_dump")

    @property
    def pg_restore(self):
        if self.bin_directory is None:
            raise RuntimeError("bin_directory not set.")
        return join(self.bin_directory, "pg_restore")

    @property
    def initdb(self):
        if self.bin_directory is None:
            raise RuntimeError("bin_directory not set.")
        return join(self.bin_directory, "initdb")
