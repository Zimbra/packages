PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(ASPELL-AR_NORM)
dictver := $(ASPELL-AR_VERSION)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/aspell6-ar-$(dictver).tar.bz2)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q ftp://ftp.gnu.org/gnu/aspell/dict/ar/aspell6-ar-$(dictver).tar.bz2 \
	)
else
	@echo "Already have the source, skipping download"
endif

pkgadd:
	$(PKG_EXTRACT) zimbra-aspell

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base

setup:
	mkdir -p tmp/$(BUILD_PLATFORM)
	cp -prf zimbra-aspell-ar tmp/$(BUILD_PLATFORM)

build: pkgadd setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-aspell-ar/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(replace-pkginfo) SPECS/aspell-ar.spec && \
	$(replace-pathinfo) SPECS/aspell-ar.spec && \
	$(replace-dictinfo) SPECS/aspell-ar.spec && \
	cp ../../../../src/aspell6-ar-$(dictver).tar.bz2 SOURCES/zimbra-aspell-ar-$(pvers).tar.bz2 && \
	$(PKG_BUILD) SPECS/aspell-ar.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
	$(replace-pkginfo) zimbra-aspell-ar/debian/changelog && \
	$(replace-pathinfo) zimbra-aspell-ar/debian/rules && \
	cp ../../src/aspell6-ar-$(dictver).tar.bz2 zimbra-aspell-ar_$(pvers).orig.tar.bz2 && \
	tar xfj zimbra-aspell-ar_$(pvers).orig.tar.bz2 --strip-components=1 -C zimbra-aspell-ar && \
	cd zimbra-aspell-ar && \
	chmod u+w debian/control && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
