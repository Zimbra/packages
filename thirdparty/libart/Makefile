PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../package.def

pvers := $(LIBART_VERSION)

.PHONY: all getsrc setup build clean

all: clean getsrc build

files = $(wildcard src/libart_lgpl-$(pvers).tar.bz2)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q http://ftp.gnome.org/pub/gnome/sources/libart_lgpl/2.3/libart_lgpl-$(pvers).tar.bz2 \
	)
else
	@echo "Already have the source, skipping download"
endif

setup:
	mkdir -p tmp/$(BUILD_PLATFORM)
	cp -prf zimbra-libart tmp/$(BUILD_PLATFORM)

build: setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-libart/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/libart.spec && \
 	$(replace-pathinfo) SPECS/libart.spec && \
	cp ../../../../src/libart_lgpl-$(pvers).tar.bz2 SOURCES/zimbra-libart-$(pvers).tar.bz2 && \
 	$(PKG_BUILD) SPECS/libart.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
	$(replace-pkginfo) zimbra-libart/debian/changelog zimbra-libart/debian/zimbra-libart-lib.shlibs && \
 	$(replace-pathinfo) zimbra-libart/debian/rules && \
	cp ../../src/libart_lgpl-$(pvers).tar.bz2 zimbra-libart_$(pvers).orig.tar.bz2 && \
	tar xfj zimbra-libart_$(pvers).orig.tar.bz2 --strip-components=1 -C zimbra-libart && \
	cd zimbra-libart && \
	$(PKG_BUILD) \
	)
endif

clean:
	$(generic-clean)
