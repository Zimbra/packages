PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(NET_DNS_RESOLVER_PROGRAMMABLE)
pname := Net-DNS-Resolver-Programmable
pname_lc := net-dns-resolver-programmable

pfile := $(pname)-v$(pvers).tar.gz
psrc_file := $(SRC_DIR)/$(pfile)
purl := https://cpan.metacpan.org/authors/id/J/JM/JMEHNLE/net-dns-resolver-programmable/$(pfile)
zname := zimbra-perl-$(pname_lc)
zspec := $(pname_lc).spec

module-build = $(module-build.$(BUILD_PLATFORM))
module-build-purge = $(module-build-purge.$(BUILD_PLATFORM))

.PHONY: all clean build getsrc pkgadd pkgrm setup

all: clean getsrc build pkgrm1

# $(@D) == directory part of the target
getsrc: $(psrc_file)
$(psrc_file):
	$(MKDIR) $(@D) && $(CD) $(@D) && $(WGET) $(purl)

pkgadd:
	$(PKG_EXTRACT) zimbra-perl-base zimbra-perl-net-dns $(module-build)

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base $(module-build-purge)

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
	$(PKG_BUILD)

clean: pkgrm
	$(generic-clean)
