PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(ASPELL-NL_NORM)
dictver := $(ASPELL-NL_VERSION)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/aspell-nl-$(dictver).tar.bz2)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q ftp://ftp.gnu.org/gnu/aspell/dict/nl/aspell-nl-$(dictver).tar.bz2 \
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
	cp -prf zimbra-aspell-nl tmp/$(BUILD_PLATFORM)

build: pkgadd setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-aspell-nl/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/aspell-nl.spec && \
 	$(replace-pathinfo) SPECS/aspell-nl.spec && \
 	$(replace-dictinfo) SPECS/aspell-nl.spec && \
	cp ../../../../src/aspell-nl-$(dictver).tar.bz2 SOURCES/zimbra-aspell-nl-$(pvers).tar.bz2 && \
	cp ../../../../patches/aspell-nl.patch SOURCES/aspell-nl.patch && \
 	$(PKG_BUILD) SPECS/aspell-nl.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-aspell-nl/debian/changelog && \
 	$(replace-pathinfo) zimbra-aspell-nl/debian/rules && \
	cp ../../src/aspell-nl-$(dictver).tar.bz2 zimbra-aspell-nl_$(pvers).orig.tar.bz2 && \
	cp ../../patches/aspell-nl.patch zimbra-aspell-nl/debian/patches && \
	tar xfj zimbra-aspell-nl_$(pvers).orig.tar.bz2 --strip-components=1 -C zimbra-aspell-nl && \
	cd zimbra-aspell-nl && \
	chmod u+w debian/control && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
