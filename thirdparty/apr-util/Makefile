PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(APR_UTIL_VERSION)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/apr-util-$(pvers).tar.bz2)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q https://archive.apache.org/dist/apr/apr-util-$(pvers).tar.bz2 \
	)
else
	@echo "Already have the source, skipping download"
endif

pkgadd:
	$(PKG_EXTRACT) zimbra-base zimbra-openssl-$(PKG_DEV) zimbra-apr-$(PKG_DEV)

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base

setup:
	mkdir -p tmp/$(BUILD_PLATFORM)
	cp -prf zimbra-apr-util tmp/$(BUILD_PLATFORM)

build: pkgadd setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-apr-util/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/apr-util.spec && \
 	$(replace-pathinfo) SPECS/apr-util.spec && \
	cp ../../../../src/apr-util-$(pvers).tar.bz2 SOURCES/zimbra-apr-util-$(pvers).tar.bz2 && \
 	$(PKG_BUILD) SPECS/apr-util.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-apr-util/debian/changelog zimbra-apr-util/debian/zimbra-apr-util-lib.shlibs && \
 	$(replace-pathinfo) zimbra-apr-util/debian/rules && \
	cp ../../src/apr-util-$(pvers).tar.bz2 zimbra-apr-util_$(pvers).orig.tar.bz2 && \
	tar xfj zimbra-apr-util_$(pvers).orig.tar.bz2 --strip-components=1 -C zimbra-apr-util && \
	cd zimbra-apr-util && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
