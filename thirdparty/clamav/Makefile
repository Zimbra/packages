PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../package.def

pvers := $(CLAMAV_VERSION)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/clamav-$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q http://www.clamav.net/downloads/production/clamav-$(pvers).tar.gz \
	)
else
	@echo "Already have the source, skipping download"
endif

pkgadd:
	$(PKG_EXTRACT) zimbra-base zimbra-openssl-$(PKG_DEV) zimbra-libxml2-$(PKG_DEV) \
	zimbra-libmilter-$(PKG_DEV)

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base

setup:
	$(generic-setup)

build: pkgadd setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-clamav/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/clamav.spec && \
 	$(replace-pathinfo) SPECS/clamav.spec && \
	cp ../../../../src/clamav-$(pvers).tar.gz SOURCES/zimbra-clamav-$(pvers).tar.gz && \
 	$(PKG_BUILD) SPECS/clamav.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-clamav/debian/changelog zimbra-clamav/debian/zimbra-clamav-lib.shlibs && \
 	$(replace-pathinfo) zimbra-clamav/debian/rules && \
	cp ../../src/clamav-$(pvers).tar.gz zimbra-clamav_$(pvers).orig.tar.gz && \
	tar xfz zimbra-clamav_$(pvers).orig.tar.gz --strip-components=1 -C zimbra-clamav && \
	cd zimbra-clamav && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
