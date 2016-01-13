PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(LDAP_VERSION)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/openldap-$(pvers).tgz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q ftp://ftp.openldap.org/pub/OpenLDAP/openldap-release/openldap-$(pvers).tgz \
	)
else
	@echo "Already have the source, skipping download"
endif

pkgadd:
	$(PKG_EXTRACT) zimbra-base zimbra-openssl-$(PKG_DEV) zimbra-cyrus-sasl-$(PKG_DEV) \
	zimbra-libltdl-$(PKG_DEV)

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base

setup:
	$(generic-setup)

build: pkgadd setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-openldap/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(replace-pkginfo) SPECS/openldap.spec && \
	$(replace-pathinfo) SPECS/openldap.spec && \
	cp ../../../../src/openldap-$(pvers).tgz SOURCES/zimbra-openldap-$(pvers).tgz && \
	cp ../../../../patches/ITS5037.patch SOURCES/ && \
	cp ../../../../patches/writers.patch SOURCES/ && \
	cp ../../../../patches/ITS7683.patch SOURCES/ && \
	cp ../../../../patches/ITS8054.patch SOURCES/ && \
	cp ../../../../patches/ITS8336.patch SOURCES/ && \
	cp ../../../../patches/threadpool.patch SOURCES/ && \
	cp ../../../../patches/liblmdb-soname.patch SOURCES/ && \
	$(PKG_BUILD) SPECS/openldap.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
	$(replace-pkginfo) zimbra-openldap/debian/changelog zimbra-openldap/debian/zimbra-lmdb-lib.shlibs zimbra-openldap/debian/zimbra-openldap-lib.shlibs && \
	$(replace-pathinfo) zimbra-openldap/debian/rules && \
	cp ../../src/openldap-$(pvers).tgz zimbra-openldap_$(pvers).orig.tar.gz && \
	tar xfz zimbra-openldap_$(pvers).orig.tar.gz --strip-components=1 -C zimbra-openldap && \
	cp ../../patches/ITS5037.patch zimbra-openldap/debian/patches && \
	cp ../../patches/writers.patch zimbra-openldap/debian/patches && \
	cp ../../patches/ITS7683.patch zimbra-openldap/debian/patches && \
	cp ../../patches/ITS8054.patch zimbra-openldap/debian/patches && \
	cp ../../patches/ITS8336.patch zimbra-openldap/debian/patches && \
	cp ../../patches/threadpool.patch zimbra-openldap/debian/patches && \
	cp ../../patches/liblmdb-soname.patch zimbra-openldap/debian/patches && \
	cd zimbra-openldap && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
