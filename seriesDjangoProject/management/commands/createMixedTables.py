from django.db import connection
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    SQL_COMMAND_DROP ="""
        DROP TABLE IF EXISTS seriesDjangoProject_seriesuser;
        
    """
    SQL_COMMAND_CREATE="""
    CREATE TABLE seriesDjangoProject_seriesuser(
  id,
  user_id,
  serie_id
);"""
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(self.SQL_COMMAND_DROP)
            cursor.execute(self.SQL_COMMAND_CREATE)



