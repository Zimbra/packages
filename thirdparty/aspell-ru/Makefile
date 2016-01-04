PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../package.def

pvers := $(ASPELL-RU_NORM)
dictver := $(ASPELL-RU_VERSION)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/aspell6-ru-$(dictver).tar.bz2)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q ftp://ftp.gnu.org/gnu/aspell/dict/ru/aspell6-ru-$(dictver).tar.bz2 \
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
	cp -prf zimbra-aspell-ru tmp/$(BUILD_PLATFORM)

build: pkgadd setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-aspell-ru/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/aspell-ru.spec && \
 	$(replace-pathinfo) SPECS/aspell-ru.spec && \
 	$(replace-dictinfo) SPECS/aspell-ru.spec && \
	cp ../../../../src/aspell6-ru-$(dictver).tar.bz2 SOURCES/zimbra-aspell-ru-$(pvers).tar.bz2 && \
 	$(PKG_BUILD) SPECS/aspell-ru.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-aspell-ru/debian/changelog && \
 	$(replace-pathinfo) zimbra-aspell-ru/debian/rules && \
	cp ../../src/aspell6-ru-$(dictver).tar.bz2 zimbra-aspell-ru_$(pvers).orig.tar.bz2 && \
	tar xfj zimbra-aspell-ru_$(pvers).orig.tar.bz2 --strip-components=1 -C zimbra-aspell-ru && \
	cd zimbra-aspell-ru && \
	chmod u+w debian/control && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
