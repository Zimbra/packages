PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(NET_LIBIDN)
pname := Net-LibIDN
pname_lc := net-libidn

pfile := $(pname)-$(pvers).tar.gz
psrc_file := $(SRC_DIR)/$(pfile)
purl := https://cpan.metacpan.org/authors/id/T/TH/THOR/$(pfile)
zname := zimbra-perl-$(pname_lc)
zspec := $(pname_lc).spec

osdeps = $(osdeps.$(BUILD_PLATFORM))

.PHONY: all clean build getsrc pkgadd pkgadd_rpm pkgrm setup

all: clean getsrc build pkgrm1

# $(@D) == directory part of the target
getsrc: $(psrc_file)
$(psrc_file):
	$(MKDIR) $(@D) && $(CD) $(@D) && $(WGET) $(purl)

ifeq ($(PKG_EXT),rpm)
pkgadd: pkgadd_rpm
else
pkgadd:
	$(PKG_EXTRACT) zimbra-perl-base
endif

# libidn-devel is in PowerTools on EL8 and EPEL on EL9.
pkgadd_rpm:
ifeq ($(BUILD_PLATFORM),RHEL8_64)
	sudo yum -y --enablerepo=powertools install libidn-devel
else ifeq ($(BUILD_PLATFORM),RHEL9_64)
	rpm -q epel-release >/dev/null 2>&1 || $(PKG_EXTRACT) epel-release
	sudo yum -y --enablerepo=epel install libidn-devel
else
	$(PKG_EXTRACT) libidn-devel
endif
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
	$(if $(filter RHEL8_64 RHEL9_64,$(BUILD_PLATFORM)),sed -i '/^make install /a chmod u+w %{buildroot}OZCL/perl5/%{perl_archname}/auto/Net/LibIDN/LibIDN.so' $(specfile) &&) \
	$(replace-pathinfo) $(specfile) && \
	$(replace-perl-modinfo) $(specfile) && \
	$(MKDIR) BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(CP) $(psrc_file) SOURCES/$(zname)-$(pvers).tar.gz && \
	$(if $(filter RHEL8_64 RHEL9_64,$(BUILD_PLATFORM)),sed -i '/^%build/i sed -i "s/\\$$cc \\$$cflags/\\$$cc -fPIC \\$$cflags/" Makefile.PL' $(specfile) &&) \
	$(PKG_BUILD) $(specfile)

build_deb: z_tgz = $(zname)_$(pvers).orig.tar.gz
build_deb: z_shlibs = $(subst $(zname)/,,$(wildcard $(zname)/debian/z*.shlibs))
build_deb:
	$(CD) $(PLATFORM_DIR)/$(zname) && \
	$(replace-pkginfo) debian/changelog $(z_shlibs) && \
	$(PERL) -pi -e 's/OSDEPS/$(osdeps)/' debian/control && \
	$(replace-pathinfo) debian/rules && \
	$(replace-perl-modinfo) debian/changelog debian/control debian/copyright debian/watch && \
	$(CP) $(psrc_file) ../$(z_tgz) && \
	$(TAR) xfz ../$(z_tgz) --strip-components=1 --exclude=debian && \
	$(PKG_BUILD)

clean: pkgrm
	$(generic-clean)
