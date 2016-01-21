PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pname_lc := aspell-zimbra
zname := zimbra-$(pname_lc)
zspec := $(pname_lc).spec

.PHONY: all clean build pkgadd pkgrm setup

all: clean build pkgrm1

build: setup pkgadd build_$(PKG_EXT)

setup:
	$(MKDIR) $(PLATFORM_DIR)
	$(CP) -prf $(zname) $(PLATFORM_DIR)

pkgadd:
	$(PKG_EXTRACT) zimbra-aspell-en

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base

build_rpm: specfile = SPECS/$(zspec)
build_rpm:
	$(CD) $(PLATFORM_DIR)/$(zname)/rpm && \
	$(replace-pkginfo) $(specfile) && \
	$(replace-pathinfo) $(specfile) && \
	$(MKDIR) BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(PKG_BUILD) $(specfile)

build_deb:
	$(CD) $(PLATFORM_DIR)/$(zname) && \
	$(replace-pkginfo) debian/changelog && \
	$(replace-pathinfo) debian/rules && \
	$(PKG_BUILD)

clean:
	$(generic-clean)
