PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(MARIADB_VERSION)
pname := mariadb
pfile := $(pname)-$(pvers).tar.gz
psrc_file := $(SRC_DIR)/$(pfile)
purl := https://archive.mariadb.org/$(pname)-$(pvers)/source/$(pfile)
zname := zimbra-$(pname)
zspec := $(pname).spec

.PHONY: all getsrc setup build clean pkgadd pkgadd_rpm pkgadd_deb pkgrm

all: clean getsrc build pkgrm1

# $(@D) == directory part of the target
getsrc: $(psrc_file)
$(psrc_file):
	$(MKDIR) $(@D) && $(CD) $(@D) && $(WGET) $(purl)

pkgadd: pkgadd_$(PKG_EXT)

pkgadd_rpm:
	$(PKG_EXTRACT) zimbra-base zimbra-openssl-$(PKG_DEV) libaio-devel ncurses-devel

pkgadd_deb:
	$(PKG_EXTRACT) zimbra-base zimbra-openssl-$(PKG_DEV) debhelper m4 dpkg-dev \
	cmake libaio-dev libncurses5-dev

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
	perl -pi -e 's|zimbra-openssl-devel = ([^[:space:]]+)|zimbra-openssl-devel >= $$1|' $(specfile) && \
	$(MKDIR) BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(CP) $(psrc_file) SOURCES/$(zname)-$(pvers).tar.gz && \
	$(CP) $(PKG_ROOT)/patches/*.patch SOURCES/ && \
	$(PKG_BUILD) $(specfile)

build_deb: z_tgz = $(zname)_$(pvers).orig.tar.gz
build_deb: z_shlibs = $(subst $(zname)/,,$(wildcard $(zname)/debian/z*.shlibs))
build_deb:
	$(CD) $(PLATFORM_DIR)/$(zname) && \
	$(replace-pkginfo) debian/changelog $(z_shlibs) && \
	$(replace-pathinfo) debian/rules && \
	$(CP) $(psrc_file) ../$(z_tgz) && \
	$(CP) $(PKG_ROOT)/patches/*.patch debian/patches/ && \
	$(TAR) xfz ../$(z_tgz) --strip-components=1 --exclude=debian && \
	$(PKG_BUILD)

clean: pkgrm
	$(generic-clean)
