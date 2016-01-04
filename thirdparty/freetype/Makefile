PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../package.def

pvers := $(FREETYPE_VERSION)

.PHONY: all getsrc setup build clean

all: clean getsrc build

files = $(wildcard src/freetype-$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q http://download.savannah.gnu.org/releases/freetype/freetype-$(pvers).tar.gz \
	)
else
	@echo "Already have the source, skipping download"
endif

setup:
	mkdir -p tmp/$(BUILD_PLATFORM)
	cp -prf zimbra-freetype tmp/$(BUILD_PLATFORM)

build: setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-freetype/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/freetype.spec && \
 	$(replace-pathinfo) SPECS/freetype.spec && \
	cp ../../../../src/freetype-$(pvers).tar.gz SOURCES/zimbra-freetype-$(pvers).tar.gz && \
 	$(PKG_BUILD) SPECS/freetype.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-freetype/debian/changelog zimbra-freetype/debian/zimbra-freetype-lib.shlibs && \
 	$(replace-pathinfo) zimbra-freetype/debian/rules && \
	cp ../../src/freetype-$(pvers).tar.gz zimbra-freetype_$(pvers).orig.tar.gz && \
	tar xfz zimbra-freetype_$(pvers).orig.tar.gz --strip-components=1 -C zimbra-freetype && \
	cd zimbra-freetype && \
	$(PKG_BUILD) \
	)
endif

clean:
	$(generic-clean)
