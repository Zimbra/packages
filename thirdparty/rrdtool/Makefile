PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(RRDTOOL_VERSION)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/rrdtool-$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q https://oss.oetiker.ch/rrdtool/pub/rrdtool-$(pvers).tar.gz \
	)
else
	@echo "Already have the source, skipping download"
endif

pkgadd:
	$(PKG_EXTRACT) zimbra-base zimbra-libart-$(PKG_DEV) zimbra-libpng-$(PKG_DEV) \
	zimbra-freetype-$(PKG_DEV)

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base

setup:
	mkdir -p tmp/$(BUILD_PLATFORM)
	cp -prf zimbra-rrdtool tmp/$(BUILD_PLATFORM)

build: pkgadd setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-rrdtool/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/rrdtool.spec && \
 	$(replace-pathinfo) SPECS/rrdtool.spec && \
	cp ../../../../src/rrdtool-$(pvers).tar.gz SOURCES/zimbra-rrdtool-$(RRDTOOL_VERSION).tar.gz && \
 	$(PKG_BUILD) SPECS/rrdtool.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-rrdtool/debian/changelog zimbra-rrdtool/debian/zimbra-rrdtool-lib.shlibs && \
 	$(replace-pathinfo) zimbra-rrdtool/debian/rules && \
	cp ../../src/rrdtool-$(pvers).tar.gz zimbra-rrdtool_$(RRDTOOL_VERSION).orig.tar.gz && \
	tar xfz zimbra-rrdtool_$(pvers).orig.tar.gz --strip-components=1 -C zimbra-rrdtool && \
	cd zimbra-rrdtool && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
