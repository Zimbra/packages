PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pname_lc := base
zname := zimbra-perl-$(pname_lc)
zspec := $(pname_lc).spec

.PHONY: all clean build setup

all: clean build

build: setup build_$(PKG_EXT)

setup:
	$(MKDIR) $(PLATFORM_DIR)
	$(CP) -prf $(zname) $(PLATFORM_DIR)

build_rpm: specfile = SPECS/$(zspec)
build_rpm:
	$(CD) $(PLATFORM_DIR)/$(zname)/rpm && \
	$(replace-pkginfo) $(specfile) && \
	$(MKDIR) BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(PKG_BUILD) $(specfile)

build_deb: z_tgz = $(zname)_$(pvers).orig.tar.gz
build_deb: z_shlibs = $(subst $(zname)/,,$(wildcard $(zname)/debian/z*.shlibs))
build_deb:
	$(CD) $(PLATFORM_DIR)/$(zname) && \
	$(replace-pkginfo) debian/changelog && \
	$(PKG_BUILD)

clean:
	$(RM) -rf $(PLATFORM_DIR)/$(zname)
	$(RM) -f $(PLATFORM_DIR)/$(zname)_*
