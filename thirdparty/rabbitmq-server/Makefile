PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(RABBITMQ_VERSION)
pname := rabbitmq-server
pfile := $(pname)-$(pvers).tar.xz
psrc_file := $(SRC_DIR)/$(pfile)
purl := https://github.com/rabbitmq/$(pname)/releases/download/v$(pvers)/$(pname)-$(pvers).tar.xz
zname := zimbra-$(pname)
zspec := $(pname).spec

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

# $(@D) == directory part of the target
getsrc: $(psrc_file)
$(psrc_file):
	$(MKDIR) $(@D) && $(CD) $(@D) && $(WGET) $(purl)

pkgadd:
	$(PKG_EXTRACT) zimbra-base zimbra-erlang zimbra-openssl-$(PKG_DEV) zip rsync gzip sed

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
	$(MKDIR) BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(CP) $(psrc_file) SOURCES/$(zname)-$(pvers).tar.xz && \
	$(CP) $(PKG_ROOT)/patches/*.patch SOURCES/ && \
	$(CP) $(PKG_ROOT)/rabbitmq-env.conf SOURCES/ && \
	$(PKG_BUILD) $(specfile)

build_deb: z_tgz = $(zname)_$(pvers).orig.tar.xz
build_deb: z_shlibs = $(subst $(zname)/,,$(wildcard $(zname)/debian/z*.shlibs))
build_deb:
	$(CD) $(PLATFORM_DIR)/$(zname) && \
	$(replace-pkginfo) debian/changelog $(z_shlibs) && \
	$(replace-pathinfo) debian/rules && \
	$(CP) $(psrc_file) ../$(z_tgz) && \
	$(CP) $(PKG_ROOT)/patches/*.patch debian/patches/ && \
	$(CP) $(PKG_ROOT)/rabbitmq-env.conf debian/ && \
	$(TAR) -xf ../$(z_tgz) --strip-components=1 && \
	$(PKG_BUILD)

clean:  pkgrm
	$(generic-clean)
