PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(PHP_VERSION)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/php-$(pvers).tar.bz2)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q http://us2.php.net/distributions/php-$(pvers).tar.bz2 \
	)
else
	@echo "Already have the source, skipping download"
endif

pkgadd:
	$(PKG_EXTRACT) zimbra-base zimbra-httpd-$(PKG_DEV) zimbra-libxml2-$(PKG_DEV) \
	zimbra-aspell zimbra-aspell-$(PKG_DEV)

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base

setup:
	$(generic-setup)

build: pkgadd setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-php/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/php.spec && \
 	$(replace-pathinfo) SPECS/php.spec && \
	cp ../../../../src/php-$(pvers).tar.bz2 SOURCES/zimbra-php-$(pvers).tar.bz2 && \
 	$(PKG_BUILD) SPECS/php.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-php/debian/changelog && \
 	$(replace-pathinfo) zimbra-php/debian/rules && \
	cp ../../src/php-$(pvers).tar.bz2 zimbra-php_$(pvers).orig.tar.bz2 && \
	tar xfj zimbra-php_$(pvers).orig.tar.bz2 --strip-components=1 -C zimbra-php && \
	cd zimbra-php && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
