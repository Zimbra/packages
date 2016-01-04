PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../package.def

pvers := $(ASPELL-SV_NORM)
dictver := $(ASPELL-SV_VERSION)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/aspell-sv-$(dictver).tar.bz2)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q ftp://ftp.gnu.org/gnu/aspell/dict/sv/aspell-sv-$(dictver).tar.bz2 \
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
	cp -prf zimbra-aspell-sv tmp/$(BUILD_PLATFORM)

build: pkgadd setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-aspell-sv/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/aspell-sv.spec && \
 	$(replace-pathinfo) SPECS/aspell-sv.spec && \
 	$(replace-dictinfo) SPECS/aspell-sv.spec && \
	cp ../../../../src/aspell-sv-$(dictver).tar.bz2 SOURCES/zimbra-aspell-sv-$(pvers).tar.bz2 && \
 	$(PKG_BUILD) SPECS/aspell-sv.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-aspell-sv/debian/changelog && \
 	$(replace-pathinfo) zimbra-aspell-sv/debian/rules && \
	cp ../../src/aspell-sv-$(dictver).tar.bz2 zimbra-aspell-sv_$(pvers).orig.tar.bz2 && \
	tar xfj zimbra-aspell-sv_$(pvers).orig.tar.bz2 --strip-components=1 -C zimbra-aspell-sv && \
	cd zimbra-aspell-sv && \
	chmod u+w debian/control && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
