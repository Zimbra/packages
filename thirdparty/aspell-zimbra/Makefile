PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../package.def

pname_lc := aspell-zimbra
ptmp := $(TMP_DIR)/$(BUILD_PLATFORM)
zname := zimbra-$(pname_lc)
zspec := $(pname_lc).spec

.PHONY: all clean build pkgadd pkgrm setup

all: clean build pkgrm1

build: setup pkgadd build_$(PKG_EXT)

setup:
	$(MKDIR) $(ptmp)
	$(CP) -prf $(zname) $(ptmp)

pkgadd:
	$(PKG_EXTRACT) zimbra-aspell-en

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base

build_rpm: specfile = SPECS/$(zspec)
build_rpm:
	$(CD) $(ptmp)/$(zname)/rpm && \
	$(replace-pkginfo) $(specfile) && \
	$(replace-pathinfo) $(specfile) && \
	$(MKDIR) BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(PKG_BUILD) $(specfile)

build_deb:
	$(CD) $(ptmp)/$(zname) && \
	$(replace-pkginfo) debian/changelog && \
	$(replace-pathinfo) debian/rules && \
	$(CHMOD) u+w debian/control && \
	$(PKG_BUILD)

clean:
	$(generic-clean)
