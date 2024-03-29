PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

psrctmp := $(PLATFORM_DIR)/srctmp
pvers := $(NGINX_VERSION)
pname := nginx
zname := zimbra-$(pname)
pfile := $(pname)-$(pvers).tar.gz
purl  := http://nginx.org/download/$(pname)-$(pvers).tar.gz
psrc_file := $(SRC_DIR)/$(pfile)
psrc_final_file := $(SRC_DIR)/$(zname)-$(pvers).tar.gz
zspec := $(pname).spec
zmodules := zmmodules

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

getsrc:
	mkdir -p $(SRC_DIR)
	mkdir -p $(psrctmp)
	mkdir -p $(psrctmp)/$(pname)-$(pvers)-zimbra/
	cd $(psrctmp) && \
	$(WGET) $(purl) && \
	$(TAR) -xvf $(pname)-$(pvers).tar.gz && \
	cp -pr $(pname)-$(pvers)/* $(psrctmp)/$(pname)-$(pvers)-zimbra/
	cd $(PLATFORM_DIR)
	mkdir -p $(psrctmp)/$(pname)-$(pvers)-zimbra/modules
	cd $(psrctmp)/$(pname)-$(pvers)-zimbra/modules && \
	git clone https://github.com/nviennot/nginx-tcp-keepalive.git nviennot-nginx-tcp-keepalive >/dev/null 2>&1 && \
	cd nviennot-nginx-tcp-keepalive && \
	git reset --hard $(NGINX_HTTP_KEEPALIVE) >/dev/null 2>&1 && \
	rm -rf .git
	cp -rp $(zmodules) $(psrctmp)/$(pname)-$(pvers)-zimbra/
	cd $(psrctmp) && tar cfz $(zname)-$(pvers).tar.gz $(pname)-$(pvers)-zimbra
	mv $(psrctmp)/$(zname)-$(pvers).tar.gz $(SRC_DIR)
	rm -rf $(psrctmp)
	mkdir -p $(PLATFORM_DIR)/$(zname)/$(zmodules)
	cp -rp $(zmodules) $(PLATFORM_DIR)/$(zname)/

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
	$(CP) $(psrc_final_file) SOURCES/ && \
	$(CP) $(PKG_ROOT)/patches/*.patch SOURCES/ && \
	$(PKG_BUILD) $(specfile)

build_deb: z_tgz = $(zname)_$(pvers).orig.tar.gz
build_deb: z_shlibs = $(subst $(zname)/,,$(wildcard $(zname)/debian/z*.shlibs))
build_deb:
	$(CD) $(PLATFORM_DIR)/$(zname) && \
	$(replace-pkginfo) debian/changelog $(z_shlibs) && \
	$(replace-pathinfo) debian/rules && \
	$(CP) $(psrc_final_file) ../$(z_tgz) && \
	$(TAR) xfz ../$(z_tgz) --strip-components=1 && \
	$(CP) $(PKG_ROOT)/patches/*.patch debian/patches/ && \
	$(PKG_BUILD)

clean: pkgrm
	$(generic-clean)
