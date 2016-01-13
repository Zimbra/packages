PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(CYRUS_VERSION)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/cyrus-sasl-$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q ftp://ftp.cyrusimap.org/cyrus-sasl/cyrus-sasl-$(pvers).tar.gz \
	)
else
	@echo "Already have the source, skipping download"
endif

pkgadd:
	$(PKG_EXTRACT) zimbra-base zimbra-openssl-$(PKG_DEV) zimbra-heimdal-$(PKG_DEV) \
	zimbra-curl-$(PKG_DEV) zimbra-libxml2-$(PKG_DEV)

pkgrm: pkgrm%

pkgrm%:
	$(PKG_PURGE) zimbra-base

setup:
	$(generic-setup)

build: pkgadd setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-cyrus-sasl/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(replace-pkginfo) SPECS/cyrus-sasl.spec && \
	$(replace-pathinfo) SPECS/cyrus-sasl.spec && \
	cp ../../../../src/cyrus-sasl-$(pvers).tar.gz SOURCES/zimbra-cyrus-sasl-$(pvers).tar.gz && \
	cp ../../../../patches/auxprop.patch SOURCES/ && \
	cp ../../../../patches/saslauthd-conf.patch SOURCES/ && \
	cp ../../../../patches/sasl-auth-zimbra-2.1.26.patch SOURCES/ && \
	$(PKG_BUILD) SPECS/cyrus-sasl.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
	$(replace-pkginfo) zimbra-cyrus-sasl/debian/changelog zimbra-cyrus-sasl/debian/zimbra-cyrus-sasl-lib.shlibs && \
	$(replace-pathinfo) zimbra-cyrus-sasl/debian/rules && \
	cp ../../src/cyrus-sasl-$(pvers).tar.gz zimbra-cyrus-sasl_$(pvers).orig.tar.gz && \
	cp ../../patches/auxprop.patch zimbra-cyrus-sasl/debian/patches && \
	cp ../../patches/saslauthd-conf.patch zimbra-cyrus-sasl/debian/patches && \
	cp ../../patches/sasl-auth-zimbra-2.1.26.patch zimbra-cyrus-sasl/debian/patches && \
	tar xfz zimbra-cyrus-sasl_$(pvers).orig.tar.gz --strip-components=1 -C zimbra-cyrus-sasl && \
	cd zimbra-cyrus-sasl && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
