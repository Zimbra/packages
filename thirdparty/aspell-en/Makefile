PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(ASPELL-EN_NORM)
dictver := $(ASPELL-EN_VERSION)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/aspell6-en-$(dictver).tar.bz2)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q ftp://ftp.gnu.org/gnu/aspell/dict/en/aspell6-en-$(dictver).tar.bz2 \
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
	cp -prf zimbra-aspell-en tmp/$(BUILD_PLATFORM)

build: pkgadd setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-aspell-en/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(replace-pkginfo) SPECS/aspell-en.spec && \
	$(replace-pathinfo) SPECS/aspell-en.spec && \
	$(replace-dictinfo) SPECS/aspell-en.spec && \
	cp ../../../../src/aspell6-en-$(dictver).tar.bz2 SOURCES/zimbra-aspell-en-$(pvers).tar.bz2 && \
	$(PKG_BUILD) SPECS/aspell-en.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
	$(replace-pkginfo) zimbra-aspell-en/debian/changelog && \
	$(replace-pathinfo) zimbra-aspell-en/debian/rules && \
	cp ../../src/aspell6-en-$(dictver).tar.bz2 zimbra-aspell-en_$(pvers).orig.tar.bz2 && \
	tar xfj zimbra-aspell-en_$(pvers).orig.tar.bz2 --strip-components=1 -C zimbra-aspell-en && \
	cd zimbra-aspell-en && \
	chmod u+w debian/control && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
