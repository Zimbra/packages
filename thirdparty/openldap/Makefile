PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(LDAP_VERSION)
pname := openldap
pfile := $(pname)-$(pvers).tgz
psrc_file := $(SRC_DIR)/$(pfile)
purl := ftp://ftp.openldap.org/pub/OpenLDAP/openldap-release/$(pfile)
zname := zimbra-$(pname)
zspec := $(pname).spec
DEB_TEST ?= nocheck

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

# $(@D) == directory part of the target
getsrc: $(psrc_file)
$(psrc_file):
	$(MKDIR) $(@D) && $(CD) $(@D) && $(WGET) $(purl)

pkgadd:
	$(PKG_EXTRACT) zimbra-base zimbra-openssl-$(PKG_DEV) zimbra-cyrus-sasl-$(PKG_DEV) \
	zimbra-libltdl-$(PKG_DEV) zimbra-curl-$(PKG_DEV) zimbra-heimdal-$(PKG_DEV) zimbra-libxml2-$(PKG_DEV)

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
	$(CP) $(psrc_file) SOURCES/$(zname)-$(pvers).tgz && \
	$(CP) $(PKG_ROOT)/patches/*.patch SOURCES/ && \
	$(PKG_BUILD) $(specfile)

build_deb: export DEB_BUILD_OPTIONS=$(DEB_TEST)
build_deb: z_tgz = $(zname)_$(pvers).orig.tar.gz
build_deb: z_shlibs = $(subst $(zname)/,,$(wildcard $(zname)/debian/z*.shlibs))
build_deb:
	$(CD) $(PLATFORM_DIR)/$(zname) && \
	$(replace-pkginfo) debian/changelog $(z_shlibs) && \
	$(replace-pathinfo) debian/rules && \
	$(CP) $(psrc_file) ../$(z_tgz) && \
	$(CP) $(PKG_ROOT)/patches/*.patch debian/patches/ && \
	$(TAR) xfz ../$(z_tgz) --strip-components=1 && \
	$(PKG_BUILD)

clean: pkgrm
	$(generic-clean)
