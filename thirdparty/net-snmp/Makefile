PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../package.def

pvers := $(SNMP_VERSION)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/net-snmp-$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q http://iweb.dl.sourceforge.net/project/net-snmp/net-snmp/$(pvers)/net-snmp-$(pvers).tar.gz \
	)
else
	@echo "Already have the source, skipping download"
endif

pkgadd:
	$(PKG_EXTRACT) zimbra-base zimbra-openssl-$(PKG_DEV)

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base

setup:
	$(generic-setup)

build: pkgadd setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-net-snmp/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/net-snmp.spec && \
 	$(replace-pathinfo) SPECS/net-snmp.spec && \
	cp ../../../../src/net-snmp-$(pvers).tar.gz SOURCES/zimbra-net-snmp-$(pvers).tar.gz && \
 	$(PKG_BUILD) SPECS/net-snmp.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-net-snmp/debian/changelog zimbra-net-snmp/debian/zimbra-net-snmp-lib.shlibs && \
 	$(replace-pathinfo) zimbra-net-snmp/debian/rules && \
	cp ../../src/net-snmp-$(pvers).tar.gz zimbra-net-snmp_$(pvers).orig.tar.gz && \
	tar xfz zimbra-net-snmp_$(pvers).orig.tar.gz --strip-components=1 -C zimbra-net-snmp && \
	cd zimbra-net-snmp && \
	$(CHMOD) u+w debian/control && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
