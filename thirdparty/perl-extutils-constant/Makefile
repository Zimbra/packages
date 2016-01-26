PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(EXTUTILS_CONSTANT)
pname := ExtUtils-Constant
pname_lc := extutils-constant
pfile := $(pname)-$(pvers).tar.gz
psrc_file := $(SRC_DIR)/$(pfile)
purl := https://cpan.metacpan.org/authors/id/N/NW/NWCLARK/$(pfile)
zname := zimbra-perl-$(pname_lc)
zspec := $(pname_lc).spec

.PHONY: all clean build getsrc pkgadd pkgrm setup checkos

all: checkos clean getsrc build pkgrm1

checkos:
ifneq ($(BUILD_PLATFORM), RHEL6_64)
	@echo "Skipping OS, not required"
	@exit 0
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
	$(CP) $(PKG_ROOT)/$(psrc_file) SOURCES/$(zname)-$(pvers).tar.gz && \
	$(PKG_BUILD) $(specfile)

clean: pkgrm
	$(generic-clean)
