PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

.PHONY: all getsrc setup build clean pkgadd pkgrm

pvers := $(MARIADB_VERSION)

all: clean getsrc build pkgrm1

files = $(wildcard src/mariadb-$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q https://downloads.mariadb.org/f/mariadb-$(pvers)/source/mariadb-$(pvers).tar.gz \
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
	(cd tmp/$(BUILD_PLATFORM)/zimbra-mariadb/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(replace-pkginfo) SPECS/mariadb.spec && \
	$(replace-pathinfo) SPECS/mariadb.spec && \
	cp ../../../../src/mariadb-$(pvers).tar.gz SOURCES/zimbra-mariadb-$(pvers).tar.gz && \
	$(PKG_BUILD) SPECS/mariadb.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
	$(replace-pkginfo) zimbra-mariadb/debian/changelog zimbra-mariadb/debian/zimbra-mariadb-lib.shlibs && \
	$(replace-pathinfo) zimbra-mariadb/debian/rules && \
	cp ../../src/mariadb-$(pvers).tar.gz zimbra-mariadb_$(pvers).orig.tar.gz && \
	tar xfz zimbra-mariadb_$(pvers).orig.tar.gz --strip-components=1  --exclude=debian -C zimbra-mariadb && \
	cd zimbra-mariadb && \
	dpkg-buildpackage -irpm \
	)
endif

clean: pkgrm
	$(generic-clean)
