PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(DBD_MYSQL)
pname := DBD-mysql
pname_lc := dbd-mysql

pfile := $(pname)-$(pvers).tar.gz
psrc_file := $(SRC_DIR)/$(pfile)
purl := https://www.cpan.org/modules/by-module/DBD/$(pfile)
zname := zimbra-perl-$(pname_lc)
zspec := $(pname_lc).spec

devel-checklib = $(if $(filter UBUNTU20_64 UBUNTU22_64 UBUNTU24_64,$(BUILD_PLATFORM)),libdevel-checklib-perl)$(if $(filter RHEL8_64 RHEL9_64,$(BUILD_PLATFORM)),perl-Devel-CheckLib)

# Makefile.PL checks that -lz can be linked, which needs zlib headers/libz.so on RHEL
zlib-devel = $(if $(filter RHEL8_64 RHEL9_64,$(BUILD_PLATFORM)),zlib-devel)

# perl-Devel-CheckLib may live in the PowerTools/CRB repos on RHEL
extra-repo = $(if $(filter RHEL8_64,$(BUILD_PLATFORM)),--enablerepo=powertools)$(if $(filter RHEL9_64,$(BUILD_PLATFORM)),--enablerepo=crb)

.PHONY: all clean build getsrc pkgadd pkgrm setup

all: clean getsrc build pkgrm1

# $(@D) == directory part of the target
getsrc: $(psrc_file)
$(psrc_file):
	$(MKDIR) $(@D) && $(CD) $(@D) && $(WGET) $(purl)

pkgadd:
	$(PKG_EXTRACT) $(extra-repo) zimbra-perl-base zimbra-perl-dbi \
	zimbra-mariadb-$(PKG_DEV) zimbra-openssl-$(PKG_DEV) $(devel-checklib) $(zlib-devel)

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base $(devel-checklib)

setup:
	$(generic-setup)

build: setup pkgadd build_$(PKG_EXT)

build_rpm: specfile = SPECS/$(zspec)
build_rpm:
	$(CD) $(PLATFORM_DIR)/$(zname)/rpm && \
	$(replace-pkginfo) $(specfile) && \
	$(if $(filter RHEL9_64,$(BUILD_PLATFORM)),sed -i '/^make install/a chmod u+w %{buildroot}OZCL/perl5/%{perl_archname}/auto/DBD/mysql/mysql.so' $(specfile) &&) \
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
	$(PKG_BUILD)

clean: pkgrm
	$(generic-clean)
