PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pname_lc := openjdk-cacerts
zname := zimbra-$(pname_lc)
zspec := $(pname_lc).spec

.PHONY: all clean build pkgadd getsrc pkgrm setup

all: clean build pkgrm1

build: setup pkgadd getsrc build_$(PKG_EXT)

pkgadd:
	$(PKG_EXTRACT) zimbra-openjdk

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base

setup:
	$(generic-setup)
	$(CP) cacerts.empty $(PLATFORM_DIR)/$(zname)/cacerts
	chmod 644 $(PLATFORM_DIR)/$(zname)/cacerts

getsrc:
	wget -O $(PLATFORM_DIR)/certdata.txt https://hg.mozilla.org/mozilla-central/raw-file/tip/security/nss/lib/ckfw/builtins/certdata.txt

build_rpm: specfile = SPECS/$(zspec)
build_rpm:
	./import-cacerts -f $(PLATFORM_DIR)/certdata.txt -o $(PLATFORM_DIR)
	$(CD) $(PLATFORM_DIR)/$(zname)/rpm && \
	$(replace-pkginfo) $(specfile) && \
	$(replace-pathinfo) $(specfile) && \
	$(MKDIR) BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(PKG_BUILD) $(specfile)

build_deb:
	./import-cacerts -f $(PLATFORM_DIR)/certdata.txt -o $(PLATFORM_DIR)
	$(CD) $(PLATFORM_DIR)/$(zname) && \
	$(replace-pkginfo) debian/changelog && \
	$(replace-pathinfo) debian/rules && \
	$(PKG_BUILD)

clean: pkgrm
	$(generic-clean)
