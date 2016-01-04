PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../package.def

pvers := $(ASPELL-PL_NORM)
dictver := $(ASPELL-PL_VERSION)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/aspell6-pl-$(dictver).tar.bz2)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q ftp://ftp.gnu.org/gnu/aspell/dict/pl/aspell6-pl-$(dictver).tar.bz2 \
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
	cp -prf zimbra-aspell-pl tmp/$(BUILD_PLATFORM)

build: pkgadd setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-aspell-pl/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/aspell-pl.spec && \
 	$(replace-pathinfo) SPECS/aspell-pl.spec && \
 	$(replace-dictinfo) SPECS/aspell-pl.spec && \
	cp ../../../../src/aspell6-pl-$(dictver).tar.bz2 SOURCES/zimbra-aspell-pl-$(pvers).tar.bz2 && \
 	$(PKG_BUILD) SPECS/aspell-pl.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-aspell-pl/debian/changelog && \
 	$(replace-pathinfo) zimbra-aspell-pl/debian/rules && \
	cp ../../src/aspell6-pl-$(dictver).tar.bz2 zimbra-aspell-pl_$(pvers).orig.tar.bz2 && \
	tar xfj zimbra-aspell-pl_$(pvers).orig.tar.bz2 --strip-components=1 -C zimbra-aspell-pl && \
	cd zimbra-aspell-pl && \
	chmod u+w debian/control && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
