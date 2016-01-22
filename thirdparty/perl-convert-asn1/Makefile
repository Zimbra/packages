PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(CONVERT_ASN1)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/Convert-ASN1-$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q http://search.cpan.org/CPAN/authors/id/G/GB/GBARR/Convert-ASN1-$(pvers).tar.gz \
	)
else
	@echo "Already have the source, skipping download"
endif

pkgadd:
	$(PKG_EXTRACT) zimbra-perl-base zimbra-perl-math-bigint

pkgrm: pkgrm%

pkgrm%:
	$(PKG_PURGE) zimbra-base

setup:
	$(generic-setup)

build: setup pkgadd
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-perl-convert-asn1/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/convert-asn1.spec && \
 	$(replace-pathinfo) SPECS/convert-asn1.spec && \
	cp ../../../../src/Convert-ASN1-$(pvers).tar.gz SOURCES/zimbra-perl-convert-asn1-$(pvers).tar.gz && \
 	$(PKG_BUILD) SPECS/convert-asn1.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-perl-convert-asn1/debian/changelog && \
 	$(replace-pathinfo) zimbra-perl-convert-asn1/debian/rules && \
 	$(CHMOD) u+w zimbra-perl-convert-asn1/debian/control && \
	cp ../../src/Convert-ASN1-$(pvers).tar.gz zimbra-perl-convert-asn1_$(pvers).orig.tar.gz && \
	tar xfz zimbra-perl-convert-asn1_$(pvers).orig.tar.gz --strip-components=1  -C zimbra-perl-convert-asn1 && \
	cd zimbra-perl-convert-asn1 && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
