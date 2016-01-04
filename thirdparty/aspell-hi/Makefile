PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../package.def

pvers := $(ASPELL-HI_NORM)
dictver := $(ASPELL-HI_VERSION)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/aspell6-hi-$(dictver).tar.bz2)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q ftp://ftp.gnu.org/gnu/aspell/dict/hi/aspell6-hi-$(dictver).tar.bz2 \
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
	cp -prf zimbra-aspell-hi tmp/$(BUILD_PLATFORM)

build: pkgadd setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-aspell-hi/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(replace-pkginfo) SPECS/aspell-hi.spec && \
	$(replace-pathinfo) SPECS/aspell-hi.spec && \
	$(replace-dictinfo) SPECS/aspell-hi.spec && \
	cp ../../../../src/aspell6-hi-$(dictver).tar.bz2 SOURCES/zimbra-aspell-hi-$(pvers).tar.bz2 && \
	$(PKG_BUILD) SPECS/aspell-hi.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
	$(replace-pkginfo) zimbra-aspell-hi/debian/changelog && \
	$(replace-pathinfo) zimbra-aspell-hi/debian/rules && \
	cp ../../src/aspell6-hi-$(dictver).tar.bz2 zimbra-aspell-hi_$(pvers).orig.tar.bz2 && \
	tar xfj zimbra-aspell-hi_$(pvers).orig.tar.bz2 --strip-components=1 -C zimbra-aspell-hi && \
	cd zimbra-aspell-hi && \
	chmod u+w debian/control && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
