PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(MAIL_SPAMASSASSIN)
pname := Mail-SpamAssassin
pname_lc := mail-spamassassin

pfile := $(pname)-$(pvers).tar.gz
psrc_file := $(SRC_DIR)/$(pfile)
purl :=  https://cpan.metacpan.org/authors/id/K/KM/KMCGRAIL/SpamAssassin/$(pfile)
zname := zimbra-perl-$(pname_lc)
zspec := $(pname_lc).spec

.PHONY: all clean build getsrc pkgadd pkgrm setup

all: clean getsrc build pkgrm1

# $(@D) == directory part of the target
getsrc: $(psrc_file)
$(psrc_file):
	$(MKDIR) $(@D) && $(CD) $(@D) && $(WGET) $(purl)

pkgadd:
	$(PKG_EXTRACT) zimbra-perl-base zimbra-perl-digest-sha1 \
	zimbra-perl-html-parser zimbra-perl-io-compress \
	zimbra-perl-mail-dkim zimbra-perl-net-dns zimbra-perl-netaddr-ip \
	zimbra-perl-mail-spf zimbra-perl-encode-detect zimbra-perl-net-cidr-lite

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
	$(CP) $(PKG_ROOT)/patches/spamassassin-net-dns.patch SOURCES/ && \
        $(CP) $(PKG_ROOT)/patches/spamassassin-mail.patch SOURCES/ && \
	$(PKG_BUILD) $(specfile)

build_deb: z_tgz = $(zname)_$(pvers).orig.tar.gz
build_deb: z_shlibs = $(subst $(zname)/,,$(wildcard $(zname)/debian/z*.shlibs))
build_deb:
	$(CD) $(PLATFORM_DIR)/$(zname) && \
	$(replace-pkginfo) debian/changelog $(z_shlibs) && \
	$(replace-pathinfo) debian/rules && \
	$(replace-perl-modinfo) debian/changelog debian/control debian/copyright debian/watch && \
	$(CP) $(psrc_file) ../$(z_tgz) && \
	$(CP) $(PKG_ROOT)/patches/spamassassin-net-dns.patch debian/patches && \
        $(CP) $(PKG_ROOT)/patches/spamassassin-mail.patch debian/patches && \
	$(TAR) xfz ../$(z_tgz) --strip-components=1 && \
	$(PKG_BUILD)

clean: pkgrm
	$(generic-clean)
