PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

psrctmp := $(PLATFORM_DIR)/srctmp
pvers := $(NGINX_VERSION)
pname := nginx
zname := zimbra-$(pname)
pfile := $(zname)-$(pvers).tar.gz
psrc_file := $(SRC_DIR)/$(pfile)
zspec := $(pname).spec

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

getsrc:
	mkdir -p $(SRC_DIR)
	curl -sLo $(SRC_DIR)/nginx-$(pvers).tgz "https://nginx.org/download/nginx-$(pvers).tar.gz"
	cd $(SRC_DIR) && tar zxf nginx-$(pvers).tgz && rm nginx-$(pvers).tgz
	mv $(SRC_DIR)/$(pname)-$(pvers) $(SRC_DIR)/$(pname)-$(pvers)-zimbra
	mkdir -p $(SRC_DIR)/$(pname)-$(pvers)-zimbra/modules
	cd $(SRC_DIR)/nginx-$(pvers)-zimbra/modules && \
	git clone https://github.com/nviennot/nginx-tcp-keepalive.git nviennot-nginx-tcp-keepalive >/dev/null 2>&1 && \
	cd $(SRC_DIR)/$(pname)-$(pvers)-zimbra/modules/nviennot-nginx-tcp-keepalive && \
	git reset --hard $(NGINX_HTTP_KEEPALIVE) >/dev/null 2>&1 && \
	rm -rf .git && cd $(SRC_DIR)/nginx-$(pvers)-zimbra && \
	patch -p1 < $(PKG_ROOT)/patches/zimbra-1.17.9.patch && \
	cd $(SRC_DIR) && tar zcf $(zname)-$(pvers).tar.gz $(pname)-$(pvers)-zimbra
	rm -rf $(SRC_DIR)/$(pname)-$(pvers)-zimbra

pkgadd:
	$(PKG_EXTRACT) zimbra-base zimbra-openssl-$(PKG_DEV) zimbra-cyrus-sasl-$(PKG_DEV)

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base

setup:
	$(generic-setup)

build: pkgadd setup build_$(PKG_EXT)

build_rpm: specfile = SPECS/$(zspec)
build_rpm:
	$(CD) $(PLATFORM_DIR)/$(zname)/rpm && \
	$(replace-pkginfo) $(specfile) && \
	$(replace-pathinfo) $(specfile) && \
	$(MKDIR) BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(CP) $(psrc_file) SOURCES/ && \
	$(PKG_BUILD) $(specfile)

build_deb: z_tgz = $(zname)_$(pvers).orig.tar.gz
build_deb: z_shlibs = $(subst $(zname)/,,$(wildcard $(zname)/debian/z*.shlibs))
build_deb:
	$(CD) $(PLATFORM_DIR)/$(zname) && \
	$(replace-pkginfo) debian/changelog $(z_shlibs) && \
	$(replace-pathinfo) debian/rules && \
	$(CP) $(psrc_file) ../$(z_tgz) && \
	$(TAR) xfz ../$(z_tgz) --strip-components=1 && \
	$(PKG_BUILD)

clean: pkgrm
	$(generic-clean)
