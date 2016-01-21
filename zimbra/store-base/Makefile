PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pname_lc := store-base
zname := zimbra-$(pname_lc)
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

build_deb:
	$(CD) $(PLATFORM_DIR)/$(zname) && \
	$(replace-pkginfo) debian/changelog && \
	$(PKG_BUILD)

clean:
	$(generic-clean)
