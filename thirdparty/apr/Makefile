PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../package.def

pvers := $(APR_VERSION)

.PHONY: all getsrc setup build clean

all: clean getsrc build

files = $(wildcard src/apr-$(pvers).tar.bz2)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q https://archive.apache.org/dist/apr/apr-$(pvers).tar.bz2 \
	)
else
	@echo "Already have the source, skipping download"
endif

setup:
	mkdir -p tmp/$(BUILD_PLATFORM)
	cp -prf zimbra-apr tmp/$(BUILD_PLATFORM)

build: setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-apr/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/apr.spec && \
 	$(replace-pathinfo) SPECS/apr.spec && \
	cp ../../../../src/apr-$(pvers).tar.bz2 SOURCES/zimbra-apr-$(pvers).tar.bz2 && \
 	$(PKG_BUILD) SPECS/apr.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-apr/debian/changelog zimbra-apr/debian/zimbra-apr-lib.shlibs && \
 	$(replace-pathinfo) zimbra-apr/debian/rules && \
	cp ../../src/apr-$(pvers).tar.bz2 zimbra-apr_$(pvers).orig.tar.bz2 && \
	tar xfj zimbra-apr_$(pvers).orig.tar.bz2 --strip-components=1 -C zimbra-apr && \
	cd zimbra-apr && \
	$(PKG_BUILD) \
	)
endif

clean:
	$(generic-clean)
