PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../package.def

pvers := $(ZMQ_LIB)
pname := ZMQ-LibZMQ3
pname_lc := zmq-libzmq3

pfile := $(pname)-$(pvers).tar.gz
psrc_file := $(SRC_DIR)/$(pfile)
purl := https://cpan.metacpan.org/authors/id/D/DM/DMAKI/$(pfile)

ptmp := $(TMP_DIR)/$(BUILD_PLATFORM)
zname := zimbra-perl-$(pname_lc)
zspec := $(pname_lc).spec

.PHONY: all clean build getsrc pkgadd pkgrm setup

all: clean getsrc build pkgrm1

build: setup pkgadd build_$(PKG_EXT)

# $(@D) == directory part of the target
getsrc: $(psrc_file)
$(psrc_file):
	$(MKDIR) $(@D) && $(CD) $(@D) && $(WGET) $(purl)

zpzc = zimbra-perl-zmq-constants
zptest = $(zptest.$(BUILD_PLATFORM))
zptest.UBUNTU14_64 := libtest-fatal-perl libtest-requires-perl libtest-sharedfork-perl libtry-tiny-perl
zptest.UBUNTU12_64 := $(zptest.UBUNTU14_64)
zptest.RHEL7_64 := perl-Test-Fatal perl-Test-Requires

pkgadd:
	$(PKG_EXTRACT) zimbra-perl-base zimbra-zeromq-$(PKG_DEV) \
	zimbra-libsodium-$(PKG_DEV) $(zpzc) $(zptest)

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base $(zptest)

setup:
	$(MKDIR) $(ptmp)
	$(CP) -prf $(zname) $(ptmp)

build_rpm: specfile = SPECS/$(zspec)
build_rpm:
	$(CD) $(ptmp)/$(zname)/rpm && \
	$(replace-pkginfo) $(specfile) && \
	$(replace-pathinfo) $(specfile) && \
	$(MKDIR) BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(CP) $(PKG_ROOT)/$(psrc_file) SOURCES/$(zname)-$(pvers).tar.gz && \
	$(PKG_BUILD) $(specfile)

build_deb: z_tgz = $(zname)_$(pvers).orig.tar.gz
build_deb: z_shlibs = $(subst $(zname)/,,$(wildcard $(zname)/debian/z*.shlibs))
build_deb:
	$(CD) $(ptmp)/$(zname) && \
	$(replace-pkginfo) debian/changelog $(z_shlibs) && \
	$(replace-pathinfo) debian/rules && \
	$(CHMOD) u+w debian/control && \
	$(CP) $(PKG_ROOT)/$(psrc_file) ../$(z_tgz) && \
	$(TAR) xfz ../$(z_tgz) --strip-components=1 && \
	$(PKG_BUILD)

clean: pkgrm
	$(RM) -rf $(ptmp)/$(zname)
	$(RM) -f $(ptmp)/$(zname)_*
