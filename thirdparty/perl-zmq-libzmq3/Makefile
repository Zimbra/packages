PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(ZMQ_LIB)
pname := ZMQ-LibZMQ3
pname_lc := zmq-libzmq3

pfile := $(pname)-$(pvers).tar.gz
psrc_file := $(SRC_DIR)/$(pfile)
purl := https://cpan.metacpan.org/authors/id/D/DM/DMAKI/$(pfile)

zname := zimbra-perl-$(pname_lc)
zspec := $(pname_lc).spec

.PHONY: all clean build getsrc pkgadd pkgrm setup

all: clean getsrc build pkgrm1

# $(@D) == directory part of the target
getsrc: $(psrc_file)
$(psrc_file):
	$(MKDIR) $(@D) && $(CD) $(@D) && $(WGET) $(purl)

zpzc = zimbra-perl-zmq-constants
zptest = $(zptest.$(BUILD_PLATFORM))

ifneq ($(filter UBUNTU20_64 UBUNTU22_64 UBUNTU24_64,$(BUILD_PLATFORM)),)
zptest := $(zptest.UBUNTU)
else ifneq ($(filter RHEL8_64 RHEL9_64,$(BUILD_PLATFORM)),)
zptest := perl-Test-Fatal perl-Test-Requires
endif

pkgadd:
	$(PKG_EXTRACT) $(if $(filter RHEL8_64,$(BUILD_PLATFORM)),--enablerepo=powertools) $(if $(filter RHEL9_64,$(BUILD_PLATFORM)),--enablerepo=crb) zimbra-perl-base zimbra-zeromq-$(PKG_DEV) \
	zimbra-libsodium-$(PKG_DEV) $(zpzc) $(zptest)

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base $(zptest)

setup:
	$(generic-setup)

build: setup pkgadd build_$(PKG_EXT)

build_rpm: specfile = SPECS/$(zspec)
build_rpm:
	$(CD) $(PLATFORM_DIR)/$(zname)/rpm && \
	$(replace-pkginfo) $(specfile) && \
	$(if $(filter RHEL8_64 RHEL9_64,$(BUILD_PLATFORM)),sed -i 's/ perl -I / perl -I . -I /' $(specfile) &&) \
	$(if $(filter RHEL9_64,$(BUILD_PLATFORM)),sed -i '/^make install /a chmod u+w %{buildroot}OZCL/perl5/%{perl_archname}/auto/ZMQ/LibZMQ3/LibZMQ3.so' $(specfile) &&) \
	$(replace-pathinfo) $(specfile) && \
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
	$(TAR) xfz ../$(z_tgz) --strip-components=1 && \
	$(PKG_BUILD)

clean: pkgrm
	$(generic-clean)
