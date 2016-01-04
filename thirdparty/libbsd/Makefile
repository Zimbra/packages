PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../package.def

pvers := $(BSD_VERSION)

.PHONY: all getsrc setup build clean

all: clean getsrc build

files = $(wildcard src/libbsd-$(pvers).tar.xz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q http://libbsd.freedesktop.org/releases/libbsd-$(pvers).tar.xz \
	)
else
	@echo "Already have the source, skipping download"
endif

setup:
	$(generic-setup)

build: setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-libbsd/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/libbsd.spec && \
 	$(replace-pathinfo) SPECS/libbsd.spec && \
	cp ../../../../src/libbsd-$(pvers).tar.xz SOURCES/zimbra-libbsd-$(pvers).tar.xz && \
 	$(PKG_BUILD) SPECS/libbsd.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-libbsd/debian/changelog zimbra-libbsd/debian/zimbra-libbsd-lib.shlibs && \
 	$(replace-pathinfo) zimbra-libbsd/debian/rules && \
	cp ../../src/libbsd-$(pvers).tar.xz zimbra-libbsd_$(pvers).orig.tar.xz && \
	tar xf zimbra-libbsd_$(pvers).orig.tar.xz --strip-components=1 -C zimbra-libbsd && \
	cd zimbra-libbsd && \
	$(PKG_BUILD) \
	)
endif

clean:
	$(generic-clean)
