PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(NET_LIBIDN2)
pname := Net-LibIDN2
pname_lc := net-libidn2

pfile := $(pname)-$(pvers).tar.gz
psrc_file := $(SRC_DIR)/$(pfile)
purl := https://cpan.metacpan.org/authors/id/T/TH/THOR/$(pfile)
zname := zimbra-perl-$(pname_lc)
zspec := $(pname_lc).spec

.PHONY: all checkos clean build getsrc pkgadd pkgrm setup

all: checkos clean getsrc build pkgrm1

checkos:
ifneq ($(BUILD_PLATFORM), RHEL9_64)
	@echo "Skipping OS, not required"
	@exit 1
endif

# $(@D) == directory part of the target
getsrc: $(psrc_file)
$(psrc_file):
	$(MKDIR) $(@D) && $(CD) $(@D) && $(WGET) $(purl)

pkgadd:
	$(PKG_EXTRACT) zimbra-perl-base

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
	$(TAR) xfz ../$(z_tgz) --strip-components=1 --exclude=debian && \
	$(CP) $(PKG_ROOT)/patches/*.patch debian/patches/ && \
	$(PKG_BUILD)

clean: pkgrm
	$(generic-clean)
