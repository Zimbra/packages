PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(NET_CIDR)

.PHONY: all getsrc setup build pkgadd pkgrm clean

all: clean getsrc build pkgrm1

files = $(wildcard src/Net-CIDR-$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q http://search.cpan.org/CPAN/authors/id/M/MR/MRSAM/Net-CIDR-$(pvers).tar.gz \
	)
else
	@echo "Already have the source, skipping download"
endif

pkgadd:
	$(PKG_EXTRACT) zimbra-perl-base

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base

setup:
	mkdir -p tmp/$(BUILD_PLATFORM)
	cp -prf zimbra-perl-net-cidr tmp/$(BUILD_PLATFORM)

build: setup pkgadd
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-perl-net-cidr/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/net-cidr.spec && \
 	$(replace-pathinfo) SPECS/net-cidr.spec && \
	cp ../../../../src/Net-CIDR-$(pvers).tar.gz SOURCES/zimbra-perl-net-cidr-$(pvers).tar.gz && \
 	$(PKG_BUILD) SPECS/net-cidr.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-perl-net-cidr/debian/changelog && \
 	$(replace-pathinfo) zimbra-perl-net-cidr/debian/rules && \
	cp ../../src/Net-CIDR-$(pvers).tar.gz zimbra-perl-net-cidr_$(pvers).orig.tar.gz && \
	tar xfz zimbra-perl-net-cidr_$(pvers).orig.tar.gz --strip-components=1  -C zimbra-perl-net-cidr && \
	cd zimbra-perl-net-cidr && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	rm -rf tmp/$(BUILD_PLATFORM)/zimbra-perl-net-cidr
	rm -f tmp/$(BUILD_PLATFORM)/zimbra-perl-net-cidr_*
