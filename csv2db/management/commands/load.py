# load.py

from datetime import datetime as dt
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from csv2db.lib.map import Map

class Command(BaseCommand):
    help = 'load tables'

    def add_arguments(self, parser):
        parser.add_argument('--term',
            action='store_true',
            dest='term',
            default=False,
            help='load Term table')
        parser.add_argument('--type',
            action='store_true',
            dest='type',
            default=False,
            help='load Type table with short names')
        parser.add_argument('--typedev',
            action='store_true',
            dest='typedev',
            default=False,
            help='load Type table with intermediate names')

    def handle(self, *args, **options):
        try:
            if options['term']:
                self.stdout.write('%s begin... term_to_term' % dt.now())
                dev = 'term'
                Map.all_csv(self, dev)
                self.stdout.write('%s .....end term_to_term' % dt.now())
            elif options['type']:
                self.stdout.write('%s begin... type_to_type' % dt.now())
                dev = 'false'
                Map.all_csv(self, dev)
                self.stdout.write('%s .....end type_to_type' % dt.now())
            elif options['typedev']:
                self.stdout.write('%s begin... type_to_type dev' % dt.now())
                dev = 'true'
                Map.all_csv(self, dev)
                self.stdout.write('%s .....end type_to_type dev' % dt.now())
            else:
                self.stdout.write('%s begin... all_csv' % dt.now())
                dev = None
                Map.all_csv(self, dev)
                self.stdout.write('%s .....end all_csv' % dt.now())
        except Exception:
            raise CommandError('Failed to load table(s)')
