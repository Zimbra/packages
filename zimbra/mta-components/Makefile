PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pname_lc := mta-components
zname := zimbra-$(pname_lc)
zspec := $(pname_lc).spec

osdeps = $(osdeps.$(BUILD_PLATFORM))

.PHONY: all clean build setup

all: clean build

build: setup build_$(PKG_EXT)

setup:
	$(generic-setup)

build_rpm: specfile = SPECS/$(zspec)
build_rpm:
	$(CD) $(PLATFORM_DIR)/$(zname)/rpm && \
	$(replace-pkginfo) $(specfile) && \
	$(PERL) -pi -e 's/OSDEPS/$(osdeps)/' $(specfile) && \
	$(MKDIR) BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(PKG_BUILD) $(specfile)

build_deb:
	$(CD) $(PLATFORM_DIR)/$(zname) && \
	$(replace-pkginfo) debian/changelog debian/control && \
	$(PKG_BUILD)

clean:
	$(generic-clean)
