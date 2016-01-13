PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(XML_VERSION)

.PHONY: all getsrc setup build clean

all: clean getsrc build

files = $(wildcard src/libxml2-$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q ftp://xmlsoft.org/libxml2/libxml2-$(pvers).tar.gz \
	)
else
	@echo "Already have the source, skipping download"
endif

setup:
	$(generic-setup)

build: setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-libxml2/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(replace-pkginfo) SPECS/libxml2.spec && \
	$(replace-pathinfo) SPECS/libxml2.spec && \
	cp ../../../../src/libxml2-$(pvers).tar.gz SOURCES/zimbra-libxml2-$(pvers).tar.gz && \
	$(PKG_BUILD) SPECS/libxml2.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
	$(replace-pkginfo) zimbra-libxml2/debian/changelog zimbra-libxml2/debian/zimbra-libxml2-lib.shlibs && \
	$(replace-pathinfo) zimbra-libxml2/debian/rules && \
	cp ../../src/libxml2-$(pvers).tar.gz zimbra-libxml2_$(pvers).orig.tar.gz && \
	tar xfz zimbra-libxml2_$(pvers).orig.tar.gz --strip-components=1  -C zimbra-libxml2 && \
	cd zimbra-libxml2 && \
	$(PKG_BUILD) \
	)
endif

clean:
	$(generic-clean)
