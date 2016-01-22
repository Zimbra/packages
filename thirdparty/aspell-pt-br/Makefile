PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(ASPELL-PT-BR_NORM)
dictver := $(ASPELL-PT-BR_VERSION)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/aspell6-pt_BR-$(dictver).tar.bz2)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q ftp://ftp.gnu.org/gnu/aspell/dict/pt_BR/aspell6-pt_BR-$(dictver).tar.bz2 \
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
	(cd tmp/$(BUILD_PLATFORM)/zimbra-aspell-pt-br/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/aspell-pt-br.spec && \
 	$(replace-pathinfo) SPECS/aspell-pt-br.spec && \
 	$(replace-dictinfo) SPECS/aspell-pt-br.spec && \
	cp ../../../../src/aspell6-pt_BR-$(dictver).tar.bz2 SOURCES/zimbra-aspell-pt-br-$(pvers).tar.bz2 && \
 	$(PKG_BUILD) SPECS/aspell-pt-br.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-aspell-pt-br/debian/changelog && \
 	$(replace-pathinfo) zimbra-aspell-pt-br/debian/rules && \
	cp ../../src/aspell6-pt_BR-$(dictver).tar.bz2 zimbra-aspell-pt-br_$(pvers).orig.tar.bz2 && \
	tar xfj zimbra-aspell-pt-br_$(pvers).orig.tar.bz2 --strip-components=1 -C zimbra-aspell-pt-br && \
	cd zimbra-aspell-pt-br && \
	chmod u+w debian/control && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
