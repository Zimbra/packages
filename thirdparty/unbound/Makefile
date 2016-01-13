PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(UNBOUND_VERSION)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/unbound-$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q https://www.unbound.net/downloads/unbound-$(pvers).tar.gz \
	)
else
	@echo "Already have the source, skipping download"
endif

pkgadd:
	$(PKG_EXTRACT) zimbra-base zimbra-openssl-$(PKG_DEV)

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base

setup:
	$(generic-setup)

build: pkgadd setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-unbound/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/unbound.spec && \
 	$(replace-pathinfo) SPECS/unbound.spec && \
	cp ../../../../src/unbound-$(pvers).tar.gz SOURCES/zimbra-unbound-$(pvers).tar.gz && \
	cp ../../../../patches/*.patch SOURCES/ && \
 	$(PKG_BUILD) SPECS/unbound.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-unbound/debian/changelog zimbra-unbound/debian/zimbra-unbound-lib.shlibs && \
 	$(replace-pathinfo) zimbra-unbound/debian/rules && \
	cp ../../src/unbound-$(pvers).tar.gz zimbra-unbound_$(pvers).orig.tar.gz && \
	cp ../../patches/*.patch zimbra-unbound/debian/patches && \
	tar xfz zimbra-unbound_$(pvers).orig.tar.gz --strip-components=1  -C zimbra-unbound && \
	cd zimbra-unbound && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
