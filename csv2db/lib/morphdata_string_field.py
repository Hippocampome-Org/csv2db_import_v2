# morphdata_string_field.py

import re
from ..models import ArticleEvidenceRel, ArticleSynonymRel, EvidenceFragmentRel, EvidencePropertyTypeRel, Fragment, ingest_errors, Property, SynonymTypeRel, Type

cols = ('L101','L102','L103','L104',
        'L201','L202','L203','L204','L205',
        'L301','L302','L303','L304',
        'L401','L402','L403','L404',
        'L501','L502','L503',
        'L601','L602','L603','L604','L605','L606')

parcels = ('DG:SMo','DG:SMi','DG:SG','DG:H',
           'CA3:SLM','CA3:SR','CA3:SL','CA3:SP','CA3:SO',
           'CA2:SLM','CA2:SR','CA2:SP','CA2:SO',
           'CA1:SLM','CA1:SR','CA1:SP','CA1:SO',
           'SUB:SM','SUB:SP','SUB:PL',
           'EC:I','EC:II','EC:III','EC:IV','EC:V','EC:VI')

subregions = ('DG','CA3','CA2','CA1','SUB','EC','hippocampal formation')

parts = ('axons','dendrites','somata')

relations = ('in','not in')

soma_location_map = {
    'hilus'                        : 'H'  ,
    'inner stratum molecular'      : 'SMi',
    'inner stratum moleculare'     : 'SMi',
    'layer i'                      : 'I'  ,
    'layer ii'                     : 'II' ,
    'layer iii'                    : 'III',
    'layer iv'                     : 'IV' ,
    'layer v'                      : 'V'  ,
    'layer vi'                     : 'VI' ,
    'outer stratum moleculare'     : 'SMo',
    'strartum radiatum'            : 'SR' ,
    'stratum granulare'            : 'SG' ,
    'stratum granulosum'           : 'SG' ,
    'stratum lacunosum moleculare' : 'SLM',
    'stratum lacunosum-moleculare' : 'SLM',
    'stratum lucidum'              : 'SL' ,
    'stratum moleculare'           : 'SM' ,
    'stratum moleculare outer'     : 'SMo',
    'stratum oriens'               : 'SO' ,
    'stratum pyramidale'           : 'SP' ,
    'stratum radiatum'             : 'SR'
}

class MorphdataPropertyRecords:
    def save():
        for part in parts:
            subject = part
            for relation in relations:
                predicate = relation
                for parcel in parcels:
                    object = parcel
                    try:
                        row_object = Property.objects.get(subject=subject,predicate=predicate,object=object)
                    except Property.DoesNotExist:
                        row_object = Property(subject=subject,predicate=predicate,object=object)
                        row_object.save()
                for subregion in subregions:
                    object = subregion
                    try:
                        row_object = Property.objects.get(subject=subject,predicate=predicate,object=object)
                    except Property.DoesNotExist:
                        row_object = Property(subject=subject,predicate=predicate,object=object)
                        row_object.save()

class MorphdataStringField:
    def parse_and_save(row,count):
        try:
            if (row['Class Status'] == 'N' or row['Class Status'] == 'M') and row['Neurites \ Layer ID->'] != 'somata':
                Type_id = int(row['unique ID'])
                unvetted = 0
                try:
                    pc_flag = int(row['PC flag'].strip())
                except ValueError:
                    pc_flag = None
                try:
                    soma_pcl_flag = int(row['Soma PCL flag'].strip())
                except ValueError:
                    soma_pcl_flag = None
                try:
                    ax_de_pcl_flag = int(row['Ax/De PCL flag'].strip())
                except ValueError:
                    ax_de_pcl_flag = None
                try:
                    perisomatic_targeting_flag = int(row['Perisomatic targeting flag'].strip())
                except ValueError:
                    perisomatic_targeting_flag = None
                #supplemental pmids
                supplemental_pmids = row['Supplemental PMIDs'].strip()
                #supertype
                super_type=row['Supertype'].strip()
                if ':blank' in super_type:
                    super_type=None
                try:
                    id_type=int(Type_id)
                    row_object_type = Type.objects.get(id=id_type)
                    row_object_type.supertype=super_type
                    row_object_type.save()
                except Exception as e:
                    try:
                        error_object = ingest_errors.objects.get(file_row_num=count,filename='morphdata.csv')
                    except ingest_errors.DoesNotExist:
                        error_object = ingest_errors(filename='morphdata.csv',file_row_num=count,comment=str(e))
                        error_object.save()
                # process soma location information
                soma_location = row['Soma location'].split('(',1)
                subject       = 'somata'
                predicate     = 'in'
                object        = row['Subregion'] + ':' + soma_location_map[soma_location[0].strip().lower()]
                try:
                    row_object  = Property.objects.get(subject=subject,predicate=predicate,object=object)
                    Property_id = row_object.id
                    # identify Evidence_id
                    soma_location_remainder = soma_location[1]
                    soma_location_remainder = re.sub(r'\.', r',', soma_location_remainder)
                    original_id_comma_delimited_set = soma_location_remainder.split(')',1)
                    original_ids = original_id_comma_delimited_set[0].split(',')
                    for id in original_ids:
                        try:
                            original_id = int(id.strip())
                        except Exception:
                            continue
                        try:
                            row_object  = Fragment.objects.get(original_id=original_id)
                            Fragment_id = row_object.id
                            try:
                                row_object  = EvidenceFragmentRel.objects.get(Fragment_id=Fragment_id)
                                Evidence_id = row_object.Evidence_id
                                # check for EvidencePropertyTypeRel match and add if new
                                try:
                                    row_object = EvidencePropertyTypeRel.objects.get(Evidence_id=Evidence_id,Property_id=Property_id,Type_id=Type_id,unvetted=unvetted,pc_flag=pc_flag,soma_pcl_flag=soma_pcl_flag,ax_de_pcl_flag=ax_de_pcl_flag,perisomatic_targeting_flag=perisomatic_targeting_flag,supplemental_pmids=supplemental_pmids)
                                except EvidencePropertyTypeRel.DoesNotExist:
                                    row_object = EvidencePropertyTypeRel(Evidence_id=Evidence_id,Property_id=Property_id,Type_id=Type_id,unvetted=unvetted,pc_flag=pc_flag,soma_pcl_flag=soma_pcl_flag,ax_de_pcl_flag=ax_de_pcl_flag,perisomatic_targeting_flag=perisomatic_targeting_flag,supplemental_pmids=supplemental_pmids)
                                    row_object.save()
                                    # add ArticleSynonymRel record if unique
                                    try:
                                        row_object = ArticleEvidenceRel.objects.get(Evidence_id=Evidence_id)
                                        Article_id = row_object.Article_id
                                        try:
                                            synonym_row_objects = SynonymTypeRel.objects.filter(Type_id=Type_id)
                                            for synonym_row_object in synonym_row_objects:
                                                Synonym_id = synonym_row_object.Synonym_id
                                                try:
                                                    row_object = ArticleSynonymRel.objects.get(Article_id=Article_id,Synonym_id=Synonym_id)
                                                except ArticleSynonymRel.DoesNotExist:
                                                    row_object = ArticleSynonymRel(Article_id=Article_id,Synonym_id=Synonym_id)
                                                    row_object.save()
                                        except SynonymTypeRel.DoesNotExist:
                                            Synonym_id = None
                                    except ArticleEvidenceRel.DoesNotExist:
                                        Article_id = None
                                    #end add ArticleSynonymRel record if unique
                            except EvidenceFragmentRel.DoesNotExist:
                                Evidence_id = None
                        except Fragment.DoesNotExist:
                            Fragment_id = None
                    #end for id in original_ids:

                except Property.DoesNotExist:
                    Property_id = None
                soma_location_remainder = soma_location[1]
                while '/' in soma_location_remainder:
                    row_post_slash_split = soma_location_remainder.split('/',1)
                    soma_location = row_post_slash_split[1].split('(',1)
                    subject       = 'somata'
                    predicate     = 'in'
                    object        = row['Subregion'] + ':' + soma_location_map[soma_location[0].strip().lower()]
                    try:
                        row_object  = Property.objects.get(subject=subject,predicate=predicate,object=object)
                        Property_id = row_object.id
                        # identify Evidence_id
                        soma_location_remainder = soma_location[1]
                        soma_location_remainder = re.sub(r'\.', r',', soma_location_remainder)
                        original_id_comma_delimited_set = soma_location_remainder.split(')',1)
                        original_ids = original_id_comma_delimited_set[0].split(',')
                        for id in original_ids:
                            try:
                                original_id = int(id.strip())
                            except Exception:
                                continue
                            try:
                                row_object  = Fragment.objects.get(original_id=original_id)
                                Fragment_id = row_object.id
                                try:
                                    row_object  = EvidenceFragmentRel.objects.get(Fragment_id=Fragment_id)
                                    Evidence_id = row_object.Evidence_id
                                    # check for EvidencePropertyTypeRel match and add if new
                                    try:
                                        row_object = EvidencePropertyTypeRel.objects.get(Evidence_id=Evidence_id,Property_id=Property_id,Type_id=Type_id,unvetted=unvetted,pc_flag=pc_flag,soma_pcl_flag=soma_pcl_flag,ax_de_pcl_flag=ax_de_pcl_flag,perisomatic_targeting_flag=perisomatic_targeting_flag,supplemental_pmids=supplemental_pmids)
                                    except EvidencePropertyTypeRel.DoesNotExist:
                                        row_object = EvidencePropertyTypeRel(Evidence_id=Evidence_id,Property_id=Property_id,Type_id=Type_id,unvetted=unvetted,pc_flag=pc_flag,soma_pcl_flag=soma_pcl_flag,ax_de_pcl_flag=ax_de_pcl_flag,perisomatic_targeting_flag=perisomatic_targeting_flag,supplemental_pmids=supplemental_pmids)
                                        row_object.save()
                                        # add ArticleSynonymRel record if unique
                                        try:
                                            row_object = ArticleEvidenceRel.objects.get(Evidence_id=Evidence_id)
                                            Article_id = row_object.Article_id
                                            try:
                                                synonym_row_objects = SynonymTypeRel.objects.filter(Type_id=Type_id)
                                                for synonym_row_object in synonym_row_objects:
                                                    Synonym_id = synonym_row_object.Synonym_id
                                                    try:
                                                        row_object = ArticleSynonymRel.objects.get(Article_id=Article_id,Synonym_id=Synonym_id)
                                                    except ArticleSynonymRel.DoesNotExist:
                                                        row_object = ArticleSynonymRel(Article_id=Article_id,Synonym_id=Synonym_id)
                                                        row_object.save()
                                            except SynonymTypeRel.DoesNotExist:
                                                Synonym_id = None
                                        except ArticleEvidenceRel.DoesNotExist:
                                            Article_id = None
                                        #end add ArticleSynonymRel record if unique
                                except EvidenceFragmentRel.DoesNotExist:
                                    Evidence_id = None
                            except Fragment.DoesNotExist:
                                Fragment_id = None
                        #end for id in original_ids:
                    except Property.DoesNotExist:
                        Property_id = None
                    soma_location_remainder = soma_location[1]
                #end while '/' in soma_location_remainder:

                # process parcel column information
                col = 0
                for parcel in parcels:
                    subject = row['Neurites \ Layer ID->']
                    if '-' in row[cols[col]]:
                        predicate = 'not in'
                    else:
                        predicate = 'in'
                    object = parcel
                    try:
                        row_object  = Property.objects.get(subject=subject,predicate=predicate,object=object)
                        Property_id = row_object.id
                        # identify Evidence_id
                        if row[cols[col]] != '' and row[cols[col]] != '"-1"':
                            original_id_comma_delimited_set = row[cols[col]]
                            original_id_comma_delimited_set = re.sub(r'"', '', original_id_comma_delimited_set)
                            original_id_comma_delimited_set = re.sub(r'-', '', original_id_comma_delimited_set)
                            original_ids = original_id_comma_delimited_set.split(',')
                            for id in original_ids:
                                try:
                                    original_id = int(id.strip())
                                except Exception:
                                    continue
                                try:
                                    row_object  = Fragment.objects.get(original_id=original_id)
                                    Fragment_id = row_object.id
                                    try:
                                        row_object  = EvidenceFragmentRel.objects.get(Fragment_id=Fragment_id)
                                        Evidence_id = row_object.Evidence_id
                                        # check for EvidencePropertyTypeRel match and add if new
                                        try:
                                            row_object = EvidencePropertyTypeRel.objects.get(Evidence_id=Evidence_id,Property_id=Property_id,Type_id=Type_id,unvetted=unvetted,pc_flag=pc_flag,soma_pcl_flag=soma_pcl_flag,ax_de_pcl_flag=ax_de_pcl_flag,perisomatic_targeting_flag=perisomatic_targeting_flag,supplemental_pmids=supplemental_pmids)
                                        except EvidencePropertyTypeRel.DoesNotExist:
                                            row_object = EvidencePropertyTypeRel(Evidence_id=Evidence_id,Property_id=Property_id,Type_id=Type_id,unvetted=unvetted,pc_flag=pc_flag,soma_pcl_flag=soma_pcl_flag,ax_de_pcl_flag=ax_de_pcl_flag,perisomatic_targeting_flag=perisomatic_targeting_flag,supplemental_pmids=supplemental_pmids)
                                            row_object.save()
                                            # add ArticleSynonymRel record if unique
                                            try:
                                                row_object = ArticleEvidenceRel.objects.get(Evidence_id=Evidence_id)
                                                Article_id = row_object.Article_id
                                                try:
                                                    synonym_row_objects = SynonymTypeRel.objects.filter(Type_id=Type_id)
                                                    for synonym_row_object in synonym_row_objects:
                                                        Synonym_id = synonym_row_object.Synonym_id
                                                        try:
                                                            row_object = ArticleSynonymRel.objects.get(Article_id=Article_id,Synonym_id=Synonym_id)
                                                        except ArticleSynonymRel.DoesNotExist:
                                                            row_object = ArticleSynonymRel(Article_id=Article_id,Synonym_id=Synonym_id)
                                                            row_object.save()
                                                except SynonymTypeRel.DoesNotExist:
                                                    Synonym_id = None
                                            except ArticleEvidenceRel.DoesNotExist:
                                                Article_id = None
                                            #end add ArticleSynonymRel record if unique
                                    except EvidenceFragmentRel.DoesNotExist:
                                        Evidence_id = None
                                except Fragment.DoesNotExist:
                                    Fragment_id = None
                            #end for id in original_ids:
                        #end if row[cols[col]] != '':
                    except Property.DoesNotExist:
                        Property_id = None
                    col = col + 1
                #end for parcel in parcels:

            #end if (row['Class Status'] == 'N' or row['Class Status'] == 'M') and row['Neurites \ Layer ID->'] != 'somata':
        except Exception:
            pass
