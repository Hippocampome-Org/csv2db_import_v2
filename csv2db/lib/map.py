# map.py

import codecs
import os
import re
from csv import DictReader, reader
from datetime import datetime as dt
from io import TextIOWrapper
from ..models import Article, ArticleAuthorRel, ArticleEvidenceRel, Attachment, Author, Conndata, ConndataFragmentRel
from ..models import ConnFragment, Evidence, EvidenceFragmentRel, Fragment, FragmentTypeRel, ingest_errors, Onhold, Synonym
from ..models import SynonymTypeRel, Term, Type, TypeTypeRel, potential_synapses, number_of_contacts,neurite
from ..models import neurite_quantified, attachment_neurite, attachment_connectivity, EvidencePropertyTypeRel
from ..models import SynproEvidencePropertyTypeRel, article_not_found, izhmodels_single, user
from ..models import SynproPropParcelRel, SynproTypeTypeRel, attachment_neurite_rar
from ..models import SynproCP, SynproCPTotal, SynproNOC, SynproNOCTotal, SynproNoPS, SynproNPSTotal
from ..models import SynproParcelVolumes, SynproSubLayers, SynproVolumesSelected
from ..models import phases, phases_fragment, attachment_phases, PhasesEvidenceTypeRel, PhasesEvidenceFragmentRel
from ..models import counts, counts_fragment, CountsEvidenceTypeRel, CountsEvidenceFragmentRel, Epdata
from ..models import attachment_counts, citations, Hippocampome_to_NMO, ModelDB_mapping
from .epdata_string_field import EpdataPropertyRecords, EpdataStringField
from .fragment_string_field import FragmentStringField
from .markerdata_string_field import MarkerdataStringField
from .morphdata_string_field import MorphdataPropertyRecords, MorphdataStringField
from .fpdata_string_field import FiringPatternStringField
from .synpro_string_field import SynproStringField


class Map:

    # reads specified csv file
    def __init__(self, request):
        self.request = request
        # self.rows = DictReader(TextIOWrapper(self.request.FILES['file'].file, encoding='UTF-8'))
        self.f = TextIOWrapper(self.request.FILES['file'].file, encoding='UTF-8')
        # look for morphdata file type and associated preheader lines to skip
        saw_morphdata = 0
        lines_to_skip = 0
        self.rows = reader(self.f, delimiter=',')
        for row in self.rows:
            if row[0] == '1.0 \\alpha':
                saw_morphdata = 1
                lines_to_skip = 1
            else:
                if saw_morphdata == 1:
                    if row[0] == 'Class Status':
                        break
                    lines_to_skip = lines_to_skip + 1
                else:
                    break
        self.f.seek(0)  # rewind the file
        if saw_morphdata == 1:  # skip preheader lines if morphdata
            while lines_to_skip > 0:
                next(self.f)  # read next line in file
                lines_to_skip = lines_to_skip - 1
        self.rows = DictReader(self.f)

    # from the command line, ingests the all.csv file and processes the contained list of files
    def all_csv(self, dev=None):
        module_dir = os.path.dirname(__file__)  # get current directory
        # example before sub: module_dir = '/Users/djh/wd/krasnow/csv2db/lib'
        module_dir = re.sub(r'csv2db/lib', r'static/csv2db/dat', module_dir)
        # example after sub : module_dir = '/Users/djh/wd/krasnow/static/csv2db/dat'
        if dev is None:
            all_csv_filename = 'all.csv'
            all_csv_file_path = os.path.join(module_dir, all_csv_filename)
            all_csv_file_buffer = open(all_csv_file_path, 'rb')
            self.rows = DictReader(TextIOWrapper(all_csv_file_buffer, encoding='UTF-8'))
            self.stdout.write('%s begin... %s' % (dt.now(), all_csv_file_path))
            Map.all_to_all(self)
            self.stdout.write('%s .....end %s' % (dt.now(), all_csv_file_path))
        elif (dev == 'false') or (dev == 'true'):
            type_csv_filename = 'type.csv'
            type_csv_file_path = os.path.join(module_dir, type_csv_filename)
            type_csv_file_buffer = open(type_csv_file_path, 'rb')
            self.rows = DictReader(TextIOWrapper(type_csv_file_buffer, encoding='UTF-8'))
            self.stdout.write('%s begin... %s' % (dt.now(), type_csv_file_path))
            Map.type_to_type(self, dev)
            self.stdout.write('%s .....end %s' % (dt.now(), type_csv_file_path))
        elif dev == 'term':
            term_csv_filename = 'term.csv'
            term_csv_file_path = os.path.join(module_dir, term_csv_filename)
            term_csv_file_buffer = open(term_csv_file_path, 'rb')
            self.rows = DictReader(TextIOWrapper(term_csv_file_buffer, encoding='UTF-8'))
            self.stdout.write('%s begin... %s' % (dt.now(), term_csv_file_path))
            Map.term_to_term(self)
            self.stdout.write('%s .....end %s' % (dt.now(), term_csv_file_path))
        else:
            pass

    # ingests the all.csv file and processes the contained list of files
    def all_to_all(self):
        markerdata_flag = 0
        process_order = []
        csv_filenames = []
        module_dir = os.path.dirname(__file__)  # get current directory
        # example before sub: module_dir = '/Users/djh/wd/krasnow/csv2db/lib'
        module_dir = re.sub(r'csv2db/lib', r'static/csv2db/dat', module_dir)
        # example after sub : module_dir = '/Users/djh/wd/krasnow/static/csv2db/dat'
        for row in self.rows:
            process_order.append(row['process order'])
            csv_filenames.append(row['csv filename'])
        for order, csv_filename in zip(process_order, csv_filenames):
            csv_file_path = os.path.join(module_dir, csv_filename)
            csv_file_buffer = open(csv_file_path, 'rb')
            # self.rows = DictReader(TextIOWrapper(csv_file_buffer, encoding='UTF-8'))
            self.f = TextIOWrapper(csv_file_buffer, encoding='UTF-8')
            # look for morphdata file type and associated preheader lines to skip
            saw_morphdata = 0
            lines_to_skip = 0
            self.rows = reader(self.f, delimiter=',')
            for row in self.rows:
                if row[0] == '1.0 \\alpha':
                    saw_morphdata = 1
                    lines_to_skip = 1
                else:
                    if saw_morphdata == 1:
                        if row[0] == 'Class Status':
                            break
                        lines_to_skip = lines_to_skip + 1
                    else:
                        break
            self.f.seek(0)  # rewind the file
            if saw_morphdata == 1:  # skip preheader lines if morphdata
                while lines_to_skip > 0:
                    next(self.f)  # read next line in file
                    lines_to_skip = lines_to_skip - 1
            # skip  3 lines for markerdata
            if csv_filename == 'markerdata.csv':
                lines_to_skip_marker = 3
                while lines_to_skip_marker > 0:
                    next(self.f)  # read next line in file
                    lines_to_skip_marker = lines_to_skip_marker - 1
            self.rows = DictReader(self.f)

            # material_method
            if csv_filename == 'material_method.csv':
                self.rows = reader(self.f, delimiter=',')

            try:
                self.stdout.write('%s begin... [%02s] %s' % (dt.now(), order, csv_file_path))
            except AttributeError:
                pass
            if order == '1':
                # dev = 'true'
                dev = 'false'
                Map.type_to_type(self, dev)
            elif order == '2':
                Map.notes_to_type(self)
            elif order == '3':
                Map.connection_to_connection(self)
            elif order == '4':
                Map.synonym_to_synonym(self)
            elif order == '5':
                Map.article_to_article(self)
            elif order == '6':
                Map.attachment_to_attachment(self)
            elif order == '7':
                Map.attachment_to_attachment(self)
            elif order == '8':
                Map.attachment_to_attachment(self)
            elif order == '9':
                FiringPatternStringField.attachment_fp_to_attachment_fp(self)
            elif order == '10':
                Map.fragment_to_fragment(self)
            elif order == '11':
                Map.fragment_to_fragment(self)
            elif order == '12':
                Map.fragment_to_fragment(self)
            elif order == '13':
                FiringPatternStringField.fp_fragment_to_fp_fragment(self)
            elif order == '14':
                markerdata_flag = Map.markerdata_to_markerdata(self, markerdata_flag)
            elif order == '15':
                Map.epdata_to_epdata(self)
            elif order == '16':
                Map.morphdata_to_morphdata(self)
            elif order == '17':
                FiringPatternStringField.definition_to_definition(self)
            elif order == '18':
                FiringPatternStringField.parameters_to_parameters(self)
            elif order == '19':
                FiringPatternStringField.materials_to_method(self)
            elif order == '20':
                Map.connfragment_to_connfragment(self)
            elif order == '21':
                Map.conndata_to_conndata(self)
            elif order == '22':
                Map.term_to_term(self)
            elif order == '23':
                Map.onhold_to_onhold(self)
            elif order == '24':
                Map.izhmodels_to_izhmodels(self)
            elif order == '25':
                Map.user_to_user(self)
            elif order == '26':
                Map.attachment_neurite(self)
            elif order == '27':
                Map.neurite_quantified(self)
            elif order == '28':
                Map.neurite(self)
            elif order == '29':
                Map.potential_synapses(self)
            elif order == '30':
                Map.number_of_contacts(self)
            elif order == '31':
                Map.attachment_connectivity(self)
            elif order == '32':
                self.synpro='nbyk'
                Map.synprofrag_to_synprofrag(self)
            elif order == '33':
                self.synpro='nbyk'
                Map.synprodata_to_synprodata(self)
            elif order == '34':
                self.synpro='nbym'
                Map.synprofrag_to_synprofrag(self)
            elif order == '35':
                self.synpro='nbym'
                Map.synprodata_to_synprodata(self)
            elif order == '36':
                Map.synpro_prop_parcel_rel(self)
            elif order == '37':
                Map.synpro_type_type_rel(self)
            elif order == '38':
                Map.attachment_neurite_rar(self)
            elif order == '39':
                Map.synpro_cp(self)
            elif order == '40':
                Map.synpro_cp_total(self)
            elif order == '41':
                Map.synpro_noc(self)
            elif order == '42':
                Map.synpro_noc_total(self)
            elif order == '43':
                Map.synpro_nops(self)
            elif order == '44':
                Map.synpro_nps_total(self)
            elif order == '45':
                Map.synpro_parcel_volumes(self)
            elif order == '46':
                Map.synpro_sub_layers(self)
            elif order == '47':
                Map.synpro_volumes_selected(self)
            elif order == '48':
                Map.phases(self)
            elif order == '49':
                Map.phases_fragment(self)
            elif order == '50':
                Map.attachment_phases(self)
            elif order == '51':
                Map.phases_evidence_type_rel(self)                
            elif order == '52':
                Map.phases_evidence_fragment_rel(self)
            elif order == '53':
                Map.counts(self)
            elif order == '54':
                Map.counts_fragment(self)
            elif order == '55':
                Map.counts_evidence_type_rel(self)                
            elif order == '56':
                Map.counts_evidence_fragment_rel(self)
            elif order == '57':
                Map.attachment_counts(self)
            elif order == '58':
                Map.citations(self)
            elif order == '59':
                Map.Hippocampome_to_NMO(self)
            elif order == '60':
                Map.ModelDB_mapping(self)
            else:
                pass
            try:
                self.stdout.write('%s .....end [%02s] %s' % (dt.now(), order, csv_file_path))
            except AttributeError:
                pass
            csv_file_buffer.close()

    # ingests article.csv and populates Article, ArticleAuthorRel, Author
    def article_to_article(self):  # and article_to_author
        pmid_isbn_reads = []
        first_page_reads = []
        name_list = []  # authors
        article_id = 0
        for row in self.rows:
            pmid_isbn = row['pmid_isbn'].replace('-', '')
            pmcid = row['pmcid']
            if len(pmcid) == 0:
                pmcid = None
            nihmsid = row['nihmsid']
            if len(nihmsid) == 0:
                nihmsid = None
            doi = row['doi']
            if len(doi) == 0:
                doi = None
            try:
                open_access = int(row['open_access'])
            except ValueError:
                open_access = None
            title = row['title']
            if len(title) == 0:
                title = None
            publication = row['publication']
            if len(publication) == 0:
                publication = None
            volume = row['volume']
            if len(volume) == 0:
                volume = None
            issue = row['issue']
            if len(issue) == 0:
                issue = None
            try:
                first_page = int(row['first_page'])
            except ValueError:
                first_page = None
            try:
                last_page = int(row['last_page'])
            except ValueError:
                last_page = None
            year = row['year']
            if len(year) == 0:
                year = None
            try:
                citation_count = int(row['citation_count'])
            except ValueError:
                citation_count = None
            row_object = Article(
                pmid_isbn=pmid_isbn,
                pmcid=pmcid,
                nihmsid=nihmsid,
                doi=doi,
                open_access=open_access,
                title=title,
                publication=publication,
                volume=volume,
                issue=issue,
                first_page=first_page,
                last_page=last_page,
                year=year,
                citation_count=citation_count
            )
            # check for dups in article.csv and only continue processing if new
            saw_article = 0
            for pmid_isbn_read, first_page_read in zip(pmid_isbn_reads, first_page_reads):
                if (pmid_isbn_read == pmid_isbn) and (first_page_read == first_page):
                    saw_article = 1
            if saw_article == 0:
                row_object.save()
                article_id = article_id + 1
                pmid_isbn_reads.append(pmid_isbn)
                first_page_reads.append(first_page)

                # article_to_author
                auth_string = row['authors']
                auth_list = auth_string.split(',')
                author_pos = 0
                for auth in auth_list:
                    name = auth.strip()
                    if name not in name_list:
                        row_object = Author(
                            name=name
                        )
                        row_object.save()
                        name_list.append(name)

                    # ArticleAuthorRel
                    row_object = ArticleAuthorRel(
                        Author_id=name_list.index(name) + 1,
                        Article_id=article_id,
                        author_pos=author_pos
                    )
                    row_object.save()
                    author_pos = author_pos + 1
                # end for auth in auth_list:
            # end if saw_article == 0:
        # end for row in self.rows:

    # end def article_to_article(self): # and article_to_author

    # ingests attachment_morph.csv, attachment_marker.csv, attachment_ephys.csv and populates Attachment, FragmentTypeRel
    def attachment_to_attachment(self):
        is_attachment_morph_csv = 0
        for row in self.rows:  # is this an attachment_morph.csv file or not
            try:
                priority = row['Representative?']
                is_attachment_morph_csv = 1
            except Exception:
                is_attachment_morph_csv = 0
            break
        self.f.seek(0)  # rewind the file
        self.rows = DictReader(self.f)
        for row in self.rows:
            try:
                # set cell_identifier
                cell_identifier = int(row['Cell Identifier'])
                # set quote_reference_id
                try:
                    quote_reference_id = int(row['Quote reference id'])
                except ValueError:
                    quote_reference_id = None
                # set name_of_file_containing_figure
                name_of_file_containing_figure = row['Name of file containing figure']
                if len(name_of_file_containing_figure) == 0:
                    name_of_file_containing_figure = None
                # set figure_table
                figure_table = row['Figure/Table']
                if is_attachment_morph_csv == 1:
                    if figure_table == 'figure':
                        figure_table = 'morph_figure'
                    elif figure_table == 'table':
                        figure_table = 'morph_table'
                # set parameter
                parameter = None
                try:
                    parameter = row['Parameter'].strip()
                    if len(parameter) == 0:
                        parameter = None
                    else:
                        # map Attachment parameter value to Fragment parameter value
                        parameters_attachment = (
                            'Vrest', 'Rin', 'tau', 'Vthresh', 'fAHP', 'APamplitude', 'APwidth', 'maxFR', 'sAHP', 'sag')
                        parameters_fragment = (
                            'Vrest', 'Rin', 'tau', 'Vthresh', 'fAHP', 'APampl', 'APwidth', 'maxFR', 'sAHP', 'sag')
                        p = 0
                        for parameter_attachment in parameters_attachment:
                            if parameter == parameter_attachment:
                                parameter = parameters_fragment[p]
                                break
                            else:
                                p = p + 1
                except Exception:
                    parameter = None
                # set protocol_tag
                try:
                    protocol_tag = row['Protocol_tag'].strip()
                    if len(protocol_tag) == 0:
                        protocol_tag = None
                except Exception:
                    protocol_tag = None
                # set interpretation_notes
                try:
                    interpretation_notes = row['Interpretation notes figures'].strip()
                    if len(interpretation_notes) == 0:
                        interpretation_notes = None
                except Exception:
                    interpretation_notes = None
                # write Attachment record
                row_object = Attachment(
                    cell_id=cell_identifier,
                    original_id=quote_reference_id,
                    name=name_of_file_containing_figure,
                    type=figure_table,
                    parameter=parameter,
                    protocol_tag=protocol_tag,
                    interpretation_notes=interpretation_notes
                )
                row_object.save()
                # write FragmentTypeRel row
                if is_attachment_morph_csv == 1:
                    priority = row['Representative?']
                    row_object = None
                    if priority == '1':
                        row_object = FragmentTypeRel(Type_id=cell_identifier, priority=1)
                    else:
                        row_object = FragmentTypeRel(Type_id=cell_identifier, priority=None)
                    row_object.save()
                else:
                    priority = None
            except ValueError:
                cell_identifier = None

    # ingests known_connections.csv and populates TypeTypeRel
    def connection_to_connection(self):
        for row in self.rows:
            try:
                Type1_id = int(row['Source_ID'])
                Type2_id = int(row['Target_ID'])
            except ValueError:
                continue
            connection_status_string = row['Connection?']
            connection_status = 'potential'
            if (connection_status_string == '1' or connection_status_string == '3' or connection_status_string == '4' or connection_status_string == '5'):
                connection_status = 'positive'
            elif (connection_status_string == '-1' or connection_status_string == '0'):
                connection_status = 'negative'
            connection_location_string = row['Layers']
            # connection_locations = connection_location_string.split(',') # was using ',' separator in original version of known_connections.csv
            connection_locations = connection_location_string.split(
                ';')  # now using ';' separator in new version of known_connections.csv
            for connection_location in connection_locations:
                try:
                    row_object = TypeTypeRel.objects.get(Type1_id=Type1_id, Type2_id=Type2_id,
                                                         connection_status=connection_status,
                                                         connection_location=connection_location.strip())
                except TypeTypeRel.DoesNotExist:
                    row_object = TypeTypeRel(Type1_id=Type1_id, Type2_id=Type2_id, connection_status=connection_status,
                                             connection_location=connection_location.strip())
                    row_object.save()

    # ingests conndata.csv and populate Conndata table
    def conndata_to_conndata(self):
        row_num = 1  # starting header offset
        for row in self.rows:
            row_num = row_num + 1
            try:
                Type1_id = int(row['Source_ID'])
                Type2_id = int(row['Target_ID'])
                connection_location_string = row['Layers'].strip()
                connection_status_string = row['Connection?'].strip()
                reference_id_string = row['RefIDs'].strip()
            except ValueError:
                continue
            if connection_status_string == '1':
                connection_status = 'positive'
            elif connection_status_string == '0':
                connection_status = 'negative'
            elif connection_status_string == '-1':
                connection_status = 'negative'
            elif connection_status_string == '4':
                connection_status = 'positive'
            elif connection_status_string == '5':
                connection_status = 'positive'
            elif len(connection_status_string) != 0:
                try:
                    row_object = ingest_errors.objects.get(field='Connection?', value=connection_status_string,
                                                           filename='conndata.csv', file_row_num=row_num,
                                                           comment='invalid connection value')
                except ingest_errors.DoesNotExist:
                    row_object = ingest_errors(field='Connection?', value=connection_status_string,
                                               filename='conndata.csv', file_row_num=row_num,
                                               comment='invalid connection value')
                    row_object.save()
                continue
            else:
                continue
            connection_locations = connection_location_string.split(';')
            references = reference_id_string.split(';')
            for connection_location in connection_locations:
                if len(connection_location) != 0:
                    connection_location = connection_location.strip()
                    # if not exists create connection
                    try:
                        row_object = Conndata.objects.get(Type1_id=Type1_id, Type2_id=Type2_id,
                                                          connection_status=connection_status,
                                                          connection_location=connection_location)
                    except Conndata.DoesNotExist:
                        row_object = Conndata(Type1_id=Type1_id, Type2_id=Type2_id, connection_status=connection_status,
                                              connection_location=connection_location)
                        row_object.save()
                    Connection_id = row_object.id
                    for reference in references:
                        if len(reference) != 0:
                            reference = reference.strip()
                            ConnFragment_id = None
                            # if reference is not a number 
                            if not (reference.isdigit()):
                                try:
                                    row_object = ingest_errors.objects.get(field='RefIDs', value=reference,
                                                                           filename='conndata.csv',
                                                                           file_row_num=row_num,
                                                                           comment='invalid reference value')
                                except ingest_errors.DoesNotExist:
                                    row_object = ingest_errors(field='RefIDs', value=reference, filename='conndata.csv',
                                                               file_row_num=row_num, comment='invalid reference value')
                                    row_object.save()
                                continue
                            # find whether given reference id exists in the database.
                            try:
                                row_object = ConnFragment.objects.get(original_id=reference)
                                ConnFragment_id = row_object.id
                            except ConnFragment.DoesNotExist:
                                try:
                                    row_object = ingest_errors.objects.get(field='RefIDs', value=reference,
                                                                           filename='conndata.csv',
                                                                           file_row_num=row_num,
                                                                           comment='missing reference in conn_fragment.csv')
                                except ingest_errors.DoesNotExist:
                                    row_object = ingest_errors(field='RefIDs', value=reference, filename='conndata.csv',
                                                               file_row_num=row_num,
                                                               comment='missing reference in conn_fragment.csv')
                                    row_object.save()
                            # Add mapping between connection and reference. If reference not found skip that mapping
                            if ConnFragment_id != None:
                                try:
                                    row_object = ConndataFragmentRel.objects.get(Conndata_id=Connection_id,
                                                                                 ConnFragment_id=ConnFragment_id)
                                except ConndataFragmentRel.DoesNotExist:
                                    row_object = ConndataFragmentRel(Conndata_id=Connection_id,
                                                                     ConnFragment_id=ConnFragment_id)
                                    row_object.save()

    # ingests conn_fragment.csv and populates ArticleEvidenceRel, Evidence, EvidenceFragmentRel, ConnFragment tables
    def connfragment_to_connfragment(self):
        row_num = 1  # starting header offset
        row_object = EvidenceFragmentRel.objects.last()
        fragment_id = row_object.Fragment_id + 1  # initialize from last fragment entry
        for row in self.rows:
            row_num = row_num + 1
            # set reference_id
            reference_id = None
            location_in_reference = None
            quote = None
            pmid_isbn = None
            article_id = None
            ref_id = row['RefID'].strip()
            try:
                reference_id = int(ref_id)
            except Exception:
                if len(ref_id) != 0:
                    try:
                        row_object = ingest_errors.objects.get(field='RefID', value=ref_id, file_row_num=row_num,
                                                               filename='conn_fragment.csv')
                    except ingest_errors.DoesNotExist:
                        row_object = ingest_errors(field='RefID', value=ref_id, filename='conn_fragment.csv',
                                                   file_row_num=row_num, comment='invalid reference value')
                        row_object.save()
                continue
            try:
                quote = row['Quote']
                if len(quote) == 0:
                    quote = None
            except Exception:
                quote = None
            try:
                location_in_reference = row['Location']
                if len(location_in_reference) == 0:
                    location_in_reference = None
            except Exception:
                location_in_reference = None
            pmid_isbn_value = row['PMID/ISBN'].strip()
            try:
                pmid_isbn = int(pmid_isbn_value.replace('-', ''))
            except Exception:
                try:
                    row_object = ingest_errors.objects.get(field='PMID/ISBN', value=pmid_isbn_value,
                                                           file_row_num=row_num, filename='conn_fragment.csv')
                except ingest_errors.DoesNotExist:
                    row_object = ingest_errors(field='PMID/ISBN', value=pmid_isbn_value, filename='conn_fragment.csv',
                                               file_row_num=row_num, comment='invalid pmid/isbn value')
                    row_object.save()
                pmid_isbn = None
            if pmid_isbn == None:
                article_id = None
            else:
                try:
                    row_object = Article.objects.filter(pmid_isbn=pmid_isbn).order_by('id').first()
                except Article.DoesNotExist:
                    article_id = None
                if row_object == None:
                    article_id = None
                else:
                    article_id = row_object.id
            if (article_id == None and pmid_isbn != None):
                # write new pmid_isbn to article_not_found
                try:
                    row_object = article_not_found.objects.get(pmid_isbn=pmid_isbn_value)
                except article_not_found.DoesNotExist:
                    row_object = article_not_found(pmid_isbn=pmid_isbn_value)
                    row_object.save()
            # set Fragment
            try:
                row_object = ConnFragment.objects.get(original_id=reference_id)
                continue
            except ConnFragment.DoesNotExist:
                row_object = ConnFragment(
                    id=fragment_id,
                    original_id=reference_id,
                    quote=quote,
                    page_location=location_in_reference,
                    pmid_isbn=pmid_isbn,
                )
                row_object.save()
                fragment_id = row_object.id
                row_object = Evidence()
                row_object.save()
                Evidence_id = row_object.id
                row_object = EvidenceFragmentRel(
                    Evidence_id=Evidence_id,
                    Fragment_id=fragment_id
                )
                row_object.save()
                row_object = ArticleEvidenceRel(
                    Article_id=article_id,
                    Evidence_id=Evidence_id
                )
                row_object.save()
                fragment_id = fragment_id + 1
            # end set fragment

    # ingests epdata.csv and populates ArticleEvidenceRel, ArticleSynonymRel, Epdata, EpdataEvidenceRel, Evidence, EvidenceEvidenceRel, EvidenceFragmentRel, EvidencePropertyTypeRel, Fragment, Property
    def epdata_to_epdata(self):
        EpdataPropertyRecords.save()
        for row in self.rows:
            try:
                EpdataStringField.parse_and_save(row)
            except Exception:
                break

    # ingests morph_fragment.csv, marker_fragment.csv, ep_fragment.csv and populates ArticleEvidenceRel, Evidence, EvidenceFragmentRel, Fragment, FragmentTypeRel(updates Fragment_id field)
    def fragment_to_fragment(self):
        fragment_id = 1
        for row in self.rows:  # is this a morph_fragment.csv file or a marker_fragment.csv file
            is_morph_fragment_csv = 0
            saw_protocol_reference = 0
            saw_ephys_parameters_extracted = 0
            try:
                protocol_reference = row['Protocol Reference']
                saw_protocol_reference = 1
                row_object = EvidenceFragmentRel.objects.last()
                fragment_id = row_object.Fragment_id + 1  # initialize from last morph_fragment.csv entry
            except Exception:
                try:
                    ephys_parameters_extracted = row['Ephys Parameters Extracted']
                    saw_ephys_parameters_extracted = 1
                    row_object = EvidenceFragmentRel.objects.last()
                    fragment_id = row_object.Fragment_id + 1  # initialize from last morph_fragment.csv entry
                except Exception:
                    is_morph_fragment_csv = 1
                    row_object = Evidence()
                    row_object.save()
                    fragment_id = 1
            break
        self.f.seek(0)  # rewind the file
        self.rows = DictReader(self.f)
        for row in self.rows:
            fragment_id = FragmentStringField.parse_and_save(row, fragment_id, saw_protocol_reference,
                                                             saw_ephys_parameters_extracted)
        # end for row in self.rows:
        # conditionally update Fragment_id fields in FragmentTypeRel
        if is_morph_fragment_csv == 1:
            FragmentTypeRel_row_objects = FragmentTypeRel.objects.all()
            for FragmentTypeRel_row_object in FragmentTypeRel_row_objects:
                try:
                    row_object = Attachment.objects.get(id=FragmentTypeRel_row_object.id)
                    original_id = row_object.original_id
                    row_object = Fragment.objects.get(original_id=original_id)
                    Fragment_id = row_object.id
                    row_object = FragmentTypeRel.objects.filter(id=FragmentTypeRel_row_object.id).update(
                        Fragment_id=Fragment_id)
                except Fragment.DoesNotExist:
                    row_object = None
        # end conditionally update Fragment_id fields in FragmentTypeRel

    # end def fragment_to_fragment(self):

    def synprofrag_to_synprofrag(self):
        fragment_id = None
        if (self.synpro=='nbyk'):
            fragment_id = 20000 # high enough to avoid overlaps
        elif (self.synpro=='nbym'):
            #row_object = EvidenceFragmentRel.objects.last()
            #fragment_id = row_object.Fragment_id + 1  # initialize from last morph_fragment.csv entry                        
            fragment_id = 30000 # high enough to avoid overlaps
            ''' This is reserved for future use
            fragment_id = row_object.Fragment_id
            row_object2 = SynproEvidenceFragmentRel.objects.last()
            fragment_id = fragment_id + row_object2 + 1  # initialize from last morph_fragment.csv entry                        
            '''
            # fragment_id = 1

        self.f.seek(0)  # rewind the file
        self.rows = DictReader(self.f)
        for row in self.rows:
            fragment_id = SynproStringField.parse_and_save(self, row, fragment_id)            

    # ingests markerdata.csv and populates ArticleSynonymRel, Evidence, EvidenceEvidenceRel, EvidenceMarkerdataRel, EvidencePropertyTypeRel, Markerdata, Property
    def markerdata_to_markerdata(self, markerdata_flag):
        count = 0
        for row in self.rows:
            try:
                MarkerdataStringField.parse_and_save(row, count, markerdata_flag)
                count = count + 1
            except Exception:
                break
        markerdata_flag = 1
        return markerdata_flag

    # ingests morphdata.csv and populates ArticleSynonymRel, EvidencePropertyTypeRel, Property
    def morphdata_to_morphdata(self):
        # intial lines skipped still actual rows
        count = 13
        MorphdataPropertyRecords.save()
        for row in self.rows:
            try:
                MorphdataStringField.parse_and_save(row, count)
                count = count + 1
            except Exception:
                break


    def synprodata_to_synprodata(self):
        if (self.synpro=='nbyk'):
            try:
                for row in self.rows:
                    try:
                        property_id=row['neurite_ID']
                    except Exception:
                        property_id=0
                    try:
                        type_id=row['type_ID']
                    except Exception:
                        type_id=0    
                    try:
                        source_id=row['source_id']
                    except Exception:
                        source_id=0
                    try:
                        target_id=row['target_id']
                    except Exception:
                        target_id=0
                    user_object = SynproEvidencePropertyTypeRel(
                        Evidence_id=row['evidence_ID'],
                        Property_id=property_id,
                        source_id=source_id,
                        target_id=target_id,
                        Type_id=type_id,
                        Article_id=row['Article_id'],
                        priority=row['priority'],
                        conflict_note=row['conflict_note'],
                        unvetted=row['unvetted'],
                        linking_quote=row['linking_quote'],
                        interpretation_notes=row['interpretation_notes'],
                        property_type_explanation=row['property_type_explanation'],
                        pc_flag=row['pc_flag'],
                        soma_pcl_flag=row['soma_pcl_flag'],
                        ax_de_pcl_flag=row['ax_de_pcl_flag'],
                        perisomatic_targeting_flag=row['perisomatic_targeting_flag'],
                        supplemental_pmids=row['supplemental_pmids']
                    )                
                    user_object.save()
            except Exception as e:
                print(e)
        if (self.synpro=='nbym'):
            try:
                for row in self.rows:
                    try:
                        property_id=row['property_ID']
                    except Exception:
                        property_id=0
                    try:
                        type_id=row['type_ID']
                    except Exception:
                        type_id=0    
                    try:
                        source_id=row['source_id']
                    except Exception:
                        source_id=0
                    try:
                        target_id=row['target_id']
                    except Exception:
                        target_id=0
                    user_object = SynproEvidencePropertyTypeRel(
                        Evidence_id=row['evidence_ID'],
                        Property_id=property_id,
                        source_id=source_id,
                        target_id=target_id,
                        Type_id=type_id,
                        Article_id=row['Article_id'],
                        priority=row['priority'],
                        conflict_note=row['conflict_note'],
                        unvetted=row['unvetted'],
                        linking_quote=row['linking_quote'],
                        interpretation_notes=row['interpretation_notes'],
                        property_type_explanation=row['property_type_explanation'],
                        pc_flag=row['pc_flag'],
                        soma_pcl_flag=row['soma_pcl_flag'],
                        ax_de_pcl_flag=row['ax_de_pcl_flag'],
                        perisomatic_targeting_flag=row['perisomatic_targeting_flag'],
                        supplemental_pmids=row['supplemental_pmids']
                    )                
                    user_object.save()
            except Exception as e:
                print(e)

    # ingests notes.csv and populates Type(updates notes field)
    def notes_to_type(self):
        module_dir = os.path.dirname(__file__)  # get current directory
        # notes_csv         = self.request.FILES['file'].name
        # notes_csv_split   = notes_csv.split('.')
        # notes_folder_name = notes_csv_split[0]
        notes_folder_name = 'packet_notes'
        notes_folder_path = os.path.join(module_dir, notes_folder_name)
        for row in self.rows:
            unique_ID = row['unique ID']
            try:
                Type_id = int(unique_ID)
            except ValueError:
                Type_id = None
            notes_file = row['Notes file']
            if notes_file != None:
                if len(notes_file) >= len('nnnn.txt'):
                    notes_folder_path_notes_file = notes_folder_path + '/' + notes_file
                    # example before: notes_folder_path_notes_file = '/Users/djh/wd/krasnow/csv2db/lib/packet_notes/1000.txt'
                    notes_folder_path_notes_file = re.sub(r'csv2db/lib', r'static/csv2db/dat',
                                                          notes_folder_path_notes_file)
                    # example after : notes_folder_path_notes_file = '/Users/djh/wd/krasnow/static/csv2db/dat/packet_notes/1000.txt'
                    try:
                        fs = codecs.open(notes_folder_path_notes_file, 'r', 'utf-8')
                        notes_txt = fs.read()
                        fs.close()
                        row_object = Type.objects.filter(id=Type_id).update(notes=notes_txt)
                    except Type.DoesNotExist:
                        row_object = None

    # ingests onhold_types_pmids.csv and populates Onhold
    def onhold_to_onhold(self):
        count = 2
        for row in self.rows:
            subregion = None
            type_id = None
            pmid_isbn = None
            name = None
            try:
                subregion = row['Subregion']
                # type id
                try:
                    type_id = int(row['Unique ID'])
                except ValueError:
                    type_id = None
                    row_object = ingest_errors(field='Unique ID', value=row['Unique ID'],
                                               filename='onhold_types_pmids.csv', file_row_num=count,
                                               comment='invalid Unique id value')
                    row_object.save()
                    continue

                # pmid isbn
                try:
                    name = row['Type'].strip()
                    pmid = row['PMID'].strip()
                    pmid_isbn = int(pmid.replace('-', ''))
                    # check if article exists for this pmid
                    try:
                        count_ids = Article.objects.filter(pmid_isbn=pmid_isbn).order_by('id').count()
                    except Article.DoesNotExist:
                        try:
                            row_object = article_not_found.objects.get(pmid_isbn=pmid_isbn)
                        except article_not_found.DoesNotExist:
                            row_object = article_not_found(pmid_isbn=pmid_isbn)
                            row_object.save()
                    if count_ids == 0:
                        try:
                            row_object = article_not_found.objects.get(pmid_isbn=pmid_isbn)
                        except article_not_found.DoesNotExist:
                            row_object = article_not_found(pmid_isbn=pmid_isbn)
                            row_object.save()
                except ValueError:
                    pmid_isbn = None
                    row_object = ingest_errors(field='PMID', value=row['PMID'], filename='onhold_types_pmids.csv',
                                               file_row_num=count, comment='invalid PMID value')
                    row_object.save()
                    continue

                row_object = Onhold(
                    Type_id=type_id,
                    subregion=subregion,
                    pmid_isbn=pmid_isbn,
                    name=name
                )
                row_object.save()
            except Exception as e:
                row_object = ingest_errors(field='', value='', filename='onhold_types_pmids.csv', file_row_num=count,
                                           comment=str(e))
                row_object.save()
            count = count + 1

    # ingests synonym.csv and populates Synonym, SynonymTypeRel
    def synonym_to_synonym(self):
        for row in self.rows:
            cited_names = row['Cited names']
            if len(cited_names) == 0:
                cited_names = None
            try:
                unique_id = int(row['Unique ID'])
            except ValueError:
                unique_id = None
            row_object = Synonym(
                name=cited_names,
                cell_id=unique_id
            )
            row_object.save()
            # write SynonymTypeRel record
            Synonym_id = row_object.id
            Type_id = row_object.cell_id
            row_object = SynonymTypeRel(Synonym_id=Synonym_id, Type_id=Type_id)
            row_object.save()

    # ingests term.csv and populates Term
    def term_to_term(self):
        for row in self.rows:
            parent = row['Parent']
            if len(parent) == 0:
                parent = None
            concept = row['Concept']
            if len(concept) == 0:
                concept = None
            term = row['Term']
            if len(term) == 0:
                term = None
            try:
                resource_rank = int(row['Resource Rank'])
            except ValueError:
                resource_rank = None
            resource = row['Resource']
            if len(resource) == 0:
                resource = None
            portal = row['Portal']
            if len(portal) == 0:
                portal = None
            repository = row['Repository']
            if len(repository) == 0:
                repository = None
            unique_id = row['Unique ID']
            if len(unique_id) == 0:
                unique_id = None
            definition_link = row['Definition Link']
            if len(definition_link) == 0:
                definition_link = None
            definition = row['Definition']
            if len(definition) == 0:
                definition = None
            protein_gene = row['protein_gene']
            if len(protein_gene) == 0:
                protein_gene = None
            human_rat = row['human_rat']
            if len(human_rat) == 0:
                human_rat = None
            control = row['control']
            if len(control) == 0:
                control = None
            row_object = Term(
                parent=parent,
                concept=concept,
                term=term,
                resource_rank=resource_rank,
                resource=resource,
                portal=portal,
                repository=repository,
                unique_id=unique_id,
                definition_link=definition_link,
                definition=definition,
                protein_gene=protein_gene,
                human_rat=human_rat,
                control=control
            )
            row_object.save()

    # ingests type.csv and populates Type(all but notes field)
    def type_to_type(self, dev):
        for row in self.rows:
            status = row['status']
            if status == 'active':
                id = int(row['id'])
                try:
                    position = int(row['position'])
                    position_HC_standard = int(row['position_HC_standard'])
                except ValueError:
                    position = None
                explanatory_notes = row['explanatory_notes']
                if len(explanatory_notes) == 0:
                    explanatory_notes = None
                subregion = row['subregion']
                if len(subregion) == 0:
                    subregion = None
                full_name = row['full_name']
                if len(full_name) == 0:
                    full_name = None
                intermediate_name = row['intermediate_name']
                if len(intermediate_name) == 0:
                    intermediate_name = None
                short_name = row['short_name']
                if len(short_name) == 0:
                    short_name = None
                CARLsim_name = row['CARLsim_name']
                if len(CARLsim_name) == 0:
                    CARLsim_name = None
                supertype = row['supertype']
                if len(supertype) == 0:
                    supertype = None
                type_subtype = row['type_subtype']
                if len(type_subtype) == 0:
                    type_subtype = None   
                if dev == 'true':  # overide for dev site
                    position = position_HC_standard
                    short_name = intermediate_name
                excit_inhib = row['excit_inhib']
                if len(excit_inhib) == 0:
                    excit_inhib = None          
#                ranks = int(row['Ranks'])
#                if len(ranks) == 0:
#                    ranks = None
                try:
                    ranks = int(row['Ranks'])
                except ValueError:
                    ranks = None
                try:
                    v2p0 = int(row['v2.0'])
                except ValueError:
                    v2p0 = 0
                mec_lec = row['pre_subregion_modifier']
                if len(mec_lec) == 0:
                    mec_lec = None          
                try:
                    interneuron_specific = int(row['interneuron_specific_flag'])
                except ValueError:
                    interneuron_specific = 0
                notes = None
                try:
                    row_object = Type.objects.get(id=id)
                    row_object = Type.objects.filter(id=id).update(position=position, nickname=short_name)
                except Type.DoesNotExist:
                    row_object = Type(
                        id=id,
                        position=position,
                        explanatory_notes=explanatory_notes,
                        subregion=subregion,
                        name=full_name,
                        nickname=short_name,
                        carlsim_name=CARLsim_name,
                        excit_inhib=excit_inhib,
                        supertype=supertype,
                        type_subtype=type_subtype,
                        status=status,
                        ranks=ranks,
                        v2p0=v2p0,
                        mec_lec=mec_lec,
                        interneuron_specific=interneuron_specific,
                        notes=notes
                    )
                    row_object.save()
            # end if status == 'active':
        # end for row in self.rows:
    # end def type_to_type(self):

    def izhmodels_to_izhmodels(self):
        try:
            for row in self.rows:
                izhmodels_single_object = izhmodels_single(
                    unique_id=row['uniqueID'].replace("-", ""),
                    subtype_id=row['subtypeID'],
                    name=row['name'],
                    preferred=row['preferred'],
                    k=row['k'],
                    a=row['a'],
                    b=row['b'],
                    d=row['d'],
                    C=row['C'],
                    Vr=row['Vr'],
                    Vt=row['Vt'],
                    Vpeak=row['Vpeak'],
                    Vmin=row['Vmin'],
                    k0=row['k0'],
                    a0=row['a0'],
                    b0=row['b0'],
                    d0=row['d0'],
                    C0=row['C0'],
                    Vr0=row['Vr0'],
                    Vt0=row['Vt0'],
                    Vpeak0=row['Vpeak0'],
                    Vmin0=row['Vmin0'],
                    k1=row['k1'],
                    a1=row['a1'],
                    b1=row['b1'],
                    d1=row['d1'],
                    C1=row['C1'],
                    Vr1=row['Vr1'],
                    Vt1=row['Vt1'],
                    Vpeak1=row['Vpeak1'],
                    Vmin1=row['Vmin1'],
                    G0=row['G0'],
                    P0=row['P0'],
                    k2=row['k2'],
                    a2=row['a2'],
                    b2=row['b2'],
                    d2=row['d2'],
                    C2=row['C2'],
                    Vr2=row['Vr2'],
                    Vt2=row['Vt2'],
                    Vpeak2=row['Vpeak2'],
                    Vmin2=row['Vmin2'],
                    G1=row['G1'],
                    P1=row['P1'],
                    k3=row['k3'],
                    a3=row['a3'],
                    b3=row['b3'],
                    d3=row['d3'],
                    C3=row['C3'],
                    Vr3=row['Vr3'],
                    Vt3=row['Vt3'],
                    Vpeak3=row['Vpeak3'],
                    Vmin3=row['Vmin3'],
                    G2=row['G2'],
                    P2=row['P2'])
                izhmodels_single_object.save()
        except Exception as e:
            print(e)

    def user_to_user(self):
        try:
            for row in self.rows:
                user_object = user(
                    password=row['password'],
                    permission=row['permission'])
                user_object.save()
        except Exception as e:
            print(e)

    def attachment_neurite(self):
        try:
            for row in self.rows:
                user_object = attachment_neurite(
                    authors=row['Authors'],
                    title=row['Title'],
                    journal_or_Book=row['Journal/Book'],
                    year=row['Year'],
                    PMID_or_ISBN=row['PMID/ISBN'],
                    cell_identifier=row['Cell Identifier'],
                    neurite=row['Neurite'],
                    neurite_ID=row['Neurite_ID'],
                    name_of_file_containing_figure=row['Name of file containing figure'],
                    reference_ID=row['Reference_ID']
                )
                user_object.save()
        except Exception as e:
            print(e)


    def neurite_quantified(self):
        try:
            for row in self.rows:
                user_object = neurite_quantified(
                    unique_ID=row['Unique_ID'],
                    subregion=row['Subregion'],
                    e_or_i=row['E/I'],
                    axonal_dendritic_pattern=row['Axonal-dendritic pattern (ax=1, de=2)'],
                    p=row['p'],
                    Projection_patterning=row['Projection patterning'],
                    hippocampome_neuronal_class = row['Hippocampome neuronal class'],
                    neurite = row['Neurite'],
                    neurite_ID=row['Neurite_ID'],
                    total_length=row['Total_length'],
                    filtered_total_length=row['Filtered_Total_length'],
                    percent_of_neurite_tree=row['%_of_neurite_tree'],
                    morphology_pattern=row['Morphology pattern'],
                    max_path_length=row['Max_path_length'],
                    min_path_length=row['Min_path_length'],
                    avg_path_length=row['Avg_path_length'],
                    convexhull = row['Convex Hull'],
                    reference_ID=row['Reference_ID'],
                    location_in_reference=row['Location in reference'],
                    reference=row['Reference'],
                    morphological_notes= row['Morphological notes']
                )
                user_object.save()
        except Exception as e:
            print(e)



    def neurite(self):
        try:
            for row in self.rows:
                user_object = neurite(
                    referenceID=row['ReferenceID'],
                    cellID=row['CellID'],
                    cellType=row['CellType'],
                    material_used=row['Material Used'],
                    location_in_reference=row['Location in reference'],
                    interpretation=row['Interpretation'],
                    authors=row['Authors'],
                    title=row['Title'],
                    journal_or_Book=row['Journal/Book'],
                    year=row['Year'],
                    PMID_or_ISBN=row['PMID/ISBN'],
                    pmid_isbn_page=row['pmid_isbn_page'],
                    area=row['Area'],
                    soma_state=row['Soma_state'],
                    soma=row['Soma'],
                    species=row['Species'],
                    strain=row['Strain'],
                    type=row['Type'],
                    gender=row['Gender'],
                    age=row['Age'],
                    slice=row['Slice'],
                    recording=row['Recording'],
                    labeled =row['Labeled'],
                    markers =row['Markers'],
                    input =row['Input'],
                    output   =row['Output'],
                    sections   =row['Sections'])
                user_object.save()
        except Exception as e:
            print(e)



    def potential_synapses(self):
        try:
            for row in self.rows:
                user_object = potential_synapses(
                    source_ID=row['Source_ID'],
                    source_Name=row['Source_Name'],
                    source_E_or_I=row['Source_E/I'],
                    target_ID=row['Target_ID'],
                    target_Name=row['Target_Name'],
                    target_E_or_I=row['Target_E/I'],
                    type=row['Type'],
                    layers=row['Layers'],
                    neurite=row['Neurite'],
                    neurite_id=row['Neurite ID'],
                    potential_synapses=row['Potential synapses'],
                    connection=row['Connection?'],
                    ES=row['ES'],
                    ES_PMID =row['ES PMID'],
                    refIDs                                     =row['RefIDs'],
                    notes                                      =row['Notes'],
                )
                user_object.save()
        except Exception as e:
            print(e)



    def number_of_contacts(self):
        try:
            for row in self.rows:
                user_object = number_of_contacts(
                    source_ID=row['Source_ID'],
                    source_Name=row['Source_Name'],
                    source_E_or_I=row['Source_E/I'],
                    target_ID=row['Target_ID'],
                    target_Name=row['Target_Name'],
                    target_E_or_I=row['Target_E/I'],
                    type=row['Type'],
                    layers=row['Layers'],
                    neurite=row['Neurite'],
                    neurite_id=row['Neurite ID'],
                    potential_synapses=row['Potential synapses'],
                    number_of_contacts=row['Number of contacts'],
                    probability=row['Probability'],
                    connection=row['Connection?'],
                    ES=row['ES'],
                    ES_PMID =row['ES PMID'],
                    refIDs                                     =row['RefIDs'],
                    notes                                      =row['Notes']
                )
                user_object.save()
        except Exception as e:
            print(e)



    def attachment_connectivity(self):
        try:
            for row in self.rows:
                user_object = attachment_connectivity(
                    RefID=row['RefID'],
                    source_ID=row['source_ID'],
                    source_class=row['source_class'],
                    target_ID=row['target_ID'],
                    target_class=row['target_class'],
                    Quote=row['Quote'],
                    Location=row['Location'],
                    Author=row['Author'],
                    Title=row['Title'],
                    Journal=row['Journal'],
                    Year=row['Year'],
                    PMID_or_ISBN=row['PMID/ISBN'],
                    pmid_isbn_page=row['pmid_isbn_page'],
                    UID=row['UID'],
                    Unknown=row['Unknown'],
                    Figure=row['Figure'],
                    HcoRefID=row['HcoRefID']
                )
                user_object.save()
        except Exception as e:
            print(e)

    def synpro_prop_parcel_rel(self):
        try:
            for row in self.rows:
                user_object = SynproPropParcelRel(
                    property_id=row['property_id'],
                    property_neurite=row['property_neurite'],
                    property_desc=row['property_desc'],
                    parcel=row['parcel'],
                    neurite_quant_neurite=row['neurite_quant_neurite']
                )
                user_object.save()
        except Exception as e:
            print(e)

    def synpro_type_type_rel(self):
        try:
            for row in self.rows:
                user_object = SynproTypeTypeRel(
                    type_name_short=row['type_name_short'],
                    type_name=row['type_name'],
                    neur_quant_type_name=row['neur_quant_type_name'],
                    type_nickname=row['type_nickname'],
                    type_id=row['type_id'],
                    subregion=row['subregion'],
                    type_name_new=row['type_name_new']
                )
                user_object.save()
        except Exception as e:
            print(e)

    def attachment_neurite_rar(self):
        try:
            for row in self.rows:
                pmid_isbn = int(row['PMID/ISBN'].replace('-','')) # remove dashes
                pmid_isbn = int(str(pmid_isbn).replace(' ','')) # remove spaces                
                user_object = attachment_neurite_rar(
                    authors=row['Authors'],
                    title=row['Title'],
                    journal_book=row['Journal/Book'],
                    year=row['Year'],
                    pmid_isbn=pmid_isbn,
                    neuron_id=row['Cell Identifier'],
                    neurite_name=row['Neurite'],
                    neurite_id=row['Neurite_ID'],
                    rar_file=row['Name of file containing figure'],
                    reference_id=row['Reference_ID']
                )
                user_object.save()
        except Exception as e:
            print(e)

    def synpro_cp(self):
        try:
            for row in self.rows:
                user_object = SynproCP(
                    source_id=row['source_id'],
                    target_id=row['target_id'],
                    subregion=row['subregion'],
                    parcel=row['parcel'],   
                    CP_mean=row['CP_mean'],
                    CP_std=row['CP_std']
                )
                user_object.save()
        except Exception as e:
            print(e)

    def synpro_cp_total(self):
        try:
            for row in self.rows:
                user_object = SynproCPTotal(
                    source_id=row['source_id'],
                    target_id=row['target_id'],
                    CP_mean_total=row['CP_mean_total'],
                    CP_stdev_total=row['CP_stdev_total'],   
                    parcel_count=row['parcel_count']
                )
                user_object.save()
        except Exception as e:
            print(e)

    def synpro_noc(self):
        try:
            for row in self.rows:
                user_object = SynproNOC(
                    source_id=row['source_id'],
                    target_id=row['target_id'],
                    subregion=row['subregion'],
                    parcel=row['parcel'],   
                    NC_mean=row['NC_mean'],
                    NC_std=row['NC_std']
                )
                user_object.save()
        except Exception as e:
            print(e)

    def synpro_noc_total(self):
        try:
            for row in self.rows:
                user_object = SynproNOCTotal(
                    source_id=row['source_id'],
                    target_id=row['target_id'],
                    NC_mean_total=row['NC_mean_total'],
                    NC_stdev_total=row['NC_stdev_total'],   
                    parcel_count=row['parcel_count']
                )
                user_object.save()
        except Exception as e:
            print(e)

    def synpro_nops(self):
        try:
            for row in self.rows:
                user_object = SynproNoPS(
                    source_id=row['source_id'],
                    target_id=row['target_id'],
                    subregion=row['subregion'],
                    parcel=row['parcel'],   
                    NPS_mean=row['NPS_mean'],
                    NPS_std=row['NPS_std']
                )
                user_object.save()
        except Exception as e:
            print(e)

    def synpro_nps_total(self):
        try:
            for row in self.rows:
                user_object = SynproNPSTotal(
                    source_id=row['source_id'],
                    target_id=row['target_id'],
                    NPS_mean_total=row['NPS_mean_total'],
                    NPS_stdev_total=row['NPS_stdev_total'],   
                    parcel_count=row['parcel_count']
                )
                user_object.save()
        except Exception as e:
            print(e)

    def synpro_parcel_volumes(self):
        try:
            for row in self.rows:
                user_object = SynproParcelVolumes(
                    subregion=row['subregion'],
                    parcel=row['parcel'],
                    volume=row['volume']
                )
                user_object.save()
        except Exception as e:
            print(e)

    def synpro_sub_layers(self):
        try:
            for row in self.rows:
                user_object = SynproSubLayers(
                    neuron_id=row['neuron_id'],
                    sub_layer=row['sub_layer']
                )
                user_object.save()
        except Exception as e:
            print(e)

    def synpro_volumes_selected(self):
        try:
            for row in self.rows:
                user_object = SynproVolumesSelected(
                    source_id=row['source_id'],
                    target_id=row['target_id'],
                    subregion=row['subregion'],
                    parcel=row['parcel'],
                    volume_1=row['volume_1'],
                    volume_2=row['volume_2'],
                    selected_volume=row['selected_volume']
                )
                user_object.save()
        except Exception as e:
            print(e)


    def phases(self):
        try:
            for row in self.rows:
                user_object = phases(
                    referenceID=row['Reference ID'],
                    cellID=row['Unique ID'],
                    cellType=row['Hippocampome Type'],
                    supertypeID=row['Supertype ID'],
                    supertype=row['Hippocampome Supertype'],
                    authors=row['Authors'],
                    title=row['Title'],
                    journal_or_Book=row['Journal/Book'],
                    year=row['Year'],
                    PMID_or_ISBN=row['PMID_or_ISBN'],
                    pmid_isbn_page=row['pmid_isbn_page'],
                    theta=row['Phase-CA1 (peak 0 deg)'],
                    thetaError=row['Theta Error'],
                    thetaErrorType=row['Theta Error Type'],
                    thetaN=row['Theta N'],
                    MVL=row['MVL'],
                    MVL_error=row['MVL Error'],
                    MVL_error_type=row['MVL Error Type'],
                    MVL_N=row['MVL N'],
                    gamma=row['Gamma Phase'],
                    gammaError=row['Gamma Error'],
                    gammaErrorType=row['Gamma Error Type'],
                    gammaN=row['Gamma N'],
                    epsilon=row['Epsilon Phase'],
                    epsilonError=row['Epsilon Error'],
                    epsilonErrorType=row['Epsilon Error Type'],
                    epsilonN=row['Epsilon N'],
                    ripple=row['Ripple Phase'],
                    rippleError=row['Ripple Error'],
                    rippleErrorType=row['Ripple Error Type'],
                    rippleN=row['Ripple N'],
                    SWR_ratio=row['SWR Ratio'],
                    SWR_ratioError=row['SWR Ratio Error'],
                    SWR_ratioErrorType=row['SWR Ratio Error Type'],
                    SWR_ratioN=row['SWR Ratio N'],
                    run_stop_ratio=row['Run/Stop Ratio'],
                    DS_ratio=row['DS Ratio'],
                    DS_ratioError=row['DS Ratio Error'],
                    DS_ratioErrorType=row['DS Ratio Error Type'],
                    DS_ratioN=row['DS Ratio N'],
                    firingRate=row['Firing Rate'],
                    firingRateError=row['Firing Rate Error'],
                    firingRateErrorType=row['Firing Rate Error Type'],
                    firingRateN=row['Firing Rate N'],
                    firingRateRank=row['Firing Rate Rank'],
                    firingRateNonBaseline=row['Firing Rate (non-baseline)'],
                    firingRateErrorNonBaseline=row['Firing Rate Error (non-baseline)'],
                    firingRateErrorTypeNonBaseline=row['Firing Rate Error Type (non-baseline)'],
                    firingRateN_NonBaseline=row['Firing Rate N (non-baseline)'],
                    firingRateRankNonBaseline=row['Firing Rate Rank (non-baseline)'],
                    Vrest=row['Vrest (mV)'],
                    VrestError=row['Vrest Error (mV)'],
                    VrestErrorType=row['Vrest Error Type'],
                    VrestN=row['Vrest N'],
                    tau=row['Tau (ms)'],
                    tauError=row['Tau Error (ms)'],
                    tauErrorType=row['Tau Error Type'],
                    tauN=row['Tau N'],
                    APthresh=row['APthresh (mV)'],
                    APthreshError=row['APthresh Error (mV)'],
                    APthreshErrorType=row['APthresh Error Type'],
                    APthreshN=row['APthresh N'],
                    fAHP=row['fAHP (mV)'],
                    fAHP_Error=row['fAHP Error (mV)'],
                    fAHP_ErrorType=row['fAHP Error Type'],
                    fAHP_N=row['fAHP N'],
                    APpeak_trough=row['APpeak-trough (ms)'],
                    APpeak_troughError=row['APpeak-trough Error (ms)'],
                    APpeak_troughErrorType=row['APpeak-trough Error Type'],
                    APpeak_troughN=row['APpeak-trough N'],
                    LFP_site=row['LFP site'],
                    recordingAssignment=row['Recording assignments'],
                    recordingMethod=row['Recording_method'],
                    species=row['Species'],
                    strain=row['Strain'],
                    gender=row['Gender'],
                    age=row['Age'],
                    ageType=row['Age_type'],
                    behavioralStatus=row['Behavioral status'],
                    dataMiningMethod=row['Data Mining Method'],
                    metadataRank=row['Metadata rank'])
                user_object.save()
        except Exception as e:
            print(e)


    def phases_fragment(self):
        try:
            for row in self.rows:
                user_object = phases_fragment(
                    referenceID=row['Reference ID'],
                    # referenceID=row['reference_id'],
                    cellID=row['Unique ID'],
                    location_in_reference=row['Location in reference'],
                    FTQ_ID=row['FTQ ID'],
                    material_used=row['Material Used'],
                    phase_parameter=row['Phase parameter'],
                    phase_parameter_ID=row['Phase parameter ID'],
                    authors=row['Authors'],
                    title=row['Title'],
                    journal=row['Journal'],
                    year=row['Year'],
                    PMID=row['PMID'],
                    pmid_isbn_page=row['pmid_isbn_page'])
                user_object.save()
        except Exception as e:
            print(e)


    def attachment_phases(self):
        try:
            for row in self.rows:
                user_object = attachment_phases(
                    authors=row['Authors'],
                    title=row['Title'],
                    journal_or_Book=row['Journal/Book'],
                    year=row['Year'],
                    PMID_or_ISBN=row['PMID/ISBN'],
                    cell_identifier=row['Unique ID'],
                    phase_parameter=row['Phase parameter'],
                    phase_parameter_ID=row['Phase parameter ID'],
                    name_of_file_containing_figure=row['Name of file containing figure'],
                    FTQ_ID=row['FTQ ID'],
                    figure_or_table=row['Figure/Table'],
                    reference_ID=row['Reference ID']
                )
                user_object.save()
        except Exception as e:
            print(e)

    def phases_evidence_type_rel(self):
        try:
            for row in self.rows:
                user_object = PhasesEvidenceTypeRel(
                    evidence_ID=row['evidence_ID'],
                    neurite_ID=row['neurite_ID'],
                    type_ID=row['type_ID'],
                    original_id=row['original_id'],
                    fragment_id=row['fragment_id'],
                    Article_id=row['Article_id'],
                    priority=row['priority'],
                    conflict_note=row['conflict_note'],
                    unvetted=row['unvetted'],
                    linking_quote=row['linking_quote'],
                    interpretation_notes=row['interpretation_notes'],
                    property_type_explanation=row['property_type_explanation'],
                    pc_flag=row['pc_flag'],
                    soma_pcl_flag=row['soma_pcl_flag'],
                    ax_de_pcl_flag=row['ax_de_pcl_flag'],
                    perisomatic_targeting_flag=row['perisomatic_targeting_flag'],
                    supplemental_pmids=row['supplemental_pmids']
                )
                user_object.save()
        except Exception as e:
            print(e)

    def phases_evidence_fragment_rel(self):
        try:
            for row in self.rows:
                user_object = PhasesEvidenceFragmentRel(
                    Evidence_id=row['Evidence_id'],
                    Fragment_id=row['Fragment_id']
                )
                user_object.save()
        except Exception as e:
            print(e)

    def counts(self):
        try:
            for row in self.rows:
                user_object = counts(
                    neuron_type=row['Neuron Type'],
                    unique_ID=row['Unique ID'],
                    counts=row['Count'],
                    lower_bound=row['Lower Bound'],
                    upper_bound=row['Upper Bound']
                )
                user_object.save()
        except Exception as e:
            print(e)

    def counts_fragment(self):
        try:
            for row in self.rows:
                user_object = counts_fragment(
                    referenceID=row['ReferenceID'],
                    cellID=row['CellID'],
                    variable=row['Variable'],
                    cell_type=row['CellType'],
                    material_used=row['Material Used'],
                    location_in_reference=row['Location in reference'],
                    measurement_equation=row['Measurement Equation'],
                    interpretation=row['Interpretation'],
                    authors=row['Authors'],
                    title=row['Title'],
                    journal=row['Journal/Book'],
                    year=row['Year'],
                    PMID=row['PMID/ISBN'],
                    pmid_isbn_page=row['pmid_isbn_page'],
                    species=row['Species'],
                    strain=row['Strain'],
                    sex=row['Sex'],
                    age_weight=row['Age or Weight']
                )
                user_object.save()
        except Exception as e:
            print(e)

    def counts_evidence_type_rel(self):
        try:
            for row in self.rows:
                user_object = CountsEvidenceTypeRel(
                    evidence_ID=row['evidence_ID'],
                    neurite_ID=row['neurite_ID'],
                    type_ID=row['type_ID'],
                    original_id=row['original_id'],
                    fragment_id=row['fragment_id'],
                    Article_id=row['Article_id'],
                    priority=row['priority'],
                    conflict_note=row['conflict_note'],
                    unvetted=row['unvetted'],
                    linking_quote=row['linking_quote'],
                    interpretation_notes=row['interpretation_notes'],
                    property_type_explanation=row['property_type_explanation'],
                    pc_flag=row['pc_flag'],
                    soma_pcl_flag=row['soma_pcl_flag'],
                    ax_de_pcl_flag=row['ax_de_pcl_flag'],
                    perisomatic_targeting_flag=row['perisomatic_targeting_flag'],
                    supplemental_pmids=row['supplemental_pmids']
                )
                user_object.save()
        except Exception as e:
            print(e)

    def counts_evidence_fragment_rel(self):
        try:
            for row in self.rows:
                user_object = CountsEvidenceFragmentRel(
                    Evidence_id=row['Evidence_id'],
                    Fragment_id=row['Fragment_id']
                )
                user_object.save()
        except Exception as e:
            print(e)

    def attachment_counts(self):
        try:
            for row in self.rows:
                user_object = attachment_counts(
                    authors=row['Authors'],
                    title=row['Title'],
                    journal_or_Book=row['Journal/Book'],
                    year=row['Year'],
                    PMID_or_ISBN=row['PMID/ISBN'],
                    cell_identifier=row['Cell Identifier'],
                    neuron_type=row['Neuron Type'],
                    variable=row['Variable'],
                    name_of_file_containing_figure=row['Name of file containing figure'],
                    reference_ID=row['Reference_ID']
                )
                user_object.save()
        except Exception as e:
            print(e)

    def citations(self):
        try:
            for row in self.rows:
                user_object = citations(
                    citation_ID=row['citation_ID'],
                    brief_citation=row['brief_citation'],
                    full_citation=row['full_citation']
                )
                user_object.save()
        except Exception as e:
            print(e)

    def Hippocampome_to_NMO(self):
        try:
            for row in self.rows:
                user_object = Hippocampome_to_NMO(
                    Hippocampome_ID=row['Hippocampome_ID'],
                    reason_for_inclusion=row['reason_for_inclusion'],
                    inclusion_flag=row['inclusion_flag'],
                    inclusion_caveat=row['inclusion_caveat'],
                    NMO_neuron_id=row['neuron_id'],
                    NMO_neuron_name=row['neuron_name'],
                    NMO_archive=row['archive'],
                    NMO_age_classification=row['age_classification'],
                    NMO_brain_region_1=row['brain_region_1'],
                    NMO_brain_region_2=row['brain_region_2'],
                    NMO_brain_region_3=row['brain_region_3'],
                    NMO_brain_region_4=row['brain_region_4'],
                    NMO_brain_region_5=row['brain_region_5'],
                    NMO_brain_region_6=row['brain_region_6'],
                    NMO_brain_region_7=row['brain_region_7'],
                    match_flag=row['match_flag'],
                    NMO_cell_type_1=row['cell_type_1'],
                    NMO_cell_type_2=row['cell_type_2'],
                    NMO_cell_type_3=row['cell_type_3'],
                    NMO_cell_type_4=row['cell_type_4'],
                    NMO_cell_type_5=row['cell_type_5'],
                    NMO_cell_type_6=row['cell_type_6'],
                    NMO_cell_type_7=row['cell_type_7'],
                    NMO_cell_type_8=row['cell_type_8'],
                    NMO_cell_type_9=row['cell_type_9'],
                    NMO_cell_type_10=row['cell_type_10'],
                    NMO_cell_type_11=row['cell_type_11'],
                    NMO_cell_type_12=row['cell_type_12'],
                    NMO_cell_type_13=row['cell_type_13'],
                    NMO_cell_type_14=row['cell_type_14'],
                    NMO_cell_type_15=row['cell_type_15'],
                    NMO_cell_type_16=row['cell_type_16'],
                    NMO_species=row['species'],
                    NMO_strain=row['strain'],
                    NMO_experiment_condition=row['experiment_condition'],
                    NMO_protocol=row['protocol'],
                    NMO_domain=row['domain'],
                    NMO_physical_integrity=row['physical_Integrity']
                )
                user_object.save()
        except Exception as e:
            print(e)

    def ModelDB_mapping(self):
        try:
            for row in self.rows:
                user_object = ModelDB_mapping(
                    Neuron_Type=row['Neuron_Type'],
                    Unique_ID=row['Unique_ID'],
                    Supertype_ID=row['Supertype_ID'],
                    ModelDB_Accession=row['ModelDB_Accession'],
                    PMID=row['PMID']
                )
                user_object.save()
        except Exception as e:
            print(e)

    def SynproIBD(self):
        try:
            for row in self.rows:
                user_object = SynproIBD(
                    source_id=row['source_id'],
                    source_name=row['source_name'],
                    source_e_or_i=row['source_e_or_i'],
                    target_id=row['target_id'],   
                    target_name=row['target_name'],
                    target_e_or_i=row['target_e_or_i']
                    type=row['type'],
                    subregion=row['subregion'],   
                    layer=row['layer'],
                    ibd=row['ibd']
                )
                user_object.save()
        except Exception as e:
            print(e)