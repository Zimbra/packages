PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../package.def

pvers := $(ASPELL-DA_NORM)
dictver := $(ASPELL-DA_VERSION)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/aspell5-da-$(dictver).tar.bz2)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q ftp://ftp.gnu.org/gnu/aspell/dict/da/aspell5-da-$(dictver).tar.bz2 \
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
	cp -prf zimbra-aspell-da tmp/$(BUILD_PLATFORM)

build: pkgadd setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-aspell-da/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(replace-pkginfo) SPECS/aspell-da.spec && \
	$(replace-pathinfo) SPECS/aspell-da.spec && \
	$(replace-dictinfo) SPECS/aspell-da.spec && \
	cp ../../../../src/aspell5-da-$(dictver).tar.bz2 SOURCES/zimbra-aspell-da-$(pvers).tar.bz2 && \
	$(PKG_BUILD) SPECS/aspell-da.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
	$(replace-pkginfo) zimbra-aspell-da/debian/changelog && \
	$(replace-pathinfo) zimbra-aspell-da/debian/rules && \
	cp ../../src/aspell5-da-$(dictver).tar.bz2 zimbra-aspell-da_$(pvers).orig.tar.bz2 && \
	tar xfj zimbra-aspell-da_$(pvers).orig.tar.bz2 --strip-components=1 -C zimbra-aspell-da && \
	cd zimbra-aspell-da && \
	chmod u+w debian/control && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
