PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(DKIM_VERSION)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/opendkim-$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q http://sourceforge.net/projects/opendkim/files/opendkim-$(pvers).tar.gz \
	)
else
	@echo "Already have the source, skipping download"
endif

pkgadd:
	$(PKG_EXTRACT) zimbra-base zimbra-openssl-$(PKG_DEV) zimbra-libbsd-$(PKG_DEV) \
	zimbra-libmilter-$(PKG_DEV) zimbra-openldap-$(PKG_DEV) zimbra-cyrus-sasl-$(PKG_DEV)

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base

setup:
	$(generic-setup)

build: pkgadd setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-opendkim/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/opendkim.spec && \
 	$(replace-pathinfo) SPECS/opendkim.spec && \
	cp ../../../../src/opendkim-$(pvers).tar.gz SOURCES/zimbra-opendkim-$(pvers).tar.gz && \
 	$(PKG_BUILD) SPECS/opendkim.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-opendkim/debian/changelog zimbra-opendkim/debian/zimbra-opendkim-lib.shlibs && \
 	$(replace-pathinfo) zimbra-opendkim/debian/rules && \
	cp ../../src/opendkim-$(pvers).tar.gz zimbra-opendkim_$(pvers).orig.tar.gz && \
	tar xfz zimbra-opendkim_$(pvers).orig.tar.gz --strip-components=1  -C zimbra-opendkim && \
	cd zimbra-opendkim && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
