PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(XML_VERSION)
pname :=  libxml2
pfile := $(pname)-$(pvers).tar.gz
psrc_file := $(SRC_DIR)/$(pfile)
purl := ftp://xmlsoft.org/libxml2//$(pfile)
zname := zimbra-$(pname)
zspec := $(pname).spec

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

# $(@D) == directory part of the target
getsrc: $(psrc_file)
$(psrc_file):
	$(MKDIR) $(@D) && $(CD) $(@D) && $(WGET) $(purl)

xml2 = $(xml2.$(BUILD_PLATFORM))

pkgadd:
	$(PKG_EXTRACT) $(xml2)

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) $(xml2)

setup:
	$(generic-setup)

build: pkgadd setup build_$(PKG_EXT)

build_rpm: specfile = SPECS/$(zspec)
build_rpm:
	$(CD) $(PLATFORM_DIR)/$(zname)/rpm && \
	$(replace-pkginfo) $(specfile) && \
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
	$(PKG_BUILD)

clean:
	$(generic-clean)
