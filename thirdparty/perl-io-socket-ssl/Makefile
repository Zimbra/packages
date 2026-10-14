PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(IO_SOCKET_SSL)
pname := IO-Socket-SSL
pname_lc := io-socket-ssl

pfile := $(pname)-$(pvers).tar.gz
psrc_file := $(SRC_DIR)/$(pfile)
purl := https://cpan.metacpan.org/authors/id/S/SU/SULLR/$(pfile)
zname := zimbra-perl-$(pname_lc)
zspec := $(pname_lc).spec

.PHONY: all clean build getsrc pkgadd pkgrm setup

all: clean getsrc build pkgrm1

# $(@D) == directory part of the target
getsrc: $(psrc_file)
$(psrc_file):
	$(MKDIR) $(@D) && $(CD) $(@D) && $(WGET) $(purl)

pkgadd:
	$(PKG_EXTRACT) zimbra-perl-base zimbra-perl-net-ssleay zimbra-perl-mozilla-ca \
	zimbra-perl-io-socket-ip $(if $(filter UBUNTU20_64,$(BUILD_PLATFORM)),zimbra-openssl-lib)

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
	$(if $(filter RHEL8_64 RHEL9_64,$(BUILD_PLATFORM)),sed -i '/^%build/i sed -i "s/>= 0x00001000/>= (\\$$linked < 0x30000000 ? 0x00001000 : 0x10000000)/" Makefile.PL' $(specfile) &&) \
	$(if $(filter RHEL8_64 RHEL9_64,$(BUILD_PLATFORM)),sed -i '/^%build/i sed -i "/Client non-SSL connection/s@is@like@; /Client non-SSL connection/s@\\"This server is SSL only\\"@qr/This server is SSL only/@" t/core.t' $(specfile) &&) \
	$(replace-pathinfo) $(specfile) && \
	$(MKDIR) BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(CP) $(psrc_file) SOURCES/$(zname)-$(pvers).tar.gz && \
	$(PKG_BUILD) $(specfile)

build_deb: z_tgz = $(zname)_$(pvers).orig.tar.gz
build_deb: z_shlibs = $(subst $(zname)/,,$(wildcard $(zname)/debian/z*.shlibs))
build_deb:
	$(CD) $(PLATFORM_DIR)/$(zname) && \
	$(replace-pkginfo) debian/changelog $(z_shlibs) && \
	$(replace-pathinfo) debian/rules && \
	$(CP) $(psrc_file) ../$(z_tgz) && \
	$(TAR) xfz ../$(z_tgz) --strip-components=1 && \
	$(if $(filter UBUNTU20_64,$(BUILD_PLATFORM)),sed -i 's/>= 0x00001000/>= ($$linked < 0x30000000 ? 0x00001000 : 0x10000000)/' Makefile.PL && sed -i '/Client non-SSL connection/s@is@like@; /Client non-SSL connection/s@"This server is SSL only"@qr/This server is SSL only/@' t/core.t && EDITOR=true dpkg-source --commit . openssl-api-compat &&) \
	$(PKG_BUILD)

clean: pkgrm
	$(generic-clean)
