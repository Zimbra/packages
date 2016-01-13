PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pname_lc := openjdk-cacerts
ptmp := $(TMP_DIR)/$(BUILD_PLATFORM)
zname := zimbra-$(pname_lc)
zspec := $(pname_lc).spec

.PHONY: all clean build pkgadd pkgrm setup

all: clean build pkgrm1

build: setup pkgadd build_$(PKG_EXT)

pkgadd:
	$(PKG_EXTRACT) zimbra-openjdk

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base

setup:
	$(MKDIR) $(ptmp)
	$(CP) -prf $(zname) $(ptmp)
	$(CP) cacerts.empty $(ptmp)/$(zname)/cacerts
	chmod 644 $(ptmp)/$(zname)/cacerts

build_rpm: specfile = SPECS/$(zspec)
build_rpm:
	./import-cacerts -f certdata.txt.20151201 -o $(ptmp)
	$(CD) $(ptmp)/$(zname)/rpm && \
	$(replace-pkginfo) $(specfile) && \
	$(replace-pathinfo) $(specfile) && \
	$(MKDIR) BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(PKG_BUILD) $(specfile)

build_deb:
	./import-cacerts -f certdata.txt.20151201 -o $(ptmp)
	$(CD) $(ptmp)/$(zname) && \
	$(replace-pkginfo) debian/changelog && \
	$(replace-pathinfo) debian/rules && \
	$(PKG_BUILD)

clean: pkgrm
	$(generic-clean)
