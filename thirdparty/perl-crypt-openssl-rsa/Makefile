PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../package.def

pvers := $(CRYPT_OPENSSL_RSA)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/Crypt-OpenSSL-RSA-$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q http://search.cpan.org/CPAN/authors/id/P/PE/PERLER/Crypt-OpenSSL-RSA-$(pvers).tar.gz \
	)
else
	@echo "Already have the source, skipping download"
endif

pkgadd:
	$(PKG_EXTRACT) zimbra-perl-base zimbra-openssl-$(PKG_DEV)

pkgrm: pkgrm%

pkgrm%:
	$(PKG_PURGE) zimbra-base

setup:
	mkdir -p tmp/$(BUILD_PLATFORM)
	cp -prf zimbra-perl-crypt-openssl-rsa tmp/$(BUILD_PLATFORM)


build: setup pkgadd
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-perl-crypt-openssl-rsa/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/crypt-openssl-rsa.spec && \
 	$(replace-pathinfo) SPECS/crypt-openssl-rsa.spec && \
	cp ../../../../src/Crypt-OpenSSL-RSA-$(pvers).tar.gz SOURCES/zimbra-perl-crypt-openssl-rsa-$(pvers).tar.gz && \
 	$(PKG_BUILD) SPECS/crypt-openssl-rsa.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-perl-crypt-openssl-rsa/debian/changelog && \
 	$(replace-pathinfo) zimbra-perl-crypt-openssl-rsa/debian/rules && \
	cp ../../src/Crypt-OpenSSL-RSA-$(pvers).tar.gz zimbra-perl-crypt-openssl-rsa_$(pvers).orig.tar.gz && \
	tar xfz zimbra-perl-crypt-openssl-rsa_$(pvers).orig.tar.gz --strip-components=1  -C zimbra-perl-crypt-openssl-rsa && \
	cd zimbra-perl-crypt-openssl-rsa && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	rm -rf tmp/$(BUILD_PLATFORM)/zimbra-perl-crypt-openssl-rsa
	rm -f tmp/$(BUILD_PLATFORM)/zimbra-perl-crypt-openssl-rsa_*
