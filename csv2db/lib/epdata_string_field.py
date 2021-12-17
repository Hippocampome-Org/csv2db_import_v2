# epdata_string_field.py

import re
from ..models import Article, ArticleEvidenceRel, ArticleSynonymRel, Epdata, EpdataEvidenceRel, Evidence, EvidenceEvidenceRel, EvidenceFragmentRel, EvidencePropertyTypeRel, Fragment, Property, SynonymTypeRel
from ..models import article_not_found

parameters = ('Vrest', 'Rin', 'tau', 'Vthresh', 'fAHP', 'APampl', 'APwidth', 'maxFR', 'sAHP', 'sag')

cols = ('PMID{Table_or_Figure#;Vrest ± SD (n)}',
        'PMID{Table_or_Figure#;Rin ± SD (n)}',
        'PMID{Table_or_Figure#;taum ± SD (n)}',
        'PMID{Table_or_Figure#;Vthresh ± SD (n)}',
        'PMID{Table_or_Figure#;FastAHP ± SD (n)}',
        'PMID{Table_or_Figure#;APampl ± SD (n)}',
        'PMID{Table_or_Figure#;APwidth ± SD (n)}',
        'PMID{Table_or_Figure#;MAxFR ± SD @Istimul (n)}',
        'PMID{Table_or_Figure#;SlowAHP ± SD @Istimul@time(n)}',
        'PMID{Table_or_Figure#;Sag_ratio ± SD @Istimul (n)}')

col_cleaned  = ('Original Spreadsheet Row',
                'Subregion',
                'Cell type name',
                'Unique ID',
                'PMID',
                'Species',
                'Method',
                'Raw temperature',
                'Room/body temperature')

col_property = ('Vrest',
                'Vrest_Rep Value?',
                'Vrest_> Value?',
                'Vrest_Statistics String',
                'Vrest_Statistical Method',
                'Vrest_n',
                '',
                '',
                'Vrest_Page Location',
                'Vrest_Notes',
                'Vrest_Orig ID',
                'Rin',
                'Rin_Rep Value?',
                'Rin_> Value?',
                'Rin_Statistics String',
                'Rin_Statistical Method',
                'Rin_n',
                '',
                '',
                'Rin_Page Location',
                'Rin_Notes',
                'Rin_Orig ID',
                'tau',
                'tau_Rep Value?',
                'tau_> Value?',
                'tau_Statistics String',
                'tau_Statistical Method',
                'tau_n',
                '',
                '',
                'tau_Page Location',
                'tau_Notes',
                'tau_Orig ID',
                'Vthresh',
                'Vthresh_Rep Value?',
                'Vthresh_> Value?',
                'Vthresh_Statistics String',
                'Vthresh_Statistical Method',
                'Vthresh_n',
                '',
                '',
                'Vthresh_Page Location',
                'Vthresh_Notes',
                'Vthresh_Orig ID',
                'Fast AHP',
                'Fast AHP_Rep Value?',
                'Fast AHP_> Value?',
                'Fast AHP_Statistics String',
                'Fast AHP_Statistical Method',
                'Fast AHP_n',
                '',
                '',
                'Fast AHP_Page Location',
                'Fast AHP_Notes',
                'Fast AHP_Orig ID',
                'AP ampl',
                'AP ampl_Rep Value?',
                'AP ampl_> Value?',
                'AP ampl_Statistics String',
                'AP ampl_Statistical Method',
                'AP ampl_n',
                '',
                '',
                'AP ampl_Page Location',
                'AP ampl_Notes',
                'AP ampl_Orig ID',
                'AP width',
                'AP width_Rep Value?',
                'AP width_> Value?',
                'AP width_Statistics String',
                'AP width_Statistical Method',
                'AP width_n',
                '',
                '',
                'AP width_Page Location',
                'AP width_Notes',
                'AP width_Orig ID',
                'Max F.R.',
                'Max F.R._Rep Value?',
                'Max F.R._> Value?',
                'Max F.R._Statistics String',
                'Max F.R._Statistical Method',
                'Max F.R._n',
                'Max F.R._i stim',
                'Max F.R._t stim',
                'Max F.R._Page Location',
                'Max F.R._Notes',
                'Max F.R._Orig ID',
                'Slow AHP',
                'Slow AHP_Rep Value?',
                'Slow AHP_> Value?',
                'Slow AHP_Statistics String',
                'Slow AHP_Statistical Method',
                'Slow AHP_n',
                'Slow AHP_i stim',
                'Slow AHP_t stim',
                'Slow AHP_Page Location',
                'Slow AHP_Notes',
                'Slow AHP_Orig ID',
                'Sag ratio',
                'Sag ratio_Rep Value?',
                'Sag ratio_> Value?',
                'Sag ratio_Statistics String',
                'Sag ratio_Statistical Method',
                'Sag ratio_n',
                'Sag ratio_i stim',
                '',
                'Sag ratio_Page Location',
                'Sag ratio_Notes',
                'Sag ratio_Orig ID')
col_properties_per_set       = 11
col_property_offset_value1   = 0
col_property_offset_value2   = 1
col_property_offset_gt_value = 2
col_property_offset_error    = 3
col_property_offset_std_sem  = 4
col_property_offset_n        = 5
col_property_offset_istim    = 6
col_property_offset_time     = 7
col_property_offset_location = 8
col_property_offset_notes    = 9
col_property_offset_orig_id  = 10

epdata_property = [['Vrest',     'is between', '[-inf, +inf]'],
                   ['Rin',       'is between', '[-inf, +inf]'],
                   ['tm',        'is between', '[-inf, +inf]'],
                   ['Vthresh',   'is between', '[-inf, +inf]'],
                   ['fast_AHP',  'is between', '[-inf, +inf]'],
                   ['AP_ampl',   'is between', '[-inf, +inf]'],
                   ['AP_width',  'is between', '[-inf, +inf]'],
                   ['max_fr',    'is between', '[-inf, +inf]'],
                   ['slow_AHP',  'is between', '[-inf, +inf]'],
                   ['sag_ratio', 'is between', '[-inf, +inf]'],
                   ['AP_width',  'is between', 'unknown'],
                   ['max_fr',    'is between', 'unknown'],
                   ['slow_AHP',  'is between', 'unknown'],
                   ['sag_ratio', 'is between', 'unknown'],
                   ['Vrest',     'is between', 'unknown'],
                   ['Rin',       'is between', 'unknown'],
                   ['tm',        'is between', 'unknown'],
                   ['Vthresh',   'is between', 'unknown'],
                   ['fast_AHP',  'is between', 'unknown'],
                   ['AP_ampl',   'is between', 'unknown']]
epdata_properties = 20
isubject          = 0
ipredicate        = 1
iobject           = 2

units = ('mV', 'mOm', 'ms', 'mV', 'mV', 'mV', 'ms', 'Hz', 'mV', '')

class EpdataPropertyRecords:
    def save():
        iproperty  = 0
        while iproperty < epdata_properties:
            subject   = epdata_property[iproperty][isubject]
            predicate = epdata_property[iproperty][ipredicate]
            object    = epdata_property[iproperty][iobject]
            try:
                row_object = Property.objects.get(subject=subject,predicate=predicate,object=object)
            except Property.DoesNotExist:
                row_object = Property(subject=subject,predicate=predicate,object=object)
                row_object.save()
            iproperty = iproperty + 1

class EpdataStringField:
    def parse_and_save(row):
        #Type_id_last = ''
        #Type_id_this = ''
        col_unit = 0
        col_property_set = 0
        for col in cols:
            raw       = None
            value1    = None
            value2    = None
            error     = None
            std_sem   = None
            n         = None
            istim     = None
            time      = None
            unit      = None
            location  = None
            rep_value = None
            gt_value  = None
            try:
                pmid_isbn = row['PMID'].strip()

                # check to see if pmid_isbn exists in Article table
                if pmid_isbn != 'None given':
                    pmid_isbn = re.sub(r'-', r'', pmid_isbn)
                    try:
                        row_object = Article.objects.filter(pmid_isbn=pmid_isbn).order_by('id').first()
                        if row_object == None:
                            Article_id = None
                            # write new pmid_isbn to article_not_found
                            try:
                                row_object = article_not_found.objects.get(pmid_isbn=pmid_isbn)
                            except article_not_found.DoesNotExist:
                                row_object = article_not_found(pmid_isbn=pmid_isbn)
                                row_object.save()
                            pmid_isbn = 'None given'
                        else:
                            Article_id = row_object.id
                    except Article.DoesNotExist:
                        Article_id = None
                        # write new pmid_isbn to article_not_found
                        try:
                            row_object = article_not_found.objects.get(pmid_isbn=pmid_isbn)
                        except article_not_found.DoesNotExist:
                            row_object = article_not_found(pmid_isbn=pmid_isbn)
                            row_object.save()
                        pmid_isbn = 'None given'
                #end check to see if pmid_isbn exists in Article table

                #raw = row[col]
                #if '{' in raw:
                if pmid_isbn != 'None given':
                    #splita = raw.split('{')
                    #pmid_isbn = int(splita[0].strip())
                    #splitb = splita[1].split(';')
                    #location = splitb[0].strip()
                    #splitb1 = splitb[1]
                    #splitb1 = splitb1.replace('±',' ±')
                    #splitb1 = splitb1.replace('_',' ')
                    #splitb1 = splitb1.replace('(',' (')
                    #splitb1 = splitb1.replace(')',' )')
                    #splitb1 = splitb1.replace('@',' @')
                    #splitb1 = splitb1.replace('@ ','@')
                    #splitb1 = splitb1.replace('}',' }')
                    #splitb1 = ' '.join(splitb1.split())
                    #splitb1 = splitb1.replace('± ','±')
                    #raw = splitb1 #debug
                    #if '@' in splitb1:
                    #    splitata = splitb1.split('@',1)
                    #    splitatb = splitata[1].split(' ')
                    #    istim    = splitatb[0].strip()
                    #    if '@' in splitatb[1]:
                    #        splitatc = splitatb[1].split('@')
                    #        splitatd = splitatc[1].split(' ')
                    #        time     = splitatd[0].strip()
                    #    if (istim == 'X') or ('[' in istim):
                    #        istim = 'unknown'
                    #    if time == 'X':
                    #        time = 'unknown'
                    #if '(' in splitb1:
                    #    splitp1 = splitb1.split('(')
                    #    splitp2 = splitp1[1].split(' ')
                    #    n       = splitp2[0].strip()
                    #if ('[' in splitb1) and ('@[' not in splitb1):
                    #    splitc = splitb1.split('[')
                    #    splitd = splitc[1].split(',')
                    #    value1 = splitd[0].strip()
                    #    splite = splitd[1].split(']')
                    #    value2 = splite[0].strip()
                    #    std_sem = 'N/A'
                    #else:
                    #    splitc = splitb1.split(' ',1)
                    #    value1 = splitc[0].strip()
                    #    if '±' in splitc[1]:
                    #        splitd = splitc[1].split('±')
                    #        splite = splitd[1].split(' ')
                    #        error  = splite[0].strip()
                    #    if 'SE' in splitb1:
                    #        std_sem  = 'sem'
                    #    else:
                    #        std_sem  = 'std'
                    # value1
                    value1_string = row[col_property[col_property_set+col_property_offset_value1]]
                    if value1_string == '':
                        value1 = None
                    else:
                        value1 = value1_string
                    if value1 is not None:
                        # value2
                        value2 = None
                        #value2_string = row[col_property[col_property_set+col_property_offset_value2]]
                        #if value2_string == '':
                        #    value2 = None
                        #else:
                        #    value2 = value2_string
                        # rep_value
                        rep_value = None
                        rep_value_string = row[col_property[col_property_set+col_property_offset_value2]]
                        if rep_value_string == '':
                            rep_value = None
                        else:
                            rep_value = rep_value_string.strip()
                        # gt_value
                        gt_value = None
                        gt_value_string = row[col_property[col_property_set+col_property_offset_gt_value]]
                        if gt_value_string == '':
                            gt_value = None
                        else:
                            gt_value = gt_value_string.strip()
                        # error
                        error_string = row[col_property[col_property_set+col_property_offset_error]]
                        if error_string == '':
                            error = None
                        else:
                            error_string = error_string.strip()
                            if '±' in error_string:
                                error_string_split = error_string.split('±',1)
                                error_string = error_string_split[1]
                                error = error_string
                            elif '_' in error_string:
                                error_string = re.sub(r'\[', r'', error_string)
                                error_string = re.sub(r'\]', r'', error_string)
                                error_string_split = error_string.split('_',1)
                                error1 = float(error_string_split[0])
                                error2 = float(error_string_split[1])
                                error = (error1 + error2)/2.0
                                error = str(round(error,1))
                                error_string = str(error)
                            else:
                                error_string = ''
                                error = None
                        # std_sem
                        std_sem_string = row[col_property[col_property_set+col_property_offset_std_sem]]
                        if std_sem_string == 'SEM':
                            std_sem        = 'sem'
                            std_sem_string = ' ' + 'SEM'
                        elif std_sem_string == 'SDEV':
                            std_sem        = 'std'
                            std_sem_string = ''
                        else:
                            std_sem        = 'N/A'
                            std_sem_string = ''
                        # n
                        n_string = row[col_property[col_property_set+col_property_offset_n]]
                        if n_string == '':
                            n = None
                        else:
                            n = n_string
                        # istim
                        if col_property[col_property_set+col_property_offset_istim] == '':
                            istim_string = ''
                            istim        = None
                        else:
                            istim_string = row[col_property[col_property_set+col_property_offset_istim]]
                            if istim_string == '' or istim_string == 'X':
                                istim = None
                            else:
                                istim = istim_string
                        # time
                        if col_property[col_property_set+col_property_offset_time] == '':
                            time_string  = ''
                            time         = None
                        else:
                            time_string = row[col_property[col_property_set+col_property_offset_time]]
                            if time_string == '' or time_string == 'X':
                                time = None
                            else:
                                time = time_string
                        # unit
                        unit = units[col_unit]
                        # location
                        location = row[col_property[col_property_set+col_property_offset_location]]
                        location = location.strip()
                        location = re.sub(r';', r',', location)
                        # original_id
                        original_id = None
                        try:
                            original_id_string = row[col_property[col_property_set+col_property_offset_orig_id]].strip()
                            original_id_string = original_id_string.strip()
                            if original_id_string != '':
                                original_id = int(original_id_string)
                        except Exception:
                            pass
                        # protocol - Species | Method | Raw temperature | Room/body temperature
                        species               = ' '
                        method                = ' '
                        raw_temperature       = ' '
                        room_body_temperature = ' '
                        protocol              = ' '
                        try:
                            species = row['Species']
                            species = species.strip()
                            if species == 'None given':
                                species = ' '
                            method = row['Method']
                            method = method.strip()
                            if method == 'None given':
                                method = ' '
                            raw_temperature = row['Raw temperature']
                            raw_temperature = raw_temperature.strip()
                            if raw_temperature == 'None given':
                                raw_temperature = ' '
                            room_body_temperature = row['Room/body temperature']
                            room_body_temperature = room_body_temperature.strip()
                            if room_body_temperature == 'None given':
                                room_body_temperature = ' '
                            protocol = species + ' | ' + method + ' | ' + raw_temperature + ' | ' + room_body_temperature
                        except Exception:
                            pass
                        # raw
                        raw = pmid_isbn + ' {' + location + '; ' + value1_string + ' ± ' + error_string + ' @' + istim_string + '@' + time_string + ' (' + n_string + std_sem_string + ')}'
                        #example: raw = 9497429 {Table 1, wild type; 0.6 ± 0.4 @250@1000 (16 SEM)}
                        # parameter
                        parameter = parameters[col_unit]
                        row_object = Epdata(
                            raw       = raw,
                            value1    = value1,
                            value2    = value2,
                            error     = error,
                            std_sem   = std_sem,
                            n         = n,
                            istim     = istim,
                            time      = time,
                            unit      = unit,
                            location  = location,
                            rep_value = rep_value,
                            gt_value  = gt_value
                        )
                        row_object.save()
                        Epdata_id = row_object.id

                        # Fragment entries - check for dups before write and find matching fragment for "original_id"
                        unique_id    = row['Unique ID'].strip()
                        unique_id    = re.sub(r'-', r'', unique_id)
                        cell_id      = int(unique_id)
                        Fragment_id  = None
                        Evidence2_id = None
                        type         = None
                        try:
                            row_object   = Fragment.objects.get(pmid_isbn=pmid_isbn,cell_id=cell_id,parameter=parameter,type=type,original_id=original_id)  # from epdata.csv where type=None
                            Fragment_id  = row_object.id
                            row_object   = EvidenceFragmentRel.objects.get(Fragment_id=Fragment_id)
                            Evidence2_id = row_object.Evidence_id
                        except Fragment.DoesNotExist:
                            # set original_id and other info from Fragment record if found
                            #original_id            = None
                            quote                  = None
                            page_location          = None
                            pmid_isbn_page         = None
                            interpretation         = None
                            interpretation_notes   = None
                            linking_cell_id        = None
                            linking_pmid_isbn      = None
                            linking_pmid_isbn_page = None
                            linking_quote          = None
                            linking_page_location  = None
                            try:
                                # from ep_fragment.csv where type='data'
                                row_object  = Fragment.objects.filter(pmid_isbn=pmid_isbn,cell_id=cell_id,parameter=parameter,type='data',original_id=original_id).order_by('id').first()
                                #original_id            = row_object.original_id
                                quote                  = row_object.quote
                                page_location          = row_object.page_location
                                pmid_isbn_page         = row_object.pmid_isbn_page
                                interpretation         = row_object.interpretation
                                interpretation_notes   = row_object.interpretation_notes
                                linking_cell_id        = row_object.linking_cell_id
                                linking_pmid_isbn      = row_object.linking_pmid_isbn
                                linking_pmid_isbn_page = row_object.linking_pmid_isbn_page
                                linking_quote          = row_object.linking_quote
                                linking_page_location  = row_object.linking_page_location
                            except Exception:
                                pass
                            #end set original_id and other info from Fragment record if found
                            # protocol
                            try:
                                page_location = re.sub(r',', r' |', page_location)
                                page_location = page_location + ', ' + protocol
                            except Exception:
                                pass
                            # add Fragment conditionally
                            row_object = Fragment(pmid_isbn=pmid_isbn,cell_id=cell_id,parameter=parameter,type=type,  # from epdata.csv where type=None
                                                  original_id            = original_id,
                                                  quote                  = quote,
                                                  page_location          = page_location,
                                                  pmid_isbn_page         = pmid_isbn_page,
                                                  interpretation         = interpretation,
                                                  interpretation_notes   = interpretation_notes,
                                                  linking_cell_id        = linking_cell_id,
                                                  linking_pmid_isbn      = linking_pmid_isbn,
                                                  linking_pmid_isbn_page = linking_pmid_isbn_page,
                                                  linking_quote          = linking_quote,
                                                  linking_page_location  = linking_page_location
                                                 )
                            row_object.save()
                            Fragment_id = row_object.id
                            # add Evidence conditionally
                            row_object = Evidence()
                            row_object.save()
                            Evidence_id  = row_object.id
                            Evidence2_id = Evidence_id
                            # add EvidenceFragmentRel conditionally
                            row_object = EvidenceFragmentRel(Evidence_id=Evidence_id,Fragment_id=Fragment_id)
                            row_object.save()
                            # add ArticleEvidenceRel conditionally
                            try:
                                row_object = Article.objects.filter(pmid_isbn=pmid_isbn).order_by('id').first()
                                if row_object == None:
                                    Article_id = None
                                else:
                                    Article_id = row_object.id
                            except Article.DoesNotExist:
                                Article_id = None
                            row_object = ArticleEvidenceRel(Article_id=Article_id,Evidence_id=Evidence_id)
                            row_object.save()
                            #end add ArticleEvidenceRel conditionally
                        #end Fragment entries - check for dups before write and find matching fragment for "original_id"

                        # add Evidence always
                        row_object = Evidence()
                        row_object.save()
                        Evidence_id = row_object.id
                        # add EpdataEvidenceRel always
                        row_object = EpdataEvidenceRel(Epdata_id=Epdata_id,Evidence_id=Evidence_id)
                        row_object.save()
                        # add EvidenceEvidenceRel always
                        Evidence1_id = Evidence_id
                        row_object = EvidenceEvidenceRel(Evidence1_id=Evidence1_id,Evidence2_id=Evidence2_id,type='interpretation')
                        row_object.save()
                        # add EvidencePropertyTypeRel
                        try:
                            iproperty   = col_unit
                            subject     = epdata_property[iproperty][isubject]
                            predicate   = epdata_property[iproperty][ipredicate]
                            object      = epdata_property[iproperty][iobject]
                            row_object  = Property.objects.get(subject=subject,predicate=predicate,object=object)
                            Property_id = row_object.id
                            #Type_id_this = row['Type_id']
                            #if Type_id_this == '':
                            #    Type_id_this = Type_id_last
                            #else:
                            #    Type_id_this = Type_id_this.strip()
                            #    Type_id_this = re.sub(r'-', r'', Type_id_this)
                            #    Type_id_this = Type_id_this[:4]
                            #    Type_id_last = Type_id_this
                            #Type_id = int(Type_id_this)
                            Type_id = row['Unique ID']
                            Type_id = re.sub(r'-', r'', Type_id)
                            Type_id = int(Type_id)
                            conflict_note = None
                            unvetted = 0
                            try:
                                row_object = EvidencePropertyTypeRel.objects.get(Evidence_id=Evidence_id,Property_id=Property_id,Type_id=Type_id,conflict_note=conflict_note,unvetted=unvetted)
                            except EvidencePropertyTypeRel.DoesNotExist:
                                row_object = EvidencePropertyTypeRel(Evidence_id=Evidence_id,Property_id=Property_id,Type_id=Type_id,conflict_note=conflict_note,unvetted=unvetted)
                                row_object.save()
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
                                                row_object = ArticleSynonymRel(Article_id=Article_id,Synonym_id=Synonym_id)
                                                row_object.save()
                                    except SynonymTypeRel.DoesNotExist:
                                        Synonym_id = None
                                except ArticleEvidenceRel.DoesNotExist:
                                    Article_id = None
                                #end add ArticleSynonymRel record if unique
                        except Property.DoesNotExist:
                            Property_id = None
                            Type_id = None
                        #end add EvidencePropertyTypeRel
                    #end if value1 is not None:
                #end if pmid_isbn != 'None given'
                #end if '{' in raw:
            except Exception:
                pass
            col_unit         = col_unit + 1
            col_property_set = col_property_set + col_properties_per_set
        #end for col in cols:
    #end def parse_and_save(row):
