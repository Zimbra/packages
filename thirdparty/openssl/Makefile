PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../package.def

pvers := $(OPENSSL_VERSION)
.PHONY: all getsrc setup build clean

all: clean getsrc build

files = $(wildcard src/openssl-$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q https://www.openssl.org/source/openssl-$(pvers).tar.gz \
	)
else
	@echo "Already have the source, skipping download"
endif

setup:
	$(generic-setup)

build: setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-openssl/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(replace-pkginfo) SPECS/openssl.spec && \
	$(replace-pathinfo) SPECS/openssl.spec && \
	cp ../../../../src/openssl-$(pvers).tar.gz SOURCES/zimbra-openssl-$(pvers).tar.gz && \
	cp -f ../../../../patches/ipv6.patch SOURCES/ && \
	$(PKG_BUILD) SPECS/openssl.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
	$(replace-pkginfo) zimbra-openssl/debian/changelog zimbra-openssl/debian/zimbra-openssl-lib.shlibs && \
	$(replace-pathinfo) zimbra-openssl/debian/rules && \
	cp ../../src/openssl-$(pvers).tar.gz ./zimbra-openssl_$(pvers).orig.tar.gz && \
	tar xfz zimbra-openssl_$(pvers).orig.tar.gz --strip-components=1 -C zimbra-openssl && \
	cd zimbra-openssl && \
	cp -f ../../../patches/ipv6.patch debian/patches/ && \
	$(PKG_BUILD) \
	)
endif

clean:
	$(generic-clean)
