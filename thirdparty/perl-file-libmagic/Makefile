PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(FILE_LIBMAGIC)
pname := File-LibMagic
pname_lc := file-libmagic

pfile := $(pname)-$(pvers).tar.gz
psrc_file := $(SRC_DIR)/$(pfile)
purl := https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/$(pfile)
zname := zimbra-perl-$(pname_lc)
zspec := $(pname_lc).spec

libmagic = $(libmagic.$(BUILD_PLATFORM))
libmagic.RHEL := file-devel
libmagic.RHEL6_64 := $(libmagic.RHEL)
libmagic.RHEL7_64 := $(libmagic.RHEL)
libmagic.UBUNTU := libmagic-dev
libmagic.UBUNTU12_64 := $(libmagic.UBUNTU)
libmagic.UBUNTU14_64 := $(libmagic.UBUNTU)
libmagic.UBUNTU16_64 := $(libmagic.UBUNTU)

.PHONY: all clean build getsrc pkgadd pkgrm setup

all: clean getsrc build pkgrm1

# $(@D) == directory part of the target
getsrc: $(psrc_file)
$(psrc_file):
	$(MKDIR) $(@D) && $(CD) $(@D) && $(WGET) $(purl)

pkgadd:
	$(PKG_EXTRACT) zimbra-perl-base $(libmagic)

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base $(libmagic)

setup:
	$(generic-setup)

build: setup pkgadd build_$(PKG_EXT)

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
	$(generic-clean)
