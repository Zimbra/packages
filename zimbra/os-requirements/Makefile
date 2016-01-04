PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../package.def

pname_lc := os-requirements
ptmp := $(TMP_DIR)/$(BUILD_PLATFORM)
zname := zimbra-$(pname_lc)
zspec := $(pname_lc).spec

osdeps = $(osdeps.$(BUILD_PLATFORM))
osdeps.UBUNTU14_64 := libgmp10, libperl5.18
osdeps.UBUNTU12_64 := libgmp3c2, libperl5.14
osdeps.RHEL7_64 := nmap-ncat
osdeps.RHEL6_64 := nc

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
	$(PERL) -pi -e 's/OSDEPS/$(osdeps)/' $(specfile) && \
	$(MKDIR) BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(PKG_BUILD) $(specfile)

build_deb:
	$(CD) $(ptmp)/$(zname) && \
	$(replace-pkginfo) debian/changelog && \
	$(CHMOD) u+w debian/control && \
	$(PERL) -pi -e 's/OSDEPS/$(osdeps)/' debian/control && \
	$(PKG_BUILD)

clean:
	$(generic-clean)
