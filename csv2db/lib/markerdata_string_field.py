# markerdata_string_field.py

import re
from ..models import ArticleEvidenceRel, ArticleSynonymRel, Evidence, EvidenceEvidenceRel, EvidenceFragmentRel, EvidenceMarkerdataRel, EvidencePropertyTypeRel, Fragment, Markerdata, Property, SynonymTypeRel

cols = (  '1',  '2',  '3',  '4',  '5',  '6',  '7',  '8',  '9', '10',
         '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
         '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
         '31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
         '41', '42', '43', '44', '45', '46', '47', '48', '49', '50',
         '51', '52', '53', '54', '55', '56', '57', '58', '59', '60',
         '61', '62', '63', '64', '65', '66', '67', '68', '69', '70',
         '71', '72', '73', '74', '75', '76', '77', '78', '79', '80',
         '81', '82', '83', '84', '85', '86', '87', '88', '89', '90',
         '91', '92', '93', '94', '95', '96', '97', '98', '99','100',
        '101','102','103','104','105','106','107','108','109','110',
        '111','112','113','114','115','116','117')

markers = ('CB', 'CR', 'PV', 'CB1', 'Mus2R', 'Sub P Rec', '5HT-3', 'Gaba-a-alpha', 'mGluR1a', 'vGluT3',
           'CCK', 'ENK', 'NPY', 'SOM', 'VIP', 'NG', 'alpha-actinin-2', 'CoupTF II', 'nNOS', 'RLN',
           'ChAT', 'DYN', 'EAAT3', 'GlyT2', 'mGluR7a', 'mGluR8a', 'MOR', 'NKB', 'PPTA','vAChT',
           'vGluT2', 'AChE', 'GAT-1', 'CGRP', 'mGluR2/3', 'Kv3.1', 'mGluR5', 'Prox1','GABAa \\delta', 'VILIP',
           'Cx36', 'Mus1R', 'Mus3R', 'Mus4R', 'ErbB4', 'CaM', 'Y1', 'Man1a','Bok', 'PCP4',
           'AMIGO2', 'Sub P', 'Disc1', 'PSA-NCAM', 'BDNF', 'p-CREB', 'SCIP','Math-2', 'Neuropilin2', 'Id-2',
           'vGAT', 'SATB1', 'NECAB1', 'Chrna2', 'Y2', 'mGluR1', 'GluA2/3', 'CRF', 'GABA-B1', 'Caln',
           'vGlut1', 'mGluR2', 'mGluR3', 'mGluR4', 'SPO', 'GABAa\\alpha 2', 'GABAa\\alpha 3','GABAa\\alpha 4', 'GABAa\\alpha 5', 'GABAa\\alpha 6',
           'GABAa\\beta 1', 'GABAa\\beta 2', 'GABAa\\beta 3', 'GABAa\\gamma 1', 'GABAa\\gamma 2', 'mGluR5a', 'SATB2','Ctip2', 'GluA2', 'GluA1',
           'GluA3', 'GluA4', 'GAT-3', 'CXCR4', 'PPE', 'AR-beta1', 'AR-beta2', 'TH', 'Wfs1', 'Nr4a1', 'Nov',
           'Nr3c2', 'Ndst4', 'Astn2', 'Grp', 'Dcn', 'Htr2c', 'Gpc3', 'Tc1568100', 'Loc432748', 'Prss23',
           'Prss12', 'CaMKII \\alpha', 'DCX', 'NeuN', 'NeuroD', 'CRH')

"""
@marker_code = {
  :first =>  {
    '0' =>  ['unknown'],
    '1' =>  ['positive'],
    '2' =>  ['negative'],
    '3' =>  ['weak_positive'],
    '4' =>  ['positive', 'negative'],
    '5' =>  ['positive', 'negative']
  },
  :second =>  {
    '0' =>  ['immunohistochemistry'],
    '1' =>  ['mRNA'],
    '2' =>  ['immunohistochemistry', 'mRNA'],
    '3' =>  ['unknown'],
    '4' =>  ['promoter_expression_construct'],
    '?' =>  ['unknown'],
  },
  :third =>  {
    '0' =>  ['mouse'],
    '1' =>  ['rat'],
    '2' =>  ['mouse', 'rat'],
    '3' =>  ['unspecified_rodent'],
    '?' =>  ['unknown'],
  }
}
"""

class MarkerdataStringField:

    def parse_and_save(row,count,markerdata_flag):
        c = 0
        for col in cols:
            if (c>(len(cols)-1) and markerdata_flag==0):
                break
            marker = markers[c]
            c = c + 1
            string_field = row[col]
            # tag and conflict note determination
            tag                       = None
            conflict_note             = None
            interpretation_notes      = None
            property_type_explanation = None
            if count==0:
                markerName=string_field.strip()
                if markerName !="":
                    row_object = Property(subject=marker,predicate='has name',object=markerName)
                    row_object.save()

            if '{' in string_field:
                string_field_open_brace_split = string_field.split('{')
                tag = string_field_open_brace_split[1][0]
                string_field_close_brace_split = string_field_open_brace_split[1].split('}')
                token = string_field_close_brace_split[0].strip()
                if '<' in token:
                    token_split = token.split('<')
                    token_sans_comment = token_split[0].strip()
                else:
                    token_sans_comment = token
                if   token_sans_comment == 'p':
                    conflict_note = 'positive'
                elif token_sans_comment == 'n':
                    conflict_note = 'negative'
                elif token_sans_comment == 'a':
                    conflict_note = 'unresolved inferential conflict'
                elif token_sans_comment == 'b':
                    conflict_note = 'species/protocol inferential conflict'
                elif token_sans_comment == '1':
                    conflict_note = 'subtypes'
                elif token_sans_comment == '2':
                    conflict_note = 'unresolved'
                elif token_sans_comment == '3':
                    conflict_note = 'species/protocol differences'
                elif token_sans_comment == '4':
                    conflict_note = 'subcellular expression differences'
                elif token_sans_comment == 'pi':
                    conflict_note = 'positive inference'
                elif token_sans_comment == 'ni':
                    conflict_note = 'negative inference'
                elif token_sans_comment == 'pi,ni':
                    conflict_note = 'positive inference; negative inference'
                elif token_sans_comment == 'p,ni':
                    conflict_note = 'positive; negative inference'
                elif token_sans_comment == 'pi,n':
                    conflict_note = 'positive inference; negative'
                elif token_sans_comment == 'cp':
                    conflict_note = 'confirmed positive'
                elif token_sans_comment == 'cn':
                    conflict_note = 'confirmed negative'
                elif token_sans_comment == 'cpi':
                    conflict_note = 'confirmed positive inference'
                elif token_sans_comment == 'cni':
                    conflict_note = 'confirmed negative inference'

                if '*' in token:
                    token_property_type_explanation  = token.strip()
                    tokens_property_type_explanation = token_property_type_explanation.split('*')
                    property_type_explanation        = tokens_property_type_explanation[1]
                string_field = string_field_close_brace_split[1]

            # begin parsing field string
            if '"' in string_field:
                q1 = string_field.find('"')
                string_field_sub = string_field[q1+1:] + '; '
                # handle ';' in <"*6 of 7 positive; at least one with soma in SR*"> example from CA1 Ivy - CB
                insert_placeholder_char = 0
                prev_char               = ''
                prev_prev_char          = ''
                placeholder_string      = ''
                for char in string_field_sub:
                    if prev_prev_char == '<' and prev_char == '"' and char == '*':
                        insert_placeholder_char = 1
                    if char == ';' and insert_placeholder_char == 1:
                        placeholder_string = placeholder_string + '}'   # change character ';' to placeholder character '}'
                    else:
                       placeholder_string = placeholder_string + char
                    if prev_prev_char == '*' and prev_char == '"' and char == '>':
                        insert_placeholder_char = 0
                    prev_prev_char = prev_char
                    prev_char      = char
                tokens = placeholder_string.split(';')
                for token in tokens:
                    token = re.sub(r'}', r';', token) # change placeholder character '}' back to character ';'
                    if '[' in token:
                        continue # skip this inferred evidence
                    interpretation_notes = None
                    if '*' in token:
                        token_interpretation_notes  = token.strip()
                        tokens_interpretation_notes = token_interpretation_notes.split('*')
                        interpretation_notes        = tokens_interpretation_notes[1]
                    #end if
                    if '.' in token:
                        token = token.strip()
                        Evidence_id = None

                        # expression
                        if   token[0] == '0':
                            Evidence_id = 1
                            expression  = '["unknown"]'
                            object      =   'unknown'
                        elif token[0] == '1':
                            expression  = '["positive"]'
                            object      =   'positive'
                        elif token[0] == '2':
                            expression  = '["negative"]'
                            object      =   'negative'
                        elif token[0] == '3':
                            expression  = '["weak_positive"]'
                            object      =   'weak_positive'
                        elif token[0] == '4':
                            expression  = '["positive", "negative"]'
                            object      =   'positive_negative'
                        elif token[0] == '5':
                            expression  = '["positive", "negative"]'
                            object      =   'positive_negative'
                        elif token[0] == '8':
                            expression  = '["positive_inference"]'
                            object      =   'positive_inference'
                        elif token[0] == '9':
                            expression  = '["negative_inference"]'
                            object      =   'negative_inference'
                        else:
                            if tag is None:
                                continue

                        # tag {} expression override
                        if   tag == '}':
                            Evidence_id = 1
                            expression  = '["unknown"]'
                            object      =   'unknown'
                        #elif tag == 'p':
                        #    expression  = '["positive"]'
                        #    object      =   'positive'
                        #elif tag == 'n':
                        #    expression  = '["negative"]'
                        #    object      =   'negative'
                        #elif tag == '1': # subtypes
                        #    expression  = '["positive", "negative"]'
                        #    object      =   'positive_negative'
                        #elif tag == '2': # conflicting data
                        #    expression  = '["positive", "negative"]'
                        #    object      =   'positive_negative'
                        #elif tag == '3': # species/protocol differences
                        #    expression  = '["positive", "negative"]'
                        #    object      =   'positive_negative'
                        else:
                            pass

                        # protocol
                        if   token[1] == '0':
                            protocol   = '["immunohistochemistry"]'
                        elif token[1] == '1':
                            protocol   = '["mRNA"]'
                        elif token[1] == '2':
                            protocol   = '["immunohistochemistry", "mRNA"]'
                        elif token[1] == '3':
                            protocol   = '["unknown"]'
                        elif token[1] == '4':
                            protocol   = '["promoter_expression_construct"]'
                        else:
                            continue

                        # animal
                        if   token[2] == '0':
                            animal     = '["mouse"]'
                        elif token[2] == '1':
                            animal     = '["rat"]'
                        elif token[2] == '2':
                            animal     = '["mouse", "rat"]'
                        elif token[2] == '3':
                            animal     = '["unspecified_rodent"]'
                        else:
                            continue

                        # check for existance of Markerdata record, then save if new
                        try:
                            row_object = Markerdata.objects.get(expression=expression,animal=animal,protocol=protocol)
                        except Markerdata.DoesNotExist:
                            if (c<len(cols) and markerdata_flag==1):
                                break
                            row_object = Markerdata(expression=expression,animal=animal,protocol=protocol)
                            if expression != '["unknown"]':
                                row_object.save()

                        # check for existance of Property record, then save if new
                        subject   = marker
                        predicate = 'has expression'
                        if object == 'positive_negative':
                            object = 'positive'
                            try:
                                row_object = Property.objects.get(subject=subject,predicate=predicate,object=object)
                            except Property.DoesNotExist:
                                if (c<len(cols) and markerdata_flag==1):
                                    break
                                row_object = Property(subject=subject,predicate=predicate,object=object)
                                row_object.save()
                            object = 'negative'
                            try:
                                row_object = Property.objects.get(subject=subject,predicate=predicate,object=object)
                            except Property.DoesNotExist:
                                if (c<len(cols) and markerdata_flag==1):
                                    break
                                row_object = Property(subject=subject,predicate=predicate,object=object)
                                row_object.save()
                            object = 'positive_negative'
                        else:
                            try:
                                row_object = Property.objects.get(subject=subject,predicate=predicate,object=object)
                            except Property.DoesNotExist:
                                if (c<len(cols) and markerdata_flag==1):
                                    break
                                row_object = Property(subject=subject,predicate=predicate,object=object)
                                row_object.save()

                        # populate EvidencePropertyTypeRel and related tables ArticleSynonymRel, EvidenceEvidenceRel, Evidence, EvidenceMarkerdataRel
                        if Evidence_id is None:
                            try:
                                original_id_string = token[4:10]
                                original_id = int(token[4:10]) # convert the original_id protion of the token (i.e. substring after the dot) to int
                                try:
                                    row_object  = Fragment.objects.filter(original_id=original_id).first()
                                    Fragment_id = row_object.id
                                    try:
                                        row_object   = EvidenceFragmentRel.objects.filter(Fragment_id=Fragment_id).first()
                                        Evidence2_id = row_object.Evidence_id
                                        Evidence1_id = Evidence.objects.count() + 1
                                        Evidence_id  = Evidence1_id
                                        try:
                                            row_object = EvidenceEvidenceRel.objects.get(Evidence1_id=Evidence1_id,Evidence2_id=Evidence2_id)
                                        except EvidenceEvidenceRel.DoesNotExist:
                                            if (c<len(cols) and markerdata_flag==1):
                                                break
                                            row_object = EvidenceEvidenceRel(Evidence1_id=Evidence1_id,Evidence2_id=Evidence2_id,type='interpretation')
                                            row_object.save()
                                            row_object = Evidence()
                                            row_object.save()
                                            try:
                                                row_object = Markerdata.objects.get(expression=expression,animal=animal,protocol=protocol)
                                                Markerdata_id = row_object.id
                                                try:
                                                    row_object = EvidenceMarkerdataRel.objects.get(Evidence_id=Evidence_id,Markerdata_id=Markerdata_id)
                                                except EvidenceMarkerdataRel.DoesNotExist:
                                                    if (c<len(cols) and markerdata_flag==1):
                                                        break
                                                    row_object = EvidenceMarkerdataRel(Evidence_id=Evidence_id,Markerdata_id=Markerdata_id)
                                                    row_object.save()
                                            except Markerdata.DoesNotExist:
                                                Markerdata_id = None
                                    except EvidenceFragmentRel.DoesNotExist:
                                        Evidence_id = None
                                except Fragment.DoesNotExist:
                                    Fragment_id = None
                            except Exception:
                                pass
                        #end if Evidence_id is None:
                        Type_id = row['Type_id']
                        Type_id = re.sub(r'-', r'', Type_id)
                        Type_id = int(Type_id)
                        unvetted = 0

                        # add two EvidencePropertyTypeRel records if object is 'positive_negative'
                        if object == 'positive_negative':
                            object = 'positive'
                            try:
                                row_object = Property.objects.get(subject=subject,predicate=predicate,object=object)
                                Property_id = row_object.id
                                try:
                                    row_object = EvidencePropertyTypeRel.objects.get(Evidence_id=Evidence_id,Property_id=Property_id,Type_id=Type_id,conflict_note=conflict_note,unvetted=unvetted,interpretation_notes=interpretation_notes,property_type_explanation=property_type_explanation)
                                except EvidencePropertyTypeRel.DoesNotExist:
                                    if (c<len(cols) and markerdata_flag==1):
                                        break
                                    row_object = EvidencePropertyTypeRel(Evidence_id=Evidence_id,Property_id=Property_id,Type_id=Type_id,conflict_note=conflict_note,unvetted=unvetted,interpretation_notes=interpretation_notes,property_type_explanation=property_type_explanation)
                                    row_object.save()
                                    if Evidence_id != 1:
                                        # add ArticleSynonymRel record if unique
                                        try:
                                            row_object = ArticleEvidenceRel.objects.get(Evidence_id=Evidence2_id)
                                            Article_id = row_object.Article_id
                                            try:
                                                synonym_row_objects = SynonymTypeRel.objects.filter(Type_id=Type_id)
                                                for synonym_row_object in synonym_row_objects:
                                                    Synonym_id = synonym_row_object.Synonym_id
                                                    try:
                                                        row_object = ArticleSynonymRel.objects.get(Article_id=Article_id,Synonym_id=Synonym_id)
                                                    except ArticleSynonymRel.DoesNotExist:
                                                        if (c<len(cols) and markerdata_flag==1):
                                                            break
                                                        row_object = ArticleSynonymRel(Article_id=Article_id,Synonym_id=Synonym_id)
                                                        row_object.save()
                                            except SynonymTypeRel.DoesNotExist:
                                                Synonym_id = None
                                        except ArticleEvidenceRel.DoesNotExist:
                                            Article_id = None
                                        #end add ArticleSynonymRel record if unique
                                    #end if Evidence_id != 1:
                            except Property.DoesNotExist:
                                Property_id = None
                                Type_id = None
                            object = 'negative'
                            try:
                                row_object = Property.objects.get(subject=subject,predicate=predicate,object=object)
                                Property_id = row_object.id
                                try:
                                    row_object = EvidencePropertyTypeRel.objects.get(Evidence_id=Evidence_id,Property_id=Property_id,Type_id=Type_id,conflict_note=conflict_note,unvetted=unvetted,interpretation_notes=interpretation_notes,property_type_explanation=property_type_explanation)
                                except EvidencePropertyTypeRel.DoesNotExist:
                                    if (c<len(cols) and markerdata_flag==1):
                                        break
                                    row_object = EvidencePropertyTypeRel(Evidence_id=Evidence_id,Property_id=Property_id,Type_id=Type_id,conflict_note=conflict_note,unvetted=unvetted,interpretation_notes=interpretation_notes,property_type_explanation=property_type_explanation)
                                    row_object.save()
                                    if Evidence_id != 1:
                                        # add ArticleSynonymRel record if unique
                                        try:
                                            row_object = ArticleEvidenceRel.objects.get(Evidence_id=Evidence2_id)
                                            Article_id = row_object.Article_id
                                            try:
                                                synonym_row_objects = SynonymTypeRel.objects.filter(Type_id=Type_id)
                                                for synonym_row_object in synonym_row_objects:
                                                    Synonym_id = synonym_row_object.Synonym_id
                                                    try:
                                                        row_object = ArticleSynonymRel.objects.get(Article_id=Article_id,Synonym_id=Synonym_id)
                                                    except ArticleSynonymRel.DoesNotExist:
                                                        if (c<len(cols) and markerdata_flag==1):
                                                            break
                                                        row_object = ArticleSynonymRel(Article_id=Article_id,Synonym_id=Synonym_id)
                                                        row_object.save()
                                            except SynonymTypeRel.DoesNotExist:
                                                Synonym_id = None
                                        except ArticleEvidenceRel.DoesNotExist:
                                            Article_id = None
                                        #end add ArticleSynonymRel record if unique
                                    #end if Evidence_id != 1:
                            except Property.DoesNotExist:
                                Property_id = None
                                Type_id = None
                            object = 'positive_negative'
                        else:
                            try:
                                row_object = Property.objects.get(subject=subject,predicate=predicate,object=object)
                                Property_id = row_object.id
                                try:
                                    row_object = EvidencePropertyTypeRel.objects.get(Evidence_id=Evidence_id,Property_id=Property_id,Type_id=Type_id,conflict_note=conflict_note,unvetted=unvetted,interpretation_notes=interpretation_notes,property_type_explanation=property_type_explanation)
                                    print('row_object #1 ')
                                    print(row_object)
                                except EvidencePropertyTypeRel.DoesNotExist:
                                    if (c<len(cols) and markerdata_flag==1):
                                        break
                                    row_object = EvidencePropertyTypeRel(Evidence_id=Evidence_id,Property_id=Property_id,Type_id=Type_id,conflict_note=conflict_note,unvetted=unvetted,interpretation_notes=interpretation_notes,property_type_explanation=property_type_explanation)
                                    row_object.save()
                                    if (count < 10):
                                        print('row_object #2 ')
                                        print(row_object)
                                        print('Evidence_id: ', Evidence_id, '; Property_id: ', Property_id, '; Type_id: ', Type_id, '; conflict_note: ', conflict_note)
                                    if Evidence_id != 1:
                                        # add ArticleSynonymRel record if unique
                                        try:
                                            row_object = ArticleEvidenceRel.objects.get(Evidence_id=Evidence2_id)
                                            Article_id = row_object.Article_id
                                            try:
                                                synonym_row_objects = SynonymTypeRel.objects.filter(Type_id=Type_id)
                                                for synonym_row_object in synonym_row_objects:
                                                    Synonym_id = synonym_row_object.Synonym_id
                                                    try:
                                                        row_object = ArticleSynonymRel.objects.get(Article_id=Article_id,Synonym_id=Synonym_id)
                                                    except ArticleSynonymRel.DoesNotExist:
                                                        if (c<len(cols) and markerdata_flag==1):
                                                            break
                                                        row_object = ArticleSynonymRel(Article_id=Article_id,Synonym_id=Synonym_id)
                                                        row_object.save()
                                            except SynonymTypeRel.DoesNotExist:
                                                Synonym_id = None
                                        except ArticleEvidenceRel.DoesNotExist:
                                            Article_id = None
                                        #end add ArticleSynonymRel record if unique
                                    #end if Evidence_id != 1:
                            except Property.DoesNotExist:
                                Property_id = None
                                Type_id = None

                    #end if '.' in token:
                #end for token in tokens:
