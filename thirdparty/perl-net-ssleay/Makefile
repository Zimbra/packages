PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(NET_SSLEAY)
pname := Net-SSLeay
pname_lc := net-ssleay

pfile := $(pname)-$(pvers).tar.gz
psrc_file := $(SRC_DIR)/$(pfile)
purl := https://cpan.metacpan.org/authors/id/C/CH/CHRISN//$(pfile)

zname := zimbra-perl-$(pname_lc)
zspec := $(pname_lc).spec

.PHONY: all clean build getsrc pkgadd pkgrm setup

all: clean getsrc build pkgrm1

# $(@D) == directory part of the target..
getsrc: $(psrc_file)
$(psrc_file):
	$(MKDIR) $(@D) && $(CD) $(@D) && $(WGET) $(purl)

pkgadd:
	$(PKG_EXTRACT) zimbra-perl-base zimbra-openssl-$(PKG_DEV)

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base

setup:
	$(generic-setup)

build: setup pkgadd build_$(PKG_EXT)

# Keep the upstream tests compatible with newer OpenSSL versions.
define fix-openssl-tests
perl -pi -e 'if (/X509V3_EXT_print\(\$$ext\), \$$ext_data/) { print q(          if (is_openssl() && Net::SSLeay::SSLeay >= 0x30400000) { $$ext_data =~ s{emailAddress::}{emailAddress:} if $$nid == 85 || $$nid == 86; if ($$nid == 103 && Net::SSLeay::SSLeay > 0x3040000f) { $$ext_data =~ s{(\nFull Name:)}{\n$$1}g; $$ext_data .= "\n"; } })."\n"; } s/(X509_set_version\(\$$x509, )3/$${1}2/; s/(X509_get_version\(\$$x509\), )3/$${1}2/; s/(X509_REQ_set_version\(\$$req, )2/$${1}0/; s/(X509_REQ_get_version\(\$$req\), )2/$${1}0/;' t/local/32_x509_get_cert_info.t t/local/33_x509_create_cert.t
endef

build_rpm: specfile = SPECS/$(zspec)
build_rpm: export OPENSSL_TEST_FIX = $(fix-openssl-tests)
build_rpm:
	$(CD) $(PLATFORM_DIR)/$(zname)/rpm && \
	$(replace-pkginfo) $(specfile) && \
	$(if $(filter RHEL9_64,$(BUILD_PLATFORM)),sed -i '/^make install /a chmod u+w %{buildroot}OZCL/perl5/%{perl_archname}/auto/Net/SSLeay/SSLeay.so' $(specfile) &&) \
	$(replace-pathinfo) $(specfile) && \
	perl -pi -e 'print "$$ENV{OPENSSL_TEST_FIX}\n" if /^%build/' $(specfile) && \
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
	$(fix-openssl-tests) && \
	EDITOR=true dpkg-source --commit . openssl-test-compat && \
	$(PKG_BUILD)

clean: pkgrm
	$(generic-clean)
