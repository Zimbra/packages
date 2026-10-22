PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(LIBEVENT_VERSION)
pname := libevent
pfile := $(pname)-$(pvers)-stable.tar.gz
psrc_file := $(SRC_DIR)/$(pfile)
purl := https://github.com/libevent/libevent/releases/download/release-$(pvers)-stable/$(pfile)
zname := zimbra-$(pname)
zspec := $(pname).spec
libevent_fix_shebang = $(PERL) -pi -e 's{^make install DESTDIR=\$$\{RPM_BUILD_ROOT\}$$}{$$&."\nsed -i \"1s\@.*\@\#!/usr/bin/env python3\@\" \$${RPM_BUILD_ROOT}/opt/zimbra/common/bin/event_rpcgen.py"}e' $(1)

.PHONY: all getsrc setup build clean pkgadd

all: clean getsrc build

# $(@D) == directory part of the target
getsrc: $(psrc_file)
$(psrc_file):
	$(MKDIR) $(@D) && $(CD) $(@D) && $(WGET) $(purl)

pkgadd:
	$(PKG_EXTRACT) zimbra-base zimbra-openssl-$(PKG_DEV)

setup:
	$(generic-setup)

build: pkgadd setup build_$(PKG_EXT)

build_rpm: specfile = SPECS/$(zspec)
build_rpm:
	$(CD) $(PLATFORM_DIR)/$(zname)/rpm && \
	$(replace-pkginfo) $(specfile) && \
	$(replace-pathinfo) $(specfile) && \
	$(call libevent_fix_shebang,$(specfile)) && \
	$(MKDIR) BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(CP) $(psrc_file) SOURCES/$(zname)-$(pvers)-stable.tar.gz && \
	$(PKG_BUILD) $(specfile)

build_deb: z_tgz = $(zname)_$(pvers).orig.tar.gz
build_deb: z_shlibs = $(subst $(zname)/,,$(wildcard $(zname)/debian/z*.shlibs))
build_deb:
	$(CD) $(PLATFORM_DIR)/$(zname) && \
	$(replace-pkginfo) debian/changelog $(z_shlibs) && \
	$(replace-pathinfo) debian/rules && \
	printf '\noverride_dh_shlibdeps:\n\tdh_shlibdeps --dpkg-shlibdeps-params=--ignore-missing-info\n' >> debian/rules && \
	$(CP) $(psrc_file) ../$(z_tgz) && \
	$(TAR) xfz ../$(z_tgz) --strip-components=1 && \
	$(PKG_BUILD)

clean:
	$(generic-clean)
