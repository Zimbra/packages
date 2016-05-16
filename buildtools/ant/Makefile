PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(ANT_VERSION)
pname := ant
pfile := apache-$(pname)-$(pvers)-bin.tar.bz2
psrc_file := $(SRC_DIR)/$(pfile)
purl := http://apache.osuosl.org/$(pname)/binaries/apache-$(pname)-$(pvers)-bin.tar.bz2
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
	$(CP) $(psrc_file) SOURCES/$(zname)-$(pvers).tar.bz2 && \
	$(PKG_BUILD) $(specfile)

build_deb: z_tgz = $(zname)_$(pvers).orig.tar.bz2
build_deb: z_shlibs = $(subst $(zname)/,,$(wildcard $(zname)/debian/z*.shlibs))
build_deb:
	$(CD) $(PLATFORM_DIR)/$(zname) && \
	$(replace-pkginfo) debian/changelog $(z_shlibs) && \
	$(replace-pathinfo) debian/rules && \
	$(CP) $(psrc_file) ../$(z_tgz) && \
	$(TAR) xfj ../$(z_tgz) --strip-components=1 && \
	$(PKG_BUILD)

clean:
	$(generic-clean)
