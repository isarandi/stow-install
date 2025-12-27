PREFIX ?= /usr/local

all:
	echo '#!/bin/sh' > dummy
	echo 'echo "dummy 1.0"' >> dummy
	chmod +x dummy

install:
	mkdir -p $(DESTDIR)$(PREFIX)/bin
	cp dummy $(DESTDIR)$(PREFIX)/bin/
