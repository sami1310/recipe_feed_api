#django commands for the db to be availabe 
import time

from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        self.stdout.write("Waiting for the database to be ready")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavilable, waiting...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database is ready to connect'))
