PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../package.def

pvers := $(ASPELL-FR_NORM)
dictver := $(ASPELL-FR_VERSION)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/aspell-fr-$(dictver).tar.bz2)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q ftp://ftp.gnu.org/gnu/aspell/dict/fr/aspell-fr-$(dictver).tar.bz2 \
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
	cp -prf zimbra-aspell-fr tmp/$(BUILD_PLATFORM)

build: pkgadd setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-aspell-fr/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(replace-pkginfo) SPECS/aspell-fr.spec && \
	$(replace-pathinfo) SPECS/aspell-fr.spec && \
	$(replace-dictinfo) SPECS/aspell-fr.spec && \
	cp ../../../../src/aspell-fr-$(dictver).tar.bz2 SOURCES/zimbra-aspell-fr-$(pvers).tar.bz2 && \
	cp ../../../../patches/aspell-fr.patch SOURCES/aspell-fr.patch && \
	$(PKG_BUILD) SPECS/aspell-fr.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
	$(replace-pkginfo) zimbra-aspell-fr/debian/changelog && \
	$(replace-pathinfo) zimbra-aspell-fr/debian/rules && \
	cp ../../src/aspell-fr-$(dictver).tar.bz2 zimbra-aspell-fr_$(pvers).orig.tar.bz2 && \
	cp ../../patches/aspell-fr.patch zimbra-aspell-fr/debian/patches && \
	tar xfj zimbra-aspell-fr_$(pvers).orig.tar.bz2 --strip-components=1 -C zimbra-aspell-fr && \
	cd zimbra-aspell-fr && \
	chmod u+w debian/control && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
