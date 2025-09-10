PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(OPENSSL_VERSION)
pname := openssl
pfile := $(pname)-$(pvers).tar.gz
psrc_file := $(SRC_DIR)/$(pfile)
purl := https://github.com/openssl/openssl/releases/download/openssl-$(pvers)/$(pfile)
zname := zimbra-$(pname)
zspec := $(pname).spec

.PHONY: all getsrc setup build clean

all: clean getsrc build

# $(@D) == directory part of the target
getsrc: $(psrc_file)
$(psrc_file):
	$(MKDIR) $(@D) && $(CD) $(@D) && $(WGET) $(purl)

setup:
	$(generic-setup)

build_fips:
	$(MKDIR) $(PLATFORM_DIR)/tmp
	$(WGET) -O $(PLATFORM_DIR)/tmp/openssl-$(OPENSSL_FIPS_VERSION).tar.gz https://www.openssl.org/source/openssl-$(OPENSSL_FIPS_VERSION).tar.gz && \
	$(CD) $(PLATFORM_DIR)/tmp && $(TAR) xfz openssl-$(OPENSSL_FIPS_VERSION).tar.gz && \
	$(CD) $(PLATFORM_DIR)/tmp/openssl-$(OPENSSL_FIPS_VERSION) && ./Configure no-idea enable-fips enable-ec_nistp_64_gcc_128 no-mdc2 --with-rand-seed=devrandom,rdcpu,os,getrandom shared linux-x86_64 -g -O2 --prefix=$(PLATFORM_DIR)/tmp/openssl-fips --openssldir=$(PLATFORM_DIR)/tmp/openssl-fips/ssl && $(MAKE) install_fips

build: setup build_fips build_$(PKG_EXT)

build_rpm: specfile = SPECS/$(zspec)
build_rpm: 
	$(CD) $(PLATFORM_DIR)/$(zname)/rpm && \
	$(replace-pkginfo) $(specfile) && \
	$(replace-pathinfo) $(specfile) && \
	$(MKDIR) BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(CP) $(psrc_file) SOURCES/$(zname)-$(pvers).tar.gz && \
	$(CP) $(PKG_ROOT)/openssl-fips.cnf SOURCES/ && \
	$(PKG_BUILD) $(specfile)

build_deb: z_tgz = $(zname)_$(pvers).orig.tar.gz
build_deb: z_shlibs = $(subst $(zname)/,,$(wildcard $(zname)/debian/z*.shlibs))
build_deb:
	$(CD) $(PLATFORM_DIR)/$(zname) && \
	$(replace-pkginfo) debian/changelog $(z_shlibs) && \
	$(replace-pathinfo) debian/rules && \
	$(CP) $(psrc_file) ../$(z_tgz) && \
	$(CP) $(PKG_ROOT)/openssl-fips.cnf debian/ && \
	$(TAR) xfz ../$(z_tgz) --strip-components=1 && \
	$(PKG_BUILD)

clean:
	$(generic-clean)
