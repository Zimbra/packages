PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../package.def

pvers := $(ASPELL-IT_NORM)
dictver := $(ASPELL-IT_VERSION)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/aspell6-it-$(dictver).tar.bz2)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q ftp://ftp.gnu.org/gnu/aspell/dict/it/aspell6-it-$(dictver).tar.bz2 \
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
	cp -prf zimbra-aspell-it tmp/$(BUILD_PLATFORM)

build: pkgadd setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-aspell-it/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(replace-pkginfo) SPECS/aspell-it.spec && \
	$(replace-pathinfo) SPECS/aspell-it.spec && \
 	$(replace-dictinfo) SPECS/aspell-it.spec && \
	cp ../../../../src/aspell6-it-$(dictver).tar.bz2 SOURCES/zimbra-aspell-it-$(pvers).tar.bz2 && \
 	$(PKG_BUILD) SPECS/aspell-it.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-aspell-it/debian/changelog && \
 	$(replace-pathinfo) zimbra-aspell-it/debian/rules && \
	cp ../../src/aspell6-it-$(dictver).tar.bz2 zimbra-aspell-it_$(pvers).orig.tar.bz2 && \
	tar xfj zimbra-aspell-it_$(pvers).orig.tar.bz2 --strip-components=1 -C zimbra-aspell-it && \
	cd zimbra-aspell-it && \
	chmod u+w debian/control && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
