PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(HEIMDAL_VERSION)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/heimdal-$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q http://www.h5l.org/dist/src/heimdal-$(pvers).tar.gz \
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
	(cd tmp/$(BUILD_PLATFORM)/zimbra-heimdal/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(replace-pkginfo) SPECS/heimdal.spec && \
	$(replace-pathinfo) SPECS/heimdal.spec && \
	cp ../../../../src/heimdal-$(pvers).tar.gz SOURCES/zimbra-heimdal-$(pvers).tar.gz && \
	$(PKG_BUILD) SPECS/heimdal.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
	$(replace-pkginfo) zimbra-heimdal/debian/changelog zimbra-heimdal/debian/zimbra-heimdal-lib.shlibs && \
	$(replace-pathinfo) zimbra-heimdal/debian/rules && \
	cp ../../src/heimdal-$(pvers).tar.gz zimbra-heimdal_$(pvers).orig.tar.gz && \
	tar xfz zimbra-heimdal_$(pvers).orig.tar.gz --strip-components=1  -C zimbra-heimdal && \
	cd zimbra-heimdal && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
