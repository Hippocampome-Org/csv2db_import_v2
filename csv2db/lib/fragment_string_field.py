# fragment_string_field.py

from ..models import Article, ArticleEvidenceRel, Attachment, Evidence, EvidenceFragmentRel, Fragment
from ..models import article_not_found

# ingests morph_fragment.csv, marker_fragment.csv, ep_fragment.scv and populates ArticleEvidenceRel, Evidence, EvidenceFragmentRel, Fragment
class FragmentStringField:
    def parse_and_save(row,fragment_id,saw_protocol_reference,saw_ephys_parameters_extracted):
        reference_id                   = None
        material_used                  = None
        location_in_reference          = None
        protocol_reference             = None
        location_in_protocol_reference = None
        pmid_isbn                      = None
        pmid_isbn_page                 = None
        type                           = None
        article_id                     = None
        attachment                     = None
        attachment_type                = None
        species_tag                    = None
        species_descriptor             = None
        age_weight                     = None
        protocol                       = None
        # set reference_id
        try:
            reference_id = int(row['ReferenceID'])
        except Exception:
            reference_id = None
        # set material_used
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
        #end set article_id
        # set type
        type = 'data'
        # set attachment and attachment_type
        obj = Attachment.objects.filter(original_id=reference_id, type='morph_figure').order_by('id').last()
        if obj is None:
            attachment      = None
            attachment_type = None
        else:
            attachment      = obj.name
            attachment_type = obj.type

        # inits for both marker and ephys interpretation and linking info
        cell_id                = None
        parameter              = None
        interpretation         = None
        interpretation_notes   = None
        linking_cell_id        = None
        linking_pmid_isbn      = None
        linking_pmid_isbn_page = None
        linking_quote          = None
        linking_page_location  = None

        # if marker file
        if saw_protocol_reference == 1:
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
                linking_cell_id = int(row['Linking Cell ID'].strip())
            except Exception:
                linking_cell_id = None
            # set linking_pmid_isbn
            try:
                linking_pmid_isbn = int(row['Linking PMID'].replace('-',''))
            except Exception:
                linking_pmid_isbn = None
            # set linking_pmid_isbn_page
            try:
                linking_pmid_isbn_page = int(row['linking_pmid_isbn_page'])
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
        #end if marker file

        # if ephys file
        if saw_ephys_parameters_extracted == 1:
            # set cell_id
            try:
                cell_id = int(row['Cell ID'].strip())
            except Exception:
                cell_id = None
            # set parameter
            try:
                parameter = row['Ephys Parameters Extracted'].strip()
                if len(parameter) == 0:
                    parameter = None
            except Exception:
                parameter = None
            # set interpretation
            #try:
            #    interpretation = row['Interpretation'].strip()
            #    if len(interpretation) == 0:
            #        interpretation = None
            #except Exception:
            #    interpretation = None
            # set interpretation_notes
            try:
                interpretation_notes = row['Interpretation Notes'].strip()
                if len(interpretation_notes) == 0:
                    interpretation_notes = None
            except Exception:
                interpretation_notes = None
            # set linking_cell_id
            try:
                linking_cell_id = int(row['Linking Cell ID'].strip())
            except Exception:
                linking_cell_id = None
            # set linking_pmid_isbn
            try:
                linking_pmid_isbn = int(row['Linking PMID'].replace('-',''))
            except Exception:
                linking_pmid_isbn = None
            # set linking_pmid_isbn_page
            try:
                linking_pmid_isbn_page = int(row['linking_pmid_isbn_page'])
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
        #end if ephys file
        # Morph fragment data

        if saw_ephys_parameters_extracted == 0 and saw_protocol_reference==0:
        # write fragment record(s)
            # set interpretation_notes
            try:
                interpretation_notes = row['Interpretation notes'].strip()
                if len(interpretation_notes) == 0:
                    interpretation_notes = None
            except Exception:
                interpretation_notes = None  
            try:
                species_tag = row['species_tag'].strip()
                if len(species_tag) == 0:
                    species_tag = None
            except Exception:
                species_tag = None
            # set species_descriptor
            try:
                species_descriptor = row['species_descriptor'].strip()
                if len(species_descriptor) == 0:
                    species_descriptor = None
            except Exception:
                species_descriptor = None
            try:
                age_weight = row['age_weight'].strip()
                if len(age_weight) == 0:
                    age_weight = None
            except Exception:
                age_weight = None
            # set protocol
            try:
                protocol = row['protocol'].strip()
                if len(protocol) == 0:
                    protocol = None
            except Exception:
                protocol = None
        if reference_id != None:
            # Fragment type = type
            row_object = Fragment(
                original_id            = reference_id,
                quote                  = material_used,
                page_location          = location_in_reference,
                pmid_isbn              = pmid_isbn,
                pmid_isbn_page         = pmid_isbn_page,
                type                   = type,
                attachment             = attachment,
                attachment_type        = attachment_type,
                cell_id                = cell_id,
                parameter              = parameter,
                interpretation         = interpretation,
                interpretation_notes   = interpretation_notes,
                linking_cell_id        = linking_cell_id,
                linking_pmid_isbn      = linking_pmid_isbn,
                linking_pmid_isbn_page = linking_pmid_isbn_page,
                linking_quote          = linking_quote,
                linking_page_location  = linking_page_location,
                species_tag            = species_tag,
                species_descriptor     = species_descriptor,
                age_weight             = age_weight,
                protocol               = protocol

            )
            try:
                row_object.save()
            except Exception as e:
                print(e)
                print(protocol)

            row_object = Evidence()
            row_object.save()
            row_object = EvidenceFragmentRel(
                Evidence_id = fragment_id + 1,
                Fragment_id = fragment_id
            )
            row_object.save()
            row_object = ArticleEvidenceRel(
                Article_id  = article_id,
                Evidence_id = fragment_id + 1
            )
            row_object.save()
            fragment_id = fragment_id + 1
            if saw_protocol_reference == 1:
                # Fragment type = 'protocol'
                row_object = Fragment(
                    original_id     = reference_id,
                    quote           = protocol_reference,
                    page_location   = location_in_protocol_reference,
                    pmid_isbn       = pmid_isbn,
                    pmid_isbn_page  = pmid_isbn_page,
                    type            = 'protocol',
                    attachment      = attachment,
                    attachment_type = attachment_type
                )
                row_object.save()
                row_object = Evidence()
                row_object.save()
                row_object = EvidenceFragmentRel(
                    Evidence_id = fragment_id + 1,
                    Fragment_id = fragment_id
                )
                row_object.save()
                row_object = ArticleEvidenceRel(
                    Article_id  = article_id,
                    Evidence_id = fragment_id + 1
                )
                row_object.save()
                fragment_id = fragment_id + 1
                # Fragment type = 'animal'
                row_object = Fragment(
                    original_id     = reference_id,
                    quote           = None,
                    page_location   = None,
                    pmid_isbn       = None,
                    pmid_isbn_page  = None,
                    type            = 'animal',
                    attachment      = attachment,
                    attachment_type = attachment_type
                )
                row_object.save()
                row_object = Evidence()
                row_object.save()
                row_object = EvidenceFragmentRel(
                    Evidence_id = fragment_id + 1,
                    Fragment_id = fragment_id
                )
                row_object.save()
                row_object = ArticleEvidenceRel(
                    Article_id  = article_id,
                    Evidence_id = fragment_id + 1
                )
                row_object.save()
                fragment_id = fragment_id + 1
            # end if saw_protocol_reference == 1:
        #end write fragment record(s)
        return(fragment_id)
    #end def parse_and_save(row):
