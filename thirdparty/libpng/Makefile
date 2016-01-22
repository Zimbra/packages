PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(PNG_VERSION)

.PHONY: all getsrc setup build clean

all: clean getsrc build

files = $(wildcard src/libpng-$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q http://download.sourceforge.net/libpng/libpng-$(pvers).tar.gz \
	)
else
	@echo "Already have the source, skipping download"
endif

setup:
	$(generic-setup)

build: setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-libpng/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/libpng.spec && \
 	$(replace-pathinfo) SPECS/libpng.spec && \
	cp ../../../../src/libpng-$(pvers).tar.gz SOURCES/zimbra-libpng-$(pvers).tar.gz && \
 	$(PKG_BUILD) SPECS/libpng.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-libpng/debian/changelog zimbra-libpng/debian/zimbra-libpng-lib.shlibs && \
 	$(replace-pathinfo) zimbra-libpng/debian/rules && \
	cp ../../src/libpng-$(pvers).tar.gz zimbra-libpng_$(pvers).orig.tar.gz && \
	tar xfz zimbra-libpng_$(pvers).orig.tar.gz --strip-components=1 -C zimbra-libpng && \
	cd zimbra-libpng && \
	$(PKG_BUILD) \
	)
endif

clean:
	$(generic-clean)
