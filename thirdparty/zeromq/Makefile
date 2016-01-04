PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../package.def

pvers := $(ZMQ_VERSION)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/zeromq-$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q http://download.zeromq.org/zeromq-$(pvers).tar.gz \
	)
else
	@echo "Already have the source, skipping download"
endif

pkgadd:
	$(PKG_EXTRACT) zimbra-base zimbra-libsodium-$(PKG_DEV)

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base

setup:
	mkdir -p tmp/$(BUILD_PLATFORM)
	cp -prf zimbra-zeromq tmp/$(BUILD_PLATFORM)

build: pkgadd setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-zeromq/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/zeromq.spec && \
 	$(replace-pathinfo) SPECS/zeromq.spec && \
	$(CP) $(PKG_ROOT)/patches/sodium-init.patch SOURCES/ && \
	cp ../../../../src/zeromq-$(pvers).tar.gz SOURCES/zimbra-zeromq-$(pvers).tar.gz && \
	$(PKG_BUILD) SPECS/zeromq.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-zeromq/debian/changelog zimbra-zeromq/debian/zimbra-zeromq-lib.shlibs && \
 	$(replace-pathinfo) zimbra-zeromq/debian/rules && \
	cp ../../src/zeromq-$(pvers).tar.gz zimbra-zeromq_$(pvers).orig.tar.gz && \
	tar xfz zimbra-zeromq_$(pvers).orig.tar.gz --strip-components=1  -C zimbra-zeromq && \
	cd zimbra-zeromq && \
	$(CP) $(PKG_ROOT)/patches/sodium-init.patch debian/patches && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
