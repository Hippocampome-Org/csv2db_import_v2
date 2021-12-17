from ..models import Article, ArticleEvidenceRel, Attachment, Evidence, EvidenceFragmentRel, Fragment, ingest_errors
from ..models import article_not_found
from ..models import FiringPattern, FiringPatternRel, SpikeTime, MaterialMethod

# ingests attachment_fp.csv, fp_fragment.csv, fp_definitions.csv, fp_parameters and populates ArticleEvidenceRel, article_not_found, Evidence, EvidenceFragmentRel, FiringPattern, FiringPatternRel, Fragment,
class FiringPatternStringField:
# firing pattern attachment
    def attachment_fp_to_attachment_fp(self):
        row_num=2
        for row in self.rows:
            cell_identifier                 = None
            quote_reference_id              = None
            name_of_file_containing_figure  = None
            figure_table                    = None
            parameter                       = None
            protocol_tag                    = None
            interpretation_notes            = None
            try:
                # set cell_identifier
                if(row['Cell Identifier'].strip()):
                    cell_identifier = int(row['Cell Identifier'].strip())
                # set quote_reference_id
                try:
                    if(row['Quote reference id'].strip()):
                        quote_reference_id = row['Quote reference id']
                        quote_reference_id=int(quote_reference_id)
                except ValueError:
                    quote_reference_id = None
                # set name_of_file_containing_figure
                name_of_file_containing_figure = row['Name of file containing figure']
                if len(name_of_file_containing_figure) == 0:
                    name_of_file_containing_figure = None
                # set figure_table
                try:
                    if(row['Figure/Table'].strip()):
                        figure_table = row['Figure/Table'].strip()
                    else:
                        figure_table = None
                except ValueError:
                    figure_table = None
                # set parameter
                parameter = None
                try:
                    parameter = row['Parameter'].strip()
                    if len(parameter) == 0:
                        parameter = None
                except Exception:
                    parameter = None
                # set interpretation_notes
                try:
                    interpretation_notes = row['Interpretation notes figures'].strip()
                    if len(interpretation_notes) == 0:
                        interpretation_notes = None
                except Exception:
                    interpretation_notes = None
                # write Attachment record
                if(cell_identifier!=None):
                    row_object = Attachment(
                        cell_id              = cell_identifier,
                        original_id          = quote_reference_id,
                        name                 = name_of_file_containing_figure,
                        type                 = figure_table,
                        parameter            = parameter,
                        protocol_tag         = protocol_tag,
                        interpretation_notes = interpretation_notes
                    )
                    row_object.save()                
            except Exception as e:
                if(cell_identifier!=None):
                    try:
                        row_object = ingest_errors.objects.get(file_row_num=row_num,filename='fp_attachment.csv')
                    except ingest_errors.DoesNotExist:
                        row_object = ingest_errors(filename='fp_attachment.csv',file_row_num=row_num,comment=str(e))
                        row_object.save()
                cell_identifier= None
            row_num=row_num+1

    # firing pattern fragment
    def fp_fragment_to_fp_fragment(self):
        row_num=2          # starting header offset
        row_object  = EvidenceFragmentRel.objects.last()
        fragment_id = row_object.Fragment_id + 1                  # initialize from last fragment entry
        for row in self.rows: # is this a morph_fragment.csv file or a marker_fragment.csv file
            reference_id                   = None
            cell_id                        = None
            material_used                  = None
            location_in_reference          = None
            pmid_isbn                      = None
            pmid_isbn_page                 = None
            type                           = None
            article_id                     = None
            attachment                     = None
            attachment_type                = None
            # set reference_id

            try:
                if(row['ReferenceID'].strip()):
                    reference_id = row['ReferenceID'].strip()
                    reference_id = int(reference_id)
                try:
                    material_used = row['Material Used']
                    if len(material_used) == 0:
                        material_used = None
                except Exception:
                    material_used = None
                # cell id    
                try:
                    if(row['Cell ID'].strip()):
                        cell_id = int(row['Cell ID'].strip())
                except Exception:
                    cell_id = None
                # set location_in_reference
                try:
                    location_in_reference = row['Location in reference']
                    if len(location_in_reference) == 0:
                        location_in_reference = None
                except Exception:
                    location_in_reference = None
                # set pmid_isbn
                try:
                    if(row['PMID/ISBN'].replace('-','').strip()):
                        pmid_isbn = int(row['PMID/ISBN'].replace('-',''))
                except Exception:
                    pmid_isbn = None
                # set pmid_isbn_page
                try:
                    pmid_isbn_page = int(row['pmid_isbn_page'])
                except Exception:
                    pmid_isbn_page = None
                # set article_id
                if pmid_isbn == None:
                    article_id = None
                else:
                    row_object = None
                    if pmid_isbn_page != None:
                        if pmid_isbn_page == 0:
                            try:
                                row_object = Article.objects.filter(pmid_isbn=pmid_isbn).order_by('id').first()
                            except Article.DoesNotExist:
                                article_id = None
                        else:
                            try:
                                row_object = Article.objects.get(pmid_isbn=pmid_isbn,first_page=pmid_isbn_page)
                            except Article.DoesNotExist:
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
                    if article_id == None:
                        # write new pmid_isbn to article_not_found
                        try:
                            row_object = article_not_found.objects.get(pmid_isbn=pmid_isbn)
                        except article_not_found.DoesNotExist:
                            row_object = article_not_found(pmid_isbn=pmid_isbn)
                            row_object.save()
                        try:
                            row_object = ingest_errors.objects.get(field='PMID/ISBN',value=pmid_isbn,file_row_num=row_num,filename='fp_fragment.csv')
                        except ingest_errors.DoesNotExist:
                            row_object = ingest_errors(field='PMID/ISBN',value=pmid_isbn,filename='fp_fragment.csv',file_row_num=row_num,comment='invalid pmid/isbn value')
                            row_object.save()
                #end set article_id
                # set type
                attachment      = None
                attachment_type = None
                type_fragment = 'data'
                

                # inits for both marker and ephys interpretation and linking info
                
                parameter              = None
                interpretation         = None
                interpretation_notes   = None
                linking_cell_id        = None
                linking_pmid_isbn      = None
                linking_pmid_isbn_page = None
                linking_quote          = None
                linking_page_location  = None
                
                # set interpretation
                try:
                    interpretation = row['Interpretation'].strip()
                    if len(interpretation) == 0:
                        interpretation = None
                except Exception:
                    interpretation = None
                # set interpretation_notes
                try:
                    interpretation_notes = row['Interpretation Notes'].strip()
                    if len(interpretation_notes) == 0:
                        interpretation_notes = None
                except Exception:
                    interpretation_notes = None
                # set linking_cell_id
                try:
                    parameter = row['Firing_Pattern'].strip()
                    if len(parameter) == 0:
                        parameter = None
                except Exception:
                    parameter = None
                try:
                    linking_cell_id = int(row['Linking Cell ID'].strip())
                except Exception:
                    linking_cell_id = None
                # set linking_pmid_isbn
                try:
                    linking_pmid_isbn = int(row['Linking PMID'].replace('-','').strip())
                except Exception:
                    linking_pmid_isbn = None
                # set linking_pmid_isbn_page
                try:
                    linking_pmid_isbn_page = int(row['Linking_pmid_isbn_page'].strip())
                except Exception:
                    linking_pmid_isbn_page = None
                # set linking_quote
                try:
                    linking_quote = row['Linking Quote'].strip()
                    if len(linking_quote) == 0:
                        linking_quote = None
                except Exception:
                    linking_quote = None
                # set linking_page_location
                try:
                    linking_page_location = row['Linking Quote Location'].strip()
                    if len(linking_page_location) == 0:
                        linking_page_location = None
                except Exception:
                    linking_page_location = None

                if reference_id != None:
                    # Fragment type = type
                    row_object = Fragment(
                        id                     = fragment_id,
                        original_id            = reference_id,
                        quote                  = material_used,
                        page_location          = location_in_reference,
                        pmid_isbn              = pmid_isbn,
                        pmid_isbn_page         = pmid_isbn_page,
                        cell_id                = cell_id,
                        type                   = type_fragment,
                        parameter              = parameter,
                        interpretation         = interpretation,
                        interpretation_notes   = interpretation_notes,
                        linking_cell_id        = linking_cell_id,
                        linking_pmid_isbn      = linking_pmid_isbn,
                        linking_pmid_isbn_page = linking_pmid_isbn_page,
                        linking_quote          = linking_quote,
                        linking_page_location  = linking_page_location
                    )
                    row_object.save()
                    fragment_id=row_object.id
                    row_object = Evidence()
                    row_object.save()
                    evidence_id=row_object.id
                    row_object = EvidenceFragmentRel(
                        Evidence_id = evidence_id,
                        Fragment_id = fragment_id
                    )
                    row_object.save()
                    #evidence_id=row_object.id
                    row_object = ArticleEvidenceRel(
                        Article_id  = article_id,
                        Evidence_id = evidence_id
                    )
                    row_object.save()
                    fragment_id=fragment_id+1

            except Exception as e:
                if(reference_id!=None):
                    try:
                        row_object = ingest_errors.objects.get(file_row_num=row_num,filename='fp_fragment.csv')
                    except ingest_errors.DoesNotExist:
                        row_object = ingest_errors(filename='fp_fragment.csv',file_row_num=row_num,comment=str(e))
                        row_object.save()
                reference_id=None
            row_num=row_num+1
            
    # firing pattern parameters
    def parameters_to_parameters(self):
        row_num=2 
        for row in self.rows:
            type_id=None
            fig_no=None
            reference_id=None
            istim=None
            tstim=None
            firingPattern_id=None
            try:
                type_id=row['Uniq ID']
                type_id=int(type_id.replace('-',''))
                fig_no=row['Figure number']
                if(row['ReferenceID'].strip()):
                    reference_id = row['ReferenceID'].strip()
                    reference_id = int(reference_id)
                    try:
                        row_object = Fragment.objects.get(original_id=reference_id)
                    except Fragment.DoesNotExist:
                        try:
                            row_object = ingest_errors.objects.get(field='ReferenceID',value=reference_id,filename='fp_parameters.csv')
                        except ingest_errors.DoesNotExist:
                            row_object = ingest_errors(field='ReferenceID',value=reference_id,filename='fp_parameters.csv',file_row_num=row_num,comment='ReferenceID value not found in fragment')
                            row_object.save()
                    istim=row['Istim (pA)']
                    tstim=row['Tstim (ms)']
                    firingPattern_id=FiringPatternStringField.firing_pattern_definition_parameter(row,'parameter')
                    row_object = FiringPatternRel(
                        FiringPattern_id    = firingPattern_id,
                        Type_id             = type_id,
                        figure_no           = fig_no,
                        original_id         = reference_id,
                        istim_pa            = istim,
                        tstim_ms            = tstim
                    )
                    row_object.save()
                    FiringPatternRel_id=row_object.id
                    # save spiking data
                    for index in range(1,100):
                        spike_name          = "ISI"
                        spike_data          = None

                        spike_name+=str(index)
                        spike_data=row[spike_name]

                        row_object = SpikeTime(
                            FiringPattern_id    = firingPattern_id,
                            spike_name          = spike_name,
                            spike_data          = spike_data
                        )
                        row_object.save()

            except Exception as e:
                try:
                    row_object = ingest_errors.objects.get(file_row_num=row_num,filename='fp_parameters.csv')
                except ingest_errors.DoesNotExist:
                    row_object = ingest_errors(filename='fp_parameters.csv',file_row_num=row_num,comment=str(e))
                    row_object.save()
                type_id=None
                reference_id=None
                firingPattern_id=None
            row_num=row_num+1

    # firing pattern definition
    def definition_to_definition(self):
        cnt=0;
        row_num=1
        #load definition name of parameters
        FiringPatternStringField.firing_pattern_definition_parameter(None,'names')
        for row in self.rows:
            try:
                if(cnt<4):
                    FiringPatternStringField.firing_pattern_definition_parameter(row,'none')
                else:
                    FiringPatternStringField.firing_pattern_definition_parameter(row,'definition')
                cnt=cnt+1
                row_num=row_num+1
            except Exception as e:
                try:
                    row_object = ingest_errors.objects.get(file_row_num=row_num,filename='fp_definitions.csv')
                except ingest_errors.DoesNotExist:
                    row_object = ingest_errors(filename='fp_definitions.csv',file_row_num=row_num,comment=str(e))
                    row_object.save()
            row_num=row_num+1
    
    # helper function for importing firing pattern definitons and parameters 
    def firing_pattern_definition_parameter(row,parameter_value):
        firingParameters=["Delay (ms)","PFS(ms)","SWA (mV)","NISI"," ISIAV (ms)","SD (ms)","Max ISI (ms)","Min ISI (ms)","1st ISI (ms)","ISIAV1-2  (ms)","ISIAV1-3 (ms)","ISIAV1-4 (ms)","Last ISI (ms)","ISIAVn-n-1 (ms)","ISIAVn-n-2 (ms)","ISIAVn-n-3 (ms)","MaxISI/MinISI","MaxISIn /ISIn-1","MaxISIn /ISIn+1","AI = (ISIAVn-n-2 - ISIAV1-3)/ ISIAVn-n-2","RDmax    (RDi=|ISIi-ISIAV|/ISIAV )","DF=(Delay-2 ISIAV1-2)/Delay","SF=(PSF-2 ISIAVn-n-1)/PSF","Tmax(scaled)","ISImax(scaled)","ISIav (scaled)","SD(scaled)","Slope","Intercept","Slope1","Intercept1","Css (Yc1)","Xc1","Slope2","Intercept2","Slope3","Intercept3","Xc2","Yc2","F1-2","F1-2crit","F2-3","F2-3crit","F3-4","F3-4crit","P1-2","P2-3","P3-4","P1-2uv","P2-3uv","P3-4uv","ISIi/ISIi-1","i","ISIav(i,n)/ISI1,i-1","MaxISIj /ISIj-1","MaxISIj /ISIj+1","NISI_c"," ISIAV (ms)_c","Max ISI (ms)_c","Min ISI (ms)_c","1st ISI (ms)_c","Tmax(scaled) _c","ISImax(scaled)_c","ISIav (scaled) _c","SD(scaled) _c","Slope_c","Intercept_c","no value_c","Intercept1_c","Css (Yc1) _c","Xc1_c","Slope2_c","Intercept2_c","Slope3_c","Intercept3_c","Xc2_c","Yc2_c","F1-2_c","F1-2crit_c","F2-3_c","F2-3crit_c","F3-4_c","F3-4crit_c","P1-2_c","P2-3_c","P3-4_c","P1-2uv_c","P2-3uv_c","P3-4uv_c","M_2p","C_2p","M_3p","C1_3p","C2_3p","M1_4p","C1_4p","M2_4p","C2_4p","N_ISI_cut_3p","N_ISI_cut_4p","F_12","F_crit_12","F_23","F_crit_23","F_34","F_crit_34","P_12","P_12_UV","P_23","P_23_UV","P_34","P_34_UV","M_FASP","C_FASP","N_ISI_cut_FASP","Original  FP names "]
        firingDefinitions=["Delay ","PFS","SWA ","NISI"," ISIAV ","SD ","Max ISI ","Min ISI ","1st ISI ","ISIAV1-2  ","ISIAV1-3 ","ISIAV1-4 ","Last ISI ","ISIAVn-n-1 ","ISIAVn-n-2 ","ISIAVn-n-3 ","MaxISI/MinISI","MaxISIn /ISIn-1","MaxISIn /ISIn+1","AI = (ISIAVn-n-2 - ISIAV1-3)/ ISIAVn-n-2","RDmax    (RDi=|ISIi-ISIAV|/ISIAV )","DF=(Delay-2 ISIAV1-2)/Delay","SF=(PSF-2 ISIAVn-n-1)/PSF","Tmax(scaled)","ISImax(scaled)","ISIav (scaled)","SD(scaled)","Slope","Intercept","Slope1","Intercept1","Css (Yc1)","Xc1","Slope2","Intercept2","Slope3","Intercept3","Xc2","Yc2","F1-2","F1-2crit","F2-3","F2-3crit","F3-4","F3-4crit","P1-2","P2-3","P3-4","P1-2uv","P2-3uv","P3-4uv","ISIi/ISIi-1","i","ISIav(i,n)/ISI1,i-1","MaxISIj /ISIj-1","MaxISIj /ISIj+1","NISI_c"," ISIAV (ms)_c","Max ISI (ms)_c","Min ISI (ms)_c","1st ISI (ms)_c","Tmax(scaled) _c","ISImax(scaled)_c","ISIav (scaled) _c","SD(scaled) _c","Slope_c","Intercept_c","Slope1_c","Intercept1_c","Css (Yc1) _c","Xc1_c","Slope2_c","Intercept2_c","Slope3_c","Intercept3_c","Xc2_c","Yc2_c","F1-2_c","F1-2crit_c","F2-3_c","F2-3crit_c","F3-4_c","F3-4crit_c","P1-2_c","P2-3_c","P3-4_c","P1-2uv_c","P2-3uv_c","P3-4uv_c","M_2p","C_2p","M_3p","C1_3p","C2_3p","M1_4p","C1_4p","M2_4p","C2_4p","N_ISI_cut_3p","N_ISI_cut_4p","F_12","F_crit_12","F_23","F_crit_23","F_34","F_crit_34","P_12","P_12_UV","P_23","P_23_UV","P_34","P_34_UV","M_FASP","C_FASP","N_ISI_cut_FASP","Firing pattern names"]      
        header=[None]*len(firingDefinitions)
        result=[None]*len(firingDefinitions)
        if(parameter_value=='definition' or parameter_value=='none' or parameter_value=='parameter'):
            overall_fp=row['OVERALL FIRING PATTERN']
            if(parameter_value=='definition'):
                overall_fp=row['OVERALL FIRING PATTERN 2']
            elif(parameter_value=='parameter'):
                overall_fp=row['OVERALL FIRING PATTERN']

            if(parameter_value=='definition' or parameter_value=='none'):
                header=firingDefinitions
            else:
                header=firingParameters
            for index in range(0,len(header)):
                result[index]=row[header[index]]
        else:
            overall_fp="Parameter Name"
            parameter_value='none'
            for index in range(0,len(header)):
                result[index]=firingDefinitions[index]
                
        row_object = FiringPattern(
            overall_fp                          =overall_fp,
            delay_ms                            =result[0],
            pfs_ms                              =result[1],
            swa_mv                              =result[2],
            nisi                                =result[3],
            isiav_ms                            =result[4],
            sd_ms                               =result[5],
            max_isi_ms                          =result[6],
            min_isi_ms                          =result[7],
            first_isi_ms                        =result[8],
            isiav1_2_ms                         =result[9],
            isiav1_3_ms                         =result[10],
            isiav1_4_ms                         =result[11],
            last_isi_ms                         =result[12],
            isiavn_n_1_ms                       =result[13],
            isiavn_n_2_ms                       =result[14],
            isiavn_n_3_ms                       =result[15],
            maxisi_minisi                       =result[16],
            maxisin_isin_m1                     =result[17],
            maxisin_isin_p1                     =result[18],
            ai                                  =result[19],
            rdmax                               =result[20],
            df                                  =result[21],
            sf                                  =result[22],
            tmax_scaled                         =result[23],
            isimax_scaled                       =result[24],
            isiav_scaled                        =result[25],
            sd_scaled                           =result[26],
            slope                               =result[27],
            intercept                           =result[28],
            slope1                              =result[29],
            intercept1                          =result[30],
            css_yc1                             =result[31],
            xc1                                 =result[32],
            slope2                              =result[33],
            intercept2                          =result[34],
            slope3                              =result[35],
            intercept3                          =result[36],
            xc2                                 =result[37],
            yc2                                 =result[38],
            f1_2                                =result[39],
            f1_2crit                            =result[40],
            f2_3                                =result[41],
            f2_3crit                            =result[42],
            f3_4                                =result[43],
            f3_4crit                            =result[44],
            p1_2                                =result[45],
            p2_3                                =result[46],
            p3_4                                =result[47],
            p1_2uv                              =result[48],
            p2_3uv                              =result[49],
            p3_4uv                              =result[50],
            isii_isii_m1                        =result[51],
            i                                   =result[52],
            isiav_i_n_isi1_i_m1                 =result[53],
            maxisij_isij_m1                     =result[54],
            maxisij_isij_p1                     =result[55],
            nisi_c                              =result[56],
            isiav_ms_c                          =result[57],
            maxisi_ms_c                         =result[58],
            minisi_ms_c                         =result[59],
            first_isi_ms_c                      =result[60],
            tmax_scaled_c                       =result[61],
            isimax_scaled_c                     =result[62],
            isiav_scaled_c                      =result[63],
            sd_scaled_c                         =result[64],
            slope_c                             =result[65],
            intercept_c                         =result[66],
            slope1_c                            =result[67],
            intercept1_c                        =result[68],
            css_yc1_c                           =result[69],
            xc1_c                               =result[70],
            slope2_c                            =result[71],
            intercept2_c                        =result[72],
            slope3_c                            =result[73],
            intercept3_c                        =result[74],
            xc2_c                               =result[75],
            yc2_c                               =result[76],
            f1_2_c                              =result[77],
            f1_2crit_c                          =result[78],
            f2_3_c                              =result[79],
            f2_3crit_c                          =result[80],
            f3_4_c                              =result[81],
            f3_4crit_c                          =result[82],
            p1_2_c                              =result[83],
            p2_3_c                              =result[84],
            p3_4_c                              =result[85],
            p1_2uv_c                            =result[86],
            p2_3uv_c                            =result[87],
            p3_4uv_c                            =result[88],
            m_2p                                =result[89],      
            c_2p                                =result[90],
            m_3p                                =result[91],
            c1_3p                               =result[92],
            c2_3p                               =result[93],
            m1_4p                               =result[94],
            c1_4p                               =result[95],
            m2_4p                               =result[96],
            c2_4p                               =result[97],
            n_isi_cut_3p                        =result[98],
            n_isi_cut_4p                        =result[99],
            f_12                                =result[100],
            f_crit_12                           =result[101],
            f_23                                =result[102],
            f_crit_23                           =result[103],
            f_34                                =result[104],
            f_crit_34                           =result[105],
            p_12                                =result[106],
            p_12_uv                             =result[107],
            p_23                                =result[108],
            p_23_uv                             =result[109],
            p_34                                =result[110],
            p_34_uv                             =result[111],
            m_fasp                              =result[112],
            c_fasp                              =result[113],
            n_isi_cut_fasp                      =result[114],
            fp_name                             =result[115].strip(),
            definition_parameter                =parameter_value  
        )
        row_object.save()
        firing_pattern_id=row_object.id
        return firing_pattern_id
    
    # # helper function for importing Animals, Preparations, Artificial cerebrospinal fluid and Recording method/Pipette solutions. 
    def materials_to_method(self):
        cnt = 0
        #Start reading row number
        row_num = 1
        for row in self.rows:
            cnt = cnt+1
            if cnt > 1:
                try:
                    result = [None]*len(row)
                    for index in range(0,len(row)):
                        result[index] = row[index]
                    # find row from FiringPattern update it
                    overall_fp = result[9]
                    #remove - frop type id
                    type_id = result[2]
                    if cnt > 2:
                        try:
                            if(type_id.replace('-','').strip()):
                                type_id = int(type_id.replace('-',''))
                        except Exception:
                            # write new pmid_isbn to article_not_found
                            row_object = ingest_errors(field='Uniqu ID',value=type_id,filename='materials_methods.csv',file_row_num=row_num,comment='invalid Unique Id value')
                            row_object.save()
                            type_id = None
                    else: 
                        type_id = None
                    # set pmid_isbn
                    pmid_isbn = result[4]
                    if cnt > 2:
                        try:
                            if(pmid_isbn.replace('-','').strip()):
                                pmid_isbn = int(pmid_isbn.replace('-',''))
                        except Exception:
                            # write new pmid_isbn to article_not_found
                            try:
                                row_object = article_not_found.objects.get(pmid_isbn=pmid_isbn)
                            except article_not_found.DoesNotExist:
                                row_object = article_not_found(pmid_isbn=pmid_isbn)
                                row_object.save()
                            pmid_isbn = None
                    else:
                        pmid_isbn = None
                    # Remove no data rows
                    if( "No_data" not in overall_fp):
                        row_object = MaterialMethod(
                            unique_id                           = type_id,
                            overall_fp                          = overall_fp,
                            pmid_isbn                           = pmid_isbn,
                            subtypes                            = result[3],
                            figure_no                           = result[5],
                            istim_pa                            = result[6],
                            tstim_ms                            = result[7],
                            species                             = result[10],
                            inbred_strain                       = result[11],
                            age_postnatal_days                  = result[12],
                            sex                                 = result[13],
                            weight                              = result[14],
                            type_of_preparation                 = result[16],
                            orientation                         = result[17],
                            thickness                           = result[18],
                            nacl                                = result[20],
                            kcl                                 = result[21],
                            cacl2                               = result[22],
                            nah2po4                             = result[23],
                            kh2po4                              = result[24],
                            mgcl2                               = result[25],
                            mgso4                               = result[26],
                            nahco3                              = result[27],
                            hepes                               = result[28],
                            napyr                               = result[29],
                            glucose                             = result[30],
                            o2                                  = result[31],
                            co2                                 = result[32],
                            t                                   = result[33],
                            kyna                                = result[34],
                            cnqx                                = result[35],
                            d_ap5                               = result[36],
                            bcc                                 = result[37],
                            recording_method                    = result[39],
                            gramicidine                         = result[40],
                            kmeso4                              = result[41],
                            kglu                                = result[42],
                            kac                                 = result[43],
                            cscl                                = result[44],
                            kcl_ps                              = result[45],
                            nacl_ps                             = result[46],
                            mgcl2_ps                            = result[47],
                            cacl2_ps                            = result[48],
                            hepes_ps                            = result[49],
                            qx_314                              = result[50],
                            egta                                = result[51],
                            na_egta                             = result[52],
                            atp                                 = result[53],
                            mg_atp                              = result[54],
                            na2_atp                             = result[55],
                            gtp                                 = result[56],
                            na_gtp                              = result[57],
                            na2_gtp                             = result[58],
                            na3_gtp                             = result[59],
                            mg_gtp                              = result[60],
                            pcr                                 = result[61],
                            na_pcr                              = result[62],
                            na2_pcr                             = result[63],
                            bc                                  = result[64],
                            ly                                  = result[65],
                            nb                                  = result[66],
                            af594                               = result[67]
                        )
                        row_object.save()
                
                except Exception as e:
                    row_object = ingest_errors(filename='materials_methods.csv',file_row_num=row_num,comment=str(e))
                    row_object.save()
            row_num=row_num+1   