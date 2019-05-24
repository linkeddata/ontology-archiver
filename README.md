# ontology-archiver
Copy favorite and commonly used RDF schemas/ontologies to a safe place

## To archive a file into file space
```
python archive-ontology.py   --root cache-root --uri URI
python archive-ontology.py   --root cache-root --uri URI --file filename
python archive-ontology.py --no  --root cache-root --uri URI

e.g. python archive-ontology --root /devel/www.w3.org/archvive \
    --webroot  /archive \
    --uri http://xmlns.com/foaf/0.1/ \
    --file foaf.rdf

e.g. pyton archive-ontology --root /devel/www.w3.org/acrhvive \
    --webroot  /archive --uri http://xmlns.com/foaf/0.1/
```
Typically you can archive an onology into a working copy of repo which you can then check into
some web space.

## List of popular ontologies:
```
make all.ttl
```
This grabs a list from `prefix.cc`, a website where people suggest porefixes for common ontologies.


all untested code use at your own risk
