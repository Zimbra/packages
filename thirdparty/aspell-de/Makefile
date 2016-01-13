PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(ASPELL-DE_NORM)
dictver := $(ASPELL-DE_VERSION)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/aspell6-de-$(dictver).tar.bz2)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q ftp://ftp.gnu.org/gnu/aspell/dict/de/aspell6-de-$(dictver).tar.bz2 \
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
	cp -prf zimbra-aspell-de tmp/$(BUILD_PLATFORM)

build: pkgadd setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-aspell-de/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(replace-pkginfo) SPECS/aspell-de.spec && \
	$(replace-pathinfo) SPECS/aspell-de.spec && \
	$(replace-dictinfo) SPECS/aspell-de.spec && \
	cp ../../../../src/aspell6-de-$(dictver).tar.bz2 SOURCES/zimbra-aspell-de-$(pvers).tar.bz2 && \
	$(PKG_BUILD) SPECS/aspell-de.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
	$(replace-pkginfo) zimbra-aspell-de/debian/changelog && \
	$(replace-pathinfo) zimbra-aspell-de/debian/rules && \
	cp ../../src/aspell6-de-$(dictver).tar.bz2 zimbra-aspell-de_$(pvers).orig.tar.bz2 && \
	tar xfj zimbra-aspell-de_$(pvers).orig.tar.bz2 --strip-components=1 -C zimbra-aspell-de && \
	cd zimbra-aspell-de && \
	chmod u+w debian/control && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
