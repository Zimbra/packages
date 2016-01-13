PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(SODIUM_VERSION)

.PHONY: all getsrc setup build clean

all: clean getsrc build

files = $(wildcard src/libsodium-$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q https://download.libsodium.org/libsodium/releases/libsodium-$(pvers).tar.gz \
	)
else
	@echo "Already have the source, skipping download"
endif

setup:
	mkdir -p tmp/$(BUILD_PLATFORM)
	cp -prf zimbra-libsodium tmp/$(BUILD_PLATFORM)

build: setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-libsodium/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/libsodium.spec && \
 	$(replace-pathinfo) SPECS/libsodium.spec && \
	cp ../../../../src/libsodium-$(pvers).tar.gz SOURCES/zimbra-libsodium-$(pvers).tar.gz && \
 	$(PKG_BUILD) SPECS/libsodium.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-libsodium/debian/changelog zimbra-libsodium/debian/zimbra-libsodium-lib.shlibs && \
 	$(replace-pathinfo) zimbra-libsodium/debian/rules && \
	cp ../../src/libsodium-$(pvers).tar.gz zimbra-libsodium_$(pvers).orig.tar.gz && \
	tar xfz zimbra-libsodium_$(pvers).orig.tar.gz --strip-components=1  -C zimbra-libsodium && \
	cd zimbra-libsodium && \
	$(PKG_BUILD) \
	)
endif

clean:
	$(generic-clean)
