PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(BSD_VERSION)
pname := libbsd
pfile := $(pname)-$(pvers).tar.xz
psrc_file := $(SRC_DIR)/$(pfile)
purl := http://libbsd.freedesktop.org/releases/$(pfile)
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

build: setup build_$(PKG_EXT)

build_rpm: specfile = SPECS/$(zspec)
build_rpm:
	$(CD) $(PLATFORM_DIR)/$(zname)/rpm && \
	$(replace-pkginfo) $(specfile) && \
	$(replace-pathinfo) $(specfile) && \
	$(MKDIR) BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(CP) $(PKG_ROOT)/$(psrc_file) SOURCES/$(zname)-$(pvers).tar.xz && \
	$(PKG_BUILD) $(specfile)

build_deb: z_tgz = $(zname)_$(pvers).orig.tar.xz
build_deb: z_shlibs = $(subst $(zname)/,,$(wildcard $(zname)/debian/z*.shlibs))
build_deb:
	$(CD) $(PLATFORM_DIR)/$(zname) && \
	$(replace-pkginfo) debian/changelog $(z_shlibs) && \
	$(replace-pathinfo) debian/rules && \
	$(CP) $(PKG_ROOT)/$(psrc_file) ../$(z_tgz) && \
	$(TAR) xf ../$(z_tgz) --strip-components=1 && \
	$(PKG_BUILD)

clean:
	$(generic-clean)
