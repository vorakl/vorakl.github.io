OUTPUTDIR ?= /home/vorakl/repos/my/github/vorakl.github.io
THEMEDIR ?= /home/vorakl/repos/my/github/aves/theme
PLUGINSDIR ?= /home/vorakl/repos/others/pelican-plugins
SITEMAP ?= https%3A%2F%2Fvorakl.com%2Fsitemap.xml

PY ?= python
PELICAN ?= pelican
PELICANOPTS =

BASEDIR = $(CURDIR)
INPUTDIR = $(BASEDIR)/content
DEVCONF = sitedev.py
PRODCONF = siteprod.py
STATICDIR = $(BASEDIR)/theme/static
UID = $(shell id -u)
GID = $(shell id -g)

GITHUB_PAGES_BRANCH=master

DEBUG ?= 0
ifeq ($(DEBUG), 1)
	PELICANOPTS += -D
endif

RELATIVE ?= 0
ifeq ($(RELATIVE), 1)
	PELICANOPTS += --relative-urls
endif

.PHONY: help dev prod bundle run deploy

help:
	@echo 'Makefile for building a static web site                                           '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make dev                        (re)generate the web site              '
	@echo '   make prod                       generate using production settings     '
	@echo '   make run [PORT=8000]            serve site at http://localhost:8000/   '
	@echo '   make deploy                     push the web site to GitHub            '
	@echo '   make clean                      remove temporary files                 '
	@echo '                                                                          '
	@echo 'Set the DEBUG variable to 1 to enable debugging, e.g. make DEBUG=1 html   '
	@echo 'Set the RELATIVE variable to 1 to enable relative urls                    '
	@echo '                                                                          '

dev:   
	@if docker version &>/dev/null; then \
		echo 'Building a local web-site using docker image'; \
		docker run \
		    --rm \
		    -u $(UID):$(GID) \
		    -v $(BASEDIR):/site \
		    -v $(INPUTDIR):/input \
		    -v $(OUTPUTDIR):/output \
		    -v $(THEMEDIR):/theme \
		    -v $(PLUGINSDIR):/plugins \
		    vorakl/alpine-pelican \
	                -F 'cd /site && pelican /input -o /output -t /theme -s $(DEVCONF) $(PELICANOPTS)'; \
	else \
		echo 'ERROR: there is no a running Docker daemon' >&2; \
		exit 1; \
	fi

prod: 
	@if docker version &>/dev/null; then \
		echo 'Building a public web-site using docker image'; \
		docker run \
		    --rm \
		    -u $(UID):$(GID) \
		    -v $(BASEDIR):/site \
		    -v $(INPUTDIR):/input \
		    -v $(OUTPUTDIR):/output \
		    -v $(THEMEDIR):/theme \
		    -v $(PLUGINSDIR):/plugins \
		    vorakl/alpine-pelican \
	                -F 'cd /site && pelican /input -o /output -t /theme -s $(PRODCONF) $(PELICANOPTS)'; \
	else \
		echo 'ERROR: there is no a running Docker daemon' >&2; \
		exit 1; \
	fi

run:
	@if docker version &>/dev/null; then \
		echo 'Launching a docker container with Nginx'; \
		docker run \
		    --rm \
		    -it \
		    --net host \
		    -v $(OUTPUTDIR):/usr/share/nginx/html \
		    nginx:mainline-alpine; \
	fi

deploy:	
	@echo 'Deploying site to Production environment'
	@cd $(OUTPUTDIR) && \
	  git add . && \
	  git commit -m "New content" && \
	  git push origin $(GITHUB_PAGES_BRANCH)

clean:
	@find . -name "*~" -exec rm -vf {} \;
