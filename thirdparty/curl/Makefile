PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(CURL_VERSION)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/curl-$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q http://curl.haxx.se/download/curl-$(pvers).tar.gz \
	)
else
	@echo "Already have the source, skipping download"
endif

pkgadd:
	$(PKG_EXTRACT) zimbra-base zimbra-openssl-$(PKG_DEV) zimbra-heimdal-$(PKG_DEV)

pkgrm: pkgrm%

pkgrm%:
	$(PKG_PURGE) zimbra-base

setup:
	$(generic-setup)

build: pkgadd setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-curl/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(replace-pkginfo) SPECS/curl.spec && \
	$(replace-pathinfo) SPECS/curl.spec && \
	cp ../../../../src/curl-$(pvers).tar.gz SOURCES/zimbra-curl-$(pvers).tar.gz && \
	$(PKG_BUILD) SPECS/curl.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
	$(replace-pkginfo) zimbra-curl/debian/changelog zimbra-curl/debian/zimbra-curl-lib.shlibs && \
	$(replace-pathinfo) zimbra-curl/debian/rules && \
	cp ../../src/curl-$(pvers).tar.gz zimbra-curl_$(pvers).orig.tar.gz && \
	tar xfz zimbra-curl_$(pvers).orig.tar.gz --strip-components=1  -C zimbra-curl && \
	cd zimbra-curl && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
