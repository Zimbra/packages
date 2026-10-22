PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(MIME_TOOLS)
pname := MIME-tools
pname_lc := mime-tools

pfile := $(pname)-$(pvers).tar.gz
psrc_file := $(SRC_DIR)/$(pfile)
purl := https://cpan.metacpan.org/authors/id/D/DS/DSKOLL/$(pfile)
zname := zimbra-perl-$(pname_lc)
zspec := $(pname_lc).spec

.PHONY: all clean build getsrc pkgadd pkgrm setup

all: clean getsrc build pkgrm1

# $(@D) == directory part of the target
getsrc: $(psrc_file)
$(psrc_file):
	$(MKDIR) $(@D) && $(CD) $(@D) && $(WGET) $(purl)

zpzc = zimbra-perl-mailtools zimbra-perl-convert-binhex zimbra-perl-timedate

ifneq ($(filter RHEL8_64 RHEL9_64,$(BUILD_PLATFORM)),)
zptest := perl-Test-Deep
endif

pkgadd:
	$(PKG_EXTRACT) $(if $(filter RHEL8_64,$(BUILD_PLATFORM)),--enablerepo=powertools) $(if $(filter RHEL9_64,$(BUILD_PLATFORM)),--enablerepo=crb) zimbra-perl-base $(zpzc) $(zptest)

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base

setup:
	$(generic-setup)

build: setup pkgadd build_$(PKG_EXT)

build_rpm: specfile = SPECS/$(zspec)
build_rpm:
	$(CD) $(PLATFORM_DIR)/$(zname)/rpm && \
	$(replace-pkginfo) $(specfile) && \
	$(if $(filter RHEL8_64 RHEL9_64,$(BUILD_PLATFORM)),sed -i 's/^perl -I /perl -I . -I /' $(specfile) &&) \
	$(replace-pathinfo) $(specfile) && \
	$(replace-perl-modinfo) $(specfile) && \
	$(MKDIR) BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(CP) $(psrc_file) SOURCES/$(zname)-$(pvers).tar.gz && \
	$(PKG_BUILD) $(specfile)

build_deb: z_tgz = $(zname)_$(pvers).orig.tar.gz
build_deb: z_shlibs = $(subst $(zname)/,,$(wildcard $(zname)/debian/z*.shlibs))
build_deb:
	$(CD) $(PLATFORM_DIR)/$(zname) && \
	$(replace-pkginfo) debian/changelog $(z_shlibs) && \
	$(replace-pathinfo) debian/rules && \
	$(replace-perl-modinfo) debian/changelog debian/control debian/copyright debian/watch && \
	$(CP) $(psrc_file) ../$(z_tgz) && \
	$(TAR) xfz ../$(z_tgz) --strip-components=1 && \
	$(CP) $(PKG_ROOT)/patches/*.patch debian/patches/ && \
	$(PKG_BUILD)

clean: pkgrm
	$(generic-clean)
