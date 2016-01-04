PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../package.def

pvers := $(BDB_VERSION)

.PHONY: all getsrc setup build clean

all: clean getsrc build

files = $(wildcard src/db-$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q http://ftp.nsysu.edu.tw/FreeBSD/ports/distfiles/bdb/db-$(pvers).tar.gz \
	)
else
	@echo "Already have the source, skipping download"
endif

setup:
	$(generic-setup)

build: setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-bdb/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/bdb.spec && \
 	$(replace-pathinfo) SPECS/bdb.spec && \
	cp ../../../../src/db-$(pvers).tar.gz SOURCES/zimbra-bdb-$(pvers).tar.gz && \
 	$(PKG_BUILD) SPECS/bdb.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-bdb/debian/changelog zimbra-bdb/debian/zimbra-bdb-lib.shlibs && \
 	$(replace-pathinfo) zimbra-bdb/debian/rules && \
	cp ../../src/db-$(pvers).tar.gz zimbra-bdb_$(pvers).orig.tar.gz && \
	tar xfz zimbra-bdb_$(pvers).orig.tar.gz --strip-components=1  -C zimbra-bdb && \
	cd zimbra-bdb && \
	$(PKG_BUILD) \
	)
endif

clean:
	$(generic-clean)
