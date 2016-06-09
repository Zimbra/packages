PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../package.def

pname_lc := spamassassin-rules
ptmp := $(TMP_DIR)/$(BUILD_PLATFORM)
zname := zimbra-$(pname_lc)
zspec := $(pname_lc).spec

.PHONY: all clean build pkgadd pkgrm setup

all: clean build pkgrm1

build: setup pkgadd build_$(PKG_EXT)

pkgadd:
	$(PKG_EXTRACT) zimbra-perl-mail-spamassassin

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base

setup:
	$(MKDIR) $(ptmp)
	$(CP) -prf $(zname) $(ptmp)

build_rpm: specfile = SPECS/$(zspec)
build_rpm:
	/opt/zimbra/common/bin/sa-update --nogpg --updatedir=$(ptmp)/rules && \
	$(CD) $(ptmp)/$(zname)/rpm && \
	$(replace-pkginfo) $(specfile) && \
	$(replace-pathinfo) $(specfile) && \
	$(MKDIR) BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(PKG_BUILD) $(specfile)

build_deb:
	/opt/zimbra/common/bin/sa-update --nogpg --updatedir=$(ptmp)/$(zname)/rules && \
	$(CD) $(ptmp)/$(zname) && \
	$(replace-pkginfo) debian/changelog && \
	$(replace-pathinfo) debian/rules && \
	$(PKG_BUILD)

clean: pkgrm
	$(generic-clean)
