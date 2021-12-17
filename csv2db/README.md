## csv2db

### Hippocampome CSV file to MySQL database ingest capability

### Description
The "csv2db" capability ingests Hippocampome data in the form of Comma Separated Value (CSV) files and loads those data into a MySQL database. This capability was written in Django/Python. It is used to import the neuroinformatic results of mining peer-reviewed literature for the Hippocampome project (GMU Krasnow CN3 Ascoli lab) into a MySQL database for machine-readable web portal rendering (http://hippocampome.org/). Both browser based and command line interfaces are facilitated.

### Install
To install and run "csv2db", the following versions (or later) of base code should be available (i.e. installed and configured) on the target platform.
- Apache (2.2.26)
- Python (3.4.2)
- mod-wsgi (4.3.0)
- MySQL (5.6.16)
- PyMySQL (0.6.2)
- Django (1.7.1) https://www.djangoproject.com/

### Configure
- git clone https://github.com/Hippocampome-Org/csv2db
- CREATE DATABASE hippocampome DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
- CREATE USER 'hdb'@'localhost' IDENTIFIED BY 'somepasswd';
- GRANT ALL PRIVILEGES ON hippocampome.* TO 'hdb'@'localhost' WITH GRANT OPTION;

### Input
#### "all.csv"
##### process order,csv filename,tables populated
- 1,type.csv,"Type(all but notes field)"
- 2,packet_notes.csv,"Type(updates notes field)"
- 3,known_connections.csv,"TypeTypeRel"
- 4,synonym.csv,"Synonym, SynonymTypeRel"
- 5,article.csv,"Article, ArticleAuthorRel, Author"
- 6,attachment_morph.csv,"Attachment, FragmentTypeRel"
- 7,attachment_marker.csv,"Attachment"
- 8,attachment_ephys.csv,"Attachment"
- 9,morph_fragment.csv,"ArticleEvidenceRel, Evidence, EvidenceFragmentRel, Fragment, FragmentTypeRel(updates Fragment_id field)"
- 10,marker_fragment.csv,"ArticleEvidenceRel, Evidence, EvidenceFragmentRel, Fragment"
- 11,markerdata.csv,"ArticleSynonymRel, Evidence, EvidenceEvidenceRel, EvidenceMarkerdataRel, EvidencePropertyTypeRel, Markerdata, Property"
- 12,epdata.csv,"ArticleEvidenceRel, ArticleSynonymRel, Epdata, EpdataEvidenceRel, Evidence, EvidenceEvidenceRel, EvidenceFragmentRel, EvidencePropertyTypeRel, Fragment, Property"
- 13,morphdata.csv,"ArticleSynonymRel, EvidencePropertyTypeRel, Property"

### Process (command line)
- python manage.py truncate
- python manage.py load

### Output
- mysqldump -u hdb -p hippocampome > hippocampome.sql
