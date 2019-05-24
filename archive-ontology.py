#  Load the cache in an Apache served file system with
#    downloaded RDF files
#
#
__doc__ = """Usage:

python archive-ontology.py   --root cache-root --uri URI
python archive-ontology.py   --root cache-root --uri URI --file filename
python archive-ontology.py --no  --root cache-root --uri URI

e.g. python archive-ontology --root /devel/www.w3.org/archvive \
    --webroot  /archive \
    --uri http://xmlns.com/foaf/0.1/ \
    --file foaf.rdf

e.g. pyton archive-ontology --root /devel/www.w3.org/acrhvive \
    --webroot  /archive --uri http://xmlns.com/foaf/0.1/

"""

import urllib2, urllib  # Python standard
import sys, os

from swap import notation3
from swap.webAccess import urlopenForRDF

if __name__ == '__main__':
    import getopt
    verbose = 0
    dummy = 0
    check = 0
    webroot = root = filename = uri = None;
    try:
        opts, args = getopt.getopt(sys.argv[1:], "r:u:w:f:hn",
            ["root=","webroot=", "uri=", "file=", "help", "no"])
    except getopt.GetoptError:
        # print help information and exit:
        print "Command line syntax error"
        print __doc__
        sys.exit(2)
    for o, a in opts:
        if o in ("-n", "--no"):
            dummy = 1
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        if o in ("-r", "--root"):
            root = a
        if o in ("-w", "--webroot"):
            webroot = a
        if o in ("-f", "--file"):
            filename = a
        if o in ("-u", "--uri"):
            uri = a
    # print "trace"
    if (root == None):
        print "No root directory given",
        print "Assuming /devel/www.w3.org/archive";
        root = "/devel/www.w3.org/archive";
    if (webroot == None):
        print "No server root URL path given (--webroot)",
        webroot = "/archive";
        print "Assuming "+webroot
    if (uri == None):
        print "No URI  given\n\n" + __doc__
        sys.exit(2)
    if (uri[:7] != 'http://' and uri[:7] != 'htts://'):
        print "URI is not http[s]:// URI \n" + __doc__
        sys.exit(2)


    #try:
    if filename != None:
        datafile = open(filename, "r");

    else:
        datafile = urlopenForRDF(uri);
        headers = datafile.headers
        print "Headers: " +`headers`

    #except:
    #    print "Cannot access file \n" + filename + "\n"
    #    sys.exit(3);

    data = datafile.read();
    print "Data length: ",len(data)

    if data.find("rdf") < 0 :
        print "File does not look like a data file:\n" + data[:100] + "\n"
        sys.exit(3);

    path = root + '/' +uri[7:]
    if  uri[-1:] == "/":  #  Trailing slash means a 303 style

        if not dummy:
            try:
                os.makedirs(path)
            except OSError:   # directory already exists
                pass
            try:
                htafn = path + '.htaccess'
                hta = open(htafn, 'r')
            except IOError:
                config303 = """
# This file written by archive-ontology.py
RewriteEngine On
RewriteBase """+ webroot + '/' + uri[7:]+"""

# CORS
Header set vary "Origin,Accept"
Header set access-control-allow-origin "*"
Header set access-control-allow-methods "GET, HEAD, OPTIONS"
Header set access-control-allow-headers "Link, Location, Accept-Post, Content-Type, Accept, Vary"
Header set access-control-expose-headers "User, Location, Link, Vary, Last-Modified, ETag, Allow, Content-Length, Accept"

# Rewrite rule to redirect 303 from any class or prop URI
# Any RDF term is assumed NOT to contaion a period.
# So files with extensions can be asked for without redirection
# Request for a term has to be 303'd to the ontology

RewriteRule ^[^\.]+$  ontology.rdf [R=303]

# The naked slash just gives the ontology
RewriteRule ^$  ontology.rdf

"""
                print "Writing new .htaccess file to "+htafn
                foo = open(htafn, 'w')
                foo.write(config303)
                foo.close()
            print "Writing new data file to "+path + 'ontology.rdf'
            outfile = open(path + 'ontology.rdf', "w");
            outfile.write(data);
            outfile.close();


    else:   # hash style - the path is a filename
        # Server uses conneg: we store it in a .rdf file where
        # the .rdf is not seen in the URL
        if path[-4:] != ".rdf": path += ".rdf"
        slash = path.rindex('/')
        dir = path[:slash]
        print 'mkdir -p '+dir
        if not dummy:
            try:
                os.makedirs(dir)
            except OSError:  # directory existed
                pass
        if filename:
            print 'mv %s %s' % (filename, path)
            if not dummy:  os.rename(filename, path)
            print 'ln -s %s %s' % (path, filename)
            if not dummy: os.symlink(path, filename)  ## Replace the file here with a symlink
        else:
            print "Writing to "+path
            if not dummy:
                outfile = open(path, "w");
                outfile.write(data);
                outfile.close();

        print "Done "+uri
