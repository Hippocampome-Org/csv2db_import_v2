# defs.py

from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from csv2db.models import EvidencePropertyTypeRel, Property, Type

class Command(BaseCommand):
    help = 'define types'

    def add_arguments(self, parser):
        parser.add_argument('table_id', nargs='+', type=int)

    def handle(self, *args, **options):
        try:
            type_row_objects = Type.objects.all().order_by('position')
            for type_row_object in type_row_objects:
                type_id = type_row_object.id
                excit_inhib = type_row_object.excit_inhib
                if excit_inhib == 'e':
                    excit_inhib = 'Excitatory'
                elif excit_inhib == 'i':
                    excit_inhib = 'Inhibitory'
                else:
                    excit_inhib = ''
                neuron_type_def = type_row_object.name + ' (nickname: ' + type_row_object.nickname + ')'
                try:
                    axons = ''
                    axons_count = 0
                    property_axons_in_row_objects = Property.objects.filter(subject='axons',predicate='in')
                    for property_axons_in_row_object in property_axons_in_row_objects:
                        property_axons_in_id = property_axons_in_row_object.id
                        try:
                            row_object = EvidencePropertyTypeRel.objects.filter(Property_id=property_axons_in_id,Type_id=type_id).first()
                            if row_object != None:
                                if axons_count == 0:
                                    axons += ' ' + property_axons_in_row_object.object
                                else:
                                    axons += ' and ' + property_axons_in_row_object.object
                                #axons_count += 1
                        except Exception:
                            pass
                    dendrites = ''
                    dendrites_count = 0
                    property_dendrites_in_row_objects = Property.objects.filter(subject='dendrites',predicate='in')
                    for property_dendrites_in_row_object in property_dendrites_in_row_objects:
                        property_dendrites_in_id = property_dendrites_in_row_object.id
                        try:
                            row_object = EvidencePropertyTypeRel.objects.filter(Property_id=property_dendrites_in_id,Type_id=type_id).first()
                            if row_object != None:
                                if dendrites_count == 0:
                                    dendrites += ' ' + property_dendrites_in_row_object.object
                                else:
                                    dendrites += ' and ' + property_dendrites_in_row_object.object
                                #dendrites_count += 1
                        except Exception:
                            pass
                    somata = ''
                    somata_count = 0
                    property_somata_in_row_objects = Property.objects.filter(subject='somata',predicate='in')
                    for property_somata_in_row_object in property_somata_in_row_objects:
                        property_somata_in_id = property_somata_in_row_object.id
                        try:
                            row_object = EvidencePropertyTypeRel.objects.filter(Property_id=property_somata_in_id,Type_id=type_id).first()
                            if row_object != None:
                                if somata_count == 0:
                                    somata += ' ' + property_somata_in_row_object.object
                                else:
                                    somata += ' or ' + property_somata_in_row_object.object
                                somata_count += 1
                        except Exception:
                            pass
                except Exception:
                    pass
                neuron_type_def += ' - ' + excit_inhib + ' neuron with axons in [' + axons + ' ], dendrites in [' + dendrites + ' ], and soma in [' + somata + ' ].'
                self.stdout.write('%s' % (neuron_type_def))
        except Exception:
            raise CommandError('Exception')
