PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../package.def

pvers := $(POSTFIX_VERSION)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/postfix-$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q ftp://postfix.cloud9.net/official/postfix-$(pvers).tar.gz \
	)
else
	@echo "Already have the source, skipping download"
endif

pkgadd:
	$(PKG_EXTRACT) zimbra-base zimbra-openssl-$(PKG_DEV) zimbra-mariadb-$(PKG_DEV) \
	zimbra-cyrus-sasl-$(PKG_DEV) zimbra-openldap-$(PKG_DEV) zimbra-lmdb-$(PKG_DEV)

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base

setup:
	$(generic-setup)

build: pkgadd setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-postfix/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/postfix.spec && \
 	$(replace-pathinfo) SPECS/postfix.spec && \
	cp ../../../../src/postfix-$(pvers).tar.gz SOURCES/zimbra-postfix-$(pvers).tar.gz && \
	cp ../../../../patches/lmdb-default.patch SOURCES/ && \
	cp ../../../../patches/postfix-ldap.patch SOURCES/ && \
	cp ../../../../patches/postfix-main-cf-zimbra.patch SOURCES/ && \
	cp ../../../../patches/stop-warning.patch SOURCES/ && \
	cp ../../../../patches/pass-ip-address.patch SOURCES/ && \
 	$(PKG_BUILD) SPECS/postfix.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-postfix/debian/changelog && \
 	$(replace-pathinfo) zimbra-postfix/debian/rules && \
	cp ../../src/postfix-$(pvers).tar.gz zimbra-postfix_$(pvers).orig.tar.gz && \
	tar xfz zimbra-postfix_$(pvers).orig.tar.gz --strip-components=1 -C zimbra-postfix && \
	cp ../../patches/lmdb-default.patch zimbra-postfix/debian/patches && \
	cp ../../patches/postfix-ldap.patch zimbra-postfix/debian/patches && \
	cp ../../patches/postfix-main-cf-zimbra.patch zimbra-postfix/debian/patches && \
	cp ../../patches/stop-warning.patch zimbra-postfix/debian/patches && \
	cp ../../patches/pass-ip-address.patch zimbra-postfix/debian/patches && \
	cd zimbra-postfix && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
