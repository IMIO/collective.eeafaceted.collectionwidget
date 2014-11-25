#!/usr/bin/make
#
all: run

.PHONY: bootstrap buildout run test cleanall
bin/buildout: bootstrap.py buildout.cfg
	virtualenv-2.7 .
	./bin/python bootstrap.py --setuptools-version=7.0 --version=2.2.5
	touch $@

buildout: bin/buildout
	bin/buildout -Nvt 5

bootstrap: bin/buildout

run: bin/instance 
	bin/instance fg

bin/instance: bin/buildout
	bin/buildout -Nvt 5
	touch $@

test: bin/test
	rm -fr htmlcov
	bin/test

bin/test: bin/buildout
	bin/buildout -Nvt 5
	touch $@

cleanall:
	rm -fr bin develop-eggs htmlcov include .installed.cfg lib .mr.developer.cfg parts downloads eggs