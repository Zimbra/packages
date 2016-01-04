PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../package.def

pvers := $(MEMCACHED_VERSION)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/memcached-$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q http://www.memcached.org/files/memcached-$(pvers).tar.gz \
	)
else
	@echo "Already have the source, skipping download"
endif

pkgadd:
	$(PKG_EXTRACT) zimbra-base zimbra-libevent-$(PKG_DEV)

pkgrm: pkgrm%

pkgrm%:
	$(PKG_PURGE) zimbra-base

setup:
	mkdir -p tmp/$(BUILD_PLATFORM)
	cp -prf zimbra-memcached tmp/$(BUILD_PLATFORM)

build: pkgadd setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-memcached/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/memcached.spec && \
 	$(replace-pathinfo) SPECS/memcached.spec && \
	cp ../../../../src/memcached-$(pvers).tar.gz SOURCES/zimbra-memcached-$(pvers).tar.gz && \
 	$(PKG_BUILD) SPECS/memcached.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-memcached/debian/changelog && \
 	$(replace-pathinfo) zimbra-memcached/debian/rules && \
	cp ../../src/memcached-$(pvers).tar.gz zimbra-memcached_$(pvers).orig.tar.gz && \
	tar xfz zimbra-memcached_$(pvers).orig.tar.gz --strip-components=1 -C zimbra-memcached && \
	cd zimbra-memcached && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
