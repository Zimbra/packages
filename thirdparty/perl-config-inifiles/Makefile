PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(CONFIG_INIFILES)
pname := Config-IniFiles
pname_lc := config-inifiles

pfile := $(pname)-$(pvers).tar.gz
psrc_file := $(SRC_DIR)/$(pfile)
purl := https://cpan.metacpan.org/authors/id/S/SH/SHLOMIF/$(pfile)
zname := zimbra-perl-$(pname_lc)
zspec := $(pname_lc).spec

.PHONY: all clean build getsrc pkgadd pkgrm setup

all: clean getsrc build pkgrm1

build: setup pkgadd build_$(PKG_EXT)

# $(@D) == directory part of the target
getsrc: $(psrc_file)
$(psrc_file):
	$(MKDIR) $(@D) && $(CD) $(@D) && $(WGET) $(purl)

pkgadd:
	$(PKG_EXTRACT) zimbra-perl-base zimbra-perl-list-moreutils

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base

setup:
	$(MKDIR) $(PLATFORM_DIR)
	$(CP) -prf $(zname) $(PLATFORM_DIR)

build_rpm: specfile = SPECS/$(zspec)
build_rpm:
	$(CD) $(PLATFORM_DIR)/$(zname)/rpm && \
	$(replace-pkginfo) $(specfile) && \
	$(replace-pathinfo) $(specfile) && \
	$(replace-perl-modinfo) $(specfile) && \
	$(MKDIR) BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(CP) $(PKG_ROOT)/$(psrc_file) SOURCES/$(zname)-$(pvers).tar.gz && \
	$(PKG_BUILD) $(specfile)

build_deb: z_tgz = $(zname)_$(pvers).orig.tar.gz
build_deb: z_shlibs = $(subst $(zname)/,,$(wildcard $(zname)/debian/z*.shlibs))
build_deb:
	$(CD) $(PLATFORM_DIR)/$(zname) && \
	$(replace-pkginfo) debian/changelog $(z_shlibs) && \
	$(replace-pathinfo) debian/rules && \
	$(replace-perl-modinfo) debian/changelog debian/control debian/copyright debian/watch && \
	$(CP) $(PKG_ROOT)/$(psrc_file) ../$(z_tgz) && \
	$(TAR) xfz ../$(z_tgz) --strip-components=1 && \
	$(PKG_BUILD)

clean: pkgrm
	$(RM) -rf $(PLATFORM_DIR)/$(zname)
	$(RM) -f $(PLATFORM_DIR)/$(zname)_*
