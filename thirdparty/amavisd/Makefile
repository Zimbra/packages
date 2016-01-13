PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(AMAVISD_VERSION)

.PHONY: all getsrc setup build clean

all: clean getsrc build

files = $(wildcard src/amavisd-new-$(pvers).tar.bz2)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q http://www.ijs.si/software/amavisd/amavisd-new-$(pvers).tar.bz2 \
	)
else
	@echo "Already have the source, skipping download"
endif

setup:
	$(generic-setup)

build: setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-amavisd/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/amavisd.spec && \
 	$(replace-pathinfo) SPECS/amavisd.spec && \
	cp ../../../../src/amavisd-new-$(pvers).tar.bz2 SOURCES/zimbra-amavisd-$(pvers).tar.bz2 && \
	cp ../../../../patches/*.patch SOURCES/ && \
 	$(PKG_BUILD) SPECS/amavisd.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-amavisd/debian/changelog && \
 	$(replace-pathinfo) zimbra-amavisd/debian/rules && \
	cp ../../src/amavisd-new-$(pvers).tar.bz2 zimbra-amavisd_$(pvers).orig.tar.bz2 && \
	cp ../../patches/*.patch zimbra-amavisd/debian/patches/ && \
	tar xfj zimbra-amavisd_$(pvers).orig.tar.bz2 --strip-components=1  -C zimbra-amavisd && \
	cd zimbra-amavisd && \
	$(PKG_BUILD) \
	)
endif

clean:
	$(generic-clean)
