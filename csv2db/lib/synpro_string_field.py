from ..models import Article, Evidence, Evidence, SynproArticleEvidenceRel, SynproEvidenceFragmentRel, SynproFragment
from ..models import article_not_found

class SynproStringField:
    def parse_and_save(self,row,count):
        fragment_id = count
        reference_id = None
        material_used = None
        location_in_reference = None
        protocol_reference = None
        location_in_protocol_reference = None
        pmid_isbn = None
        pmid_isbn_page = None
        type = None
        article_id = None
        attachment = None
        attachment_type = None
        species_tag = None
        species_descriptor = None
        age_weight = None
        protocol = None
        cell_id = None
        parameter = None
        interpretation = None
        interpretation_notes = None
        linking_cell_id = None
        linking_pmid_isbn = None
        linking_pmid_isbn_page = None
        linking_quote = None
        linking_page_location = None
        frag_id = None
        source_id = None
        target_id = None

        try:
            material_used = row['Material Used']
            if len(material_used) == 0:
                material_used = None
        except Exception:
            material_used = None
        # set location_in_reference
        try:
            location_in_reference = row['Location in reference']
            if len(location_in_reference) == 0:
                location_in_reference = None
        except Exception:
            location_in_reference = None
        # set protocol_reference
        try:
            protocol_reference = row['Protocol Reference']
            if len(protocol_reference) == 0:
                protocol_reference = None
        except Exception:
            protocol_reference = None
        # set location_in_protocol_reference
        try:
            location_in_protocol_reference = row['Location in protocol reference']
            if len(location_in_protocol_reference) == 0:
                location_in_protocol_reference = None
        except Exception:
            location_in_protocol_reference = None
        # set pmid_isbn
        try:
            if (self.synpro==''):
                pmid_isbn = int(row['PMID/ISBN'].replace('-','')) # remove dashes
                pmid_isbn = int(pmid_isbn.replace(' ','')) # remove spaces
            else:
                pmid_isbn = int(row['PMID_or_ISBN'].replace('-',''))
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
        #end set article_id
        # set type
        type = 'data'

        try:
            # synpro column settings
            if (self.synpro=='nbyk' or self.synpro=='nbym'):
                try:
                    frag_id = int(row['id'])
                    #print('**************'+str(row['id']))
                except Exception:
                    reference_id = None
                try:
                    reference_id = int(row['reference_ID'])
                    #print(reference_id)
                except Exception:
                    reference_id = None
                try:
                    material_used = row['material_used']
                    #print(material_used)
                except Exception:
                    material_used = None
                try:
                    location_in_reference = row['location_in_reference']
                except Exception:
                    location_in_reference = None
                try:
                    pmid_isbn = int(row['PMID_or_ISBN'])
                except Exception:
                    pmid_isbn = None
                try:
                    pmid_isbn_page = int(row['pmid_isbn_page'])
                except Exception:
                    pmid_isbn_page = None
                try:
                    type = row['type']
                except Exception:
                    type = None
                try:
                    attachment = row['attachment']
                except Exception:
                    attachment = None
                try:
                    attachment_type = row['attachment_type']
                    #print('test: '+str(attachment_type))
                except Exception:
                    attachment_type = None
                if (self.synpro=='nbyk'):
                    try:
                        cell_id = int(row['unique_ID'])
                    except Exception:
                        cell_id = None
                if (self.synpro=='nbyk'):
                    try:
                        source_id = int(row['cell_id'])
                    except Exception:
                        source_id = None                        
                elif (self.synpro=='nbym'):
                    try:
                        source_id = int(row['source_id'])
                    except Exception:
                        source_id = None
                    try:
                        target_id = int(row['target_id'])
                    except Exception:
                        target_id = None
                try:
                    parameter = row['parameter']
                except Exception:
                    parameter = None
                try:
                    interpretation = row['interpretation']
                except Exception:
                    interpretation = None
                try:
                    interpretation_notes = row['interpretation_notes']
                except Exception:
                    interpretation_notes = None
                try:
                    linking_cell_id = int(row['linking_cell_id'])
                except Exception:
                    linking_cell_id = None
                try:
                    linking_pmid_isbn = int(row['linking_pmid_isbn'])
                except Exception:
                    linking_pmid_isbn = None
                try:
                    linking_pmid_isbn_page = int(row['linking_pmid_isbn_page'])
                except Exception:
                    linking_pmid_isbn_page = None
                try:
                    linking_quote = row['linking_quote']
                except Exception:
                    linking_quote = None
                try:
                    linking_page_location = row['linking_page_location']
                except Exception:
                    linking_page_location = None
                try:
                    species_tag = row['species_tag']
                except Exception:
                    species_tag = None
                try:
                    strain = row['strain']
                except Exception:
                    strain = None
                try:
                    age_weight = row['age']
                except Exception:
                    age_weight = None
                try:
                    protocol = row['sections']
                except Exception:
                    protocol = None
                try:
                    cell_id = row['unique_ID']
                except Exception:
                    cell_id = None

            attachment_type = 'synpro_figure'

            row_object = SynproFragment(
                id                     = frag_id,
                original_id            = reference_id,
                quote                  = material_used,
                page_location          = location_in_reference,
                pmid_isbn              = pmid_isbn,
                pmid_isbn_page         = pmid_isbn_page,
                type                   = type,
                attachment             = attachment,
                attachment_type        = attachment_type,
                source_id              = source_id,
                target_id              = target_id,
                parameter              = parameter,
                interpretation         = interpretation,
                interpretation_notes   = interpretation_notes,
                linking_cell_id        = linking_cell_id,
                linking_pmid_isbn      = linking_pmid_isbn,
                linking_pmid_isbn_page = linking_pmid_isbn_page,
                linking_quote          = linking_quote,
                linking_page_location  = linking_page_location,
                species_tag            = species_tag,
                strain                 = strain,
                age_weight             = age_weight,
                protocol               = protocol,
                cell_id                = cell_id
            )
            try:
                row_object.save()
            except Exception as e:
                print(e)
                print(protocol)

            row_object = Evidence()
            row_object.save()
            row_object = SynproEvidenceFragmentRel(
                Evidence_id = fragment_id + 1,
                Fragment_id = fragment_id
            )
            row_object.save()
            row_object = SynproArticleEvidenceRel(
                Article_id  = article_id,
                Evidence_id = fragment_id + 1
            )
            row_object.save()
            fragment_id = fragment_id + 1

            '''
            try:
                for row in self.rows:
                    user_object = EvidencePropertyTypeRel(
                        Evidence_id=row['evidence_ID'],
                        Property_id=row['property_ID'],
                        Type_id=row['type_ID'],
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
            #print(neuron_id)
            '''
        except Exception as e:
            print(e)
        #end write fragment record(s)
        return(fragment_id)
    #end def parse_and_save(row):