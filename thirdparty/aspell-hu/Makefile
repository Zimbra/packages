PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(ASPELL-HU_NORM)
dictver := $(ASPELL-HU_VERSION)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/aspell6-hu-$(dictver).tar.bz2)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q ftp://ftp.gnu.org/gnu/aspell/dict/hu/aspell6-hu-$(dictver).tar.bz2 \
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
	$(generic-setup)

build: pkgadd setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-aspell-hu/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(replace-pkginfo) SPECS/aspell-hu.spec && \
	$(replace-pathinfo) SPECS/aspell-hu.spec && \
	$(replace-dictinfo) SPECS/aspell-hu.spec && \
	cp ../../../../src/aspell6-hu-$(dictver).tar.bz2 SOURCES/zimbra-aspell-hu-$(pvers).tar.bz2 && \
	$(PKG_BUILD) SPECS/aspell-hu.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
	$(replace-pkginfo) zimbra-aspell-hu/debian/changelog && \
	$(replace-pathinfo) zimbra-aspell-hu/debian/rules && \
	cp ../../src/aspell6-hu-$(dictver).tar.bz2 zimbra-aspell-hu_$(pvers).orig.tar.bz2 && \
	tar xfj zimbra-aspell-hu_$(pvers).orig.tar.bz2 --strip-components=1 -C zimbra-aspell-hu && \
	cd zimbra-aspell-hu && \
	chmod u+w debian/control && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
