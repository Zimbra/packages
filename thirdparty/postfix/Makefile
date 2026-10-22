PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(POSTFIX_VERSION)
pname := postfix
pfile := $(pname)-$(pvers).tar.gz
psrc_file := $(SRC_DIR)/$(pfile)
purl := https://postfix.cs.utah.edu/source/official/$(pfile)
zname := zimbra-$(pname)
zspec := $(pname).spec
postfix_linux7_compat := sed -i "/^Linux[.][[]3456[]][.][*]/i Linux.7.*) SYSTYPE=LINUX6 ;;" makedefs
postfix_disable_nis = $(PERL) -pi -e 's|-DHAS_LMDB -DNO_DB|-DHAS_LMDB -DNO_DB -DNO_NIS|' $(1)
postfix_mysqlclient_lib = $(PERL) -pi -e 's|libmariadb\.so\.3|libmysqlclient.so*|' $(1)
postfix_resolv_lib = $(PERL) -pi -e 's|-L/usr/lib -lz -lm -lpthread|-L/usr/lib -lz -lm -lresolv -lpthread|' $(1)

.PHONY: all getsrc setup build clean pkgadd pkgadd_rpm pkgadd_deb pkgrm

all: clean getsrc build pkgrm1

# $(@D) == directory part of the target
getsrc: $(psrc_file)
$(psrc_file):
	$(MKDIR) $(@D) && $(CD) $(@D) && $(WGET) $(purl)

pkgadd: pkgadd_$(PKG_EXT)

pkgadd_rpm:
	$(PKG_EXTRACT) zimbra-base zimbra-openssl-$(PKG_DEV) zimbra-mariadb-$(PKG_DEV) \
	zimbra-cyrus-sasl-$(PKG_DEV) zimbra-openldap-$(PKG_DEV) zimbra-lmdb-$(PKG_DEV) \
	pcre-devel m4 zlib-devel

pkgadd_deb:
	$(PKG_EXTRACT) zimbra-base zimbra-openssl-$(PKG_DEV) zimbra-mariadb-$(PKG_DEV) \
	zimbra-cyrus-sasl-$(PKG_DEV) zimbra-openldap-$(PKG_DEV) zimbra-lmdb-$(PKG_DEV)

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base

setup:
	$(generic-setup)

build: pkgadd setup build_$(PKG_EXT)

build_rpm: specfile = SPECS/$(zspec)
build_rpm:
	$(CD) $(PLATFORM_DIR)/$(zname)/rpm && \
	$(replace-pkginfo) $(specfile) && \
	$(replace-pathinfo) $(specfile) && \
	$(call postfix_disable_nis,$(specfile)) && \
	$(call postfix_mysqlclient_lib,$(specfile)) && \
	$(call postfix_resolv_lib,$(specfile)) && \
	$(PERL) -0pi -e 's{(%build)}{$$1 . "\n" . q{$(postfix_linux7_compat)}}e' $(specfile) && \
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
	$(call postfix_disable_nis,debian/rules) && \
	$(call postfix_mysqlclient_lib,debian/rules) && \
	$(call postfix_resolv_lib,debian/rules) && \
	$(CP) $(psrc_file) ../$(z_tgz) && \
	$(CP) $(PKG_ROOT)/patches/*.patch debian/patches/ && \
	$(TAR) xfz ../$(z_tgz) --strip-components=1 && \
	$(PERL) -0pi -e 's{(\tmake makefiles)}{\t$(postfix_linux7_compat) && \\\n$$1}' debian/rules && \
	$(PKG_BUILD)

clean: pkgrm
	$(generic-clean)
