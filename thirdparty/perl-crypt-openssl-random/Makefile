PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(CRYPT_OPENSSL_RANDOM)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/Crypt-OpenSSL-Random-$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q http://search.cpan.org/CPAN/authors/id/R/RU/RURBAN/Crypt-OpenSSL-Random-$(pvers).tar.gz \
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
	$(generic-setup)


build: setup pkgadd
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-perl-crypt-openssl-random/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/crypt-openssl-random.spec && \
 	$(replace-pathinfo) SPECS/crypt-openssl-random.spec && \
	cp ../../../../src/Crypt-OpenSSL-Random-$(pvers).tar.gz SOURCES/zimbra-perl-crypt-openssl-random-$(pvers).tar.gz && \
 	$(PKG_BUILD) SPECS/crypt-openssl-random.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-perl-crypt-openssl-random/debian/changelog && \
 	$(replace-pathinfo) zimbra-perl-crypt-openssl-random/debian/rules && \
	cp ../../src/Crypt-OpenSSL-Random-$(pvers).tar.gz zimbra-perl-crypt-openssl-random_$(pvers).orig.tar.gz && \
	tar xfz zimbra-perl-crypt-openssl-random_$(pvers).orig.tar.gz --strip-components=1  -C zimbra-perl-crypt-openssl-random && \
	cd zimbra-perl-crypt-openssl-random && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
