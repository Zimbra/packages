PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(ASPELL_VERSION)

.PHONY: all getsrc setup build clean

all: clean getsrc build

files = $(wildcard src/aspell-$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q ftp://ftp.gnu.org/gnu/aspell/aspell-$(pvers).tar.gz \
	)
else
	@echo "Already have the source, skipping download"
endif

setup:
	$(generic-setup)

build: setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-aspell/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(replace-pkginfo) SPECS/aspell.spec && \
	$(replace-pathinfo) SPECS/aspell.spec && \
	cp ../../../../src/aspell-$(pvers).tar.gz SOURCES/zimbra-aspell-$(pvers).tar.gz && \
	$(PKG_BUILD) SPECS/aspell.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
	$(replace-pkginfo) zimbra-aspell/debian/changelog zimbra-aspell/debian/zimbra-aspell-lib.shlibs && \
	$(replace-pathinfo) zimbra-aspell/debian/rules && \
	cp ../../src/aspell-$(pvers).tar.gz zimbra-aspell_$(pvers).orig.tar.gz && \
	tar xfz zimbra-aspell_$(pvers).orig.tar.gz --strip-components=1 -C zimbra-aspell && \
	cd zimbra-aspell && \
	$(PKG_BUILD) \
	)
endif

clean:
	$(generic-clean)
