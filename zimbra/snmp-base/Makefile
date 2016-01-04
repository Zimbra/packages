PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../package.def

pname_lc := snmp-base
ptmp := $(TMP_DIR)/$(BUILD_PLATFORM)
zname := zimbra-$(pname_lc)
zspec := $(pname_lc).spec

.PHONY: all clean build setup

all: clean build

build: setup build_$(PKG_EXT)

setup:
	$(MKDIR) $(ptmp)
	$(CP) -prf $(zname) $(ptmp)

build_rpm: specfile = SPECS/$(zspec)
build_rpm:
	$(CD) $(ptmp)/$(zname)/rpm && \
	$(replace-pkginfo) $(specfile) && \
	$(MKDIR) BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(PKG_BUILD) $(specfile)

build_deb:
	$(CD) $(ptmp)/$(zname) && \
	$(replace-pkginfo) debian/changelog && \
	$(CHMOD) u+w debian/control && \
	$(PKG_BUILD)

clean:
	$(generic-clean)
