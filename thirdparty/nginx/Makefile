PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

psrc := $(PLATFORM_DIR)/src
psrctmp := $(PLATFORM_DIR)/srctmp
pvers := $(NGINX_VERSION)

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

getsrc:
	mkdir -p $(psrc)
	mkdir -p $(psrctmp)
	cp -pr nginx-$(pvers)-zimbra $(psrctmp)
	mkdir -p $(psrctmp)/nginx-$(pvers)-zimbra/modules
	cd $(psrctmp)/nginx-$(pvers)-zimbra/modules && \
	git clone https://github.com/nviennot/nginx-tcp-keepalive.git nviennot-nginx-tcp-keepalive >/dev/null 2>&1 && \
	cd nviennot-nginx-tcp-keepalive && \
	git reset --hard $(NGINX_HTTP_KEEPALIVE) >/dev/null 2>&1 && \
	rm -rf .git
	cd $(psrctmp) && tar cfz zimbra-nginx-$(pvers).tar.gz nginx-$(pvers)-zimbra
	mv $(psrctmp)/zimbra-nginx-$(pvers).tar.gz $(psrc)
	rm -rf $(psrctmp)

pkgadd:
	$(PKG_EXTRACT) zimbra-base zimbra-openssl-$(PKG_DEV) zimbra-cyrus-sasl-$(PKG_DEV)

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base

setup:
	$(generic-setup)

build: pkgadd setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-nginx/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/nginx.spec && \
 	$(replace-pathinfo) SPECS/nginx.spec && \
	cp ../../src/zimbra-nginx-$(pvers).tar.gz SOURCES/ && \
 	$(PKG_BUILD) SPECS/nginx.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-nginx/debian/changelog && \
 	$(replace-pathinfo) zimbra-nginx/debian/rules && \
	cp src/zimbra-nginx-$(pvers).tar.gz zimbra-nginx_$(pvers).orig.tar.gz && \
	tar xfz zimbra-nginx_$(pvers).orig.tar.gz --strip-components=1 -C zimbra-nginx && \
	rm -f zimbra-nginx_$(pvers).orig.tar.gz && \
	cd zimbra-nginx && \
	$(PKG_BUILD) \
	)
endif

rmsrc:
	rm -rf $(psrc)

clean: rmsrc pkgrm
	$(generic-clean)
