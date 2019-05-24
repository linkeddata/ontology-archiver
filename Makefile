

all : all.n3 all.txt action

all.n3 :
	curl http://prefix.cc/popular/all.file.n3 > all.n3
all.txt :
	curl http://prefix.cc/popular/all.file.txt > all.txt
list : all.txt
	sed -e 's/^.*http/http/' < all.txt | sed  -e 's?#??' | sed -e '/\?\?\?/d' > list
root.n3 : all.n3
	sed -e 's?@prefix [a-z0-9]*:?<#root> <http://www.w3.org/2000/01/rdf-schema#seeAlso>?' < all.n3 |\
		sed -e 's?#>?>?' > root.n3
action : list
	cat list | sed -e 's?\(.*\)?curl -HAccept:application/rdf+xml \1 > holding/`echo \1 | openssl dgst -sha1`.rdf?' > action
heads : list
	cat list | sed -e 's?\(.*\)?curl -I -HAccept:application/rdf+xml \1 > holding/`echo \1 | openssl dgst -sha1`.head?' > heads

key.txt : list
	cat list | sed -e 's?\(.*\)? echo \1; ls -l  holding/`echo \1 | openssl dgst -sha1 `.rdf?' > makekey
	chmod +x makekey
	./makekey > key.txt

