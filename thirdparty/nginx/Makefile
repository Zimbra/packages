PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

psrctmp := $(PLATFORM_DIR)/srctmp
pvers := $(NGINX_VERSION)
pname := nginx
zname := zimbra-$(pname)
pfile := $(zname)-$(pvers).tar.gz
psrc_file := $(SRC_DIR)/$(pfile)
zspec := $(pname).spec
zmodules := zmmodules

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

getsrc:
	mkdir -p $(SRC_DIR)
	mkdir -p $(psrctmp)
	cp -pr $(pname)-$(pvers)-zimbra $(psrctmp)
	mkdir -p $(psrctmp)/$(pname)-$(pvers)-zimbra/modules
	cd $(psrctmp)/$(pname)-$(pvers)-zimbra/modules && \
	git clone https://github.com/nviennot/nginx-tcp-keepalive.git nviennot-nginx-tcp-keepalive >/dev/null 2>&1 && \
	cd nviennot-nginx-tcp-keepalive && \
	git reset --hard $(NGINX_HTTP_KEEPALIVE) >/dev/null 2>&1 && \
	rm -rf .git
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
