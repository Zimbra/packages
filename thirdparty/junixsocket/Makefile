PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

export JAVA_HOME:=/opt/zimbra/common
export PATH:=/opt/zimbra/common/bin:${PATH}
pvers := $(JUNIXSOCKET_VERSION)
pname := junixsocket
pfile := $(pname)-$(pvers).tgz
psrc_file := $(SRC_DIR)/$(pfile)
zname := zimbra-$(pname)
zspec := $(pname).spec

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: getsrc build pkgrm1


getsrc:
	mkdir -p $(SRC_DIR)
	(cd $(SRC_DIR) && \
	git clone https://github.com/kohlschutter/junixsocket.git $(pname) >/dev/null 2>&1 && \
	cd $(pname) && \
        git reset --hard junixsocket-parent-$(JUNIXSOCKET_VERSION) >/dev/null 2>&1 && \
        rm -rf .git .gitignore && \
	cd .. && \
	mv $(pname) $(pname)-$(pvers) && \
	tar cfz $(pfile) $(pname)-$(pvers) && \
	rm -rf $(pname)-$(pvers) \
	)

pkgadd:
	$(PKG_EXTRACT) zimbra-base zimbra-maven zimbra-openjdk-cacerts

pkgrm:  pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base zimbra-maven zimbra-openjdk-cacerts

setup:
	$(generic-setup)

build: pkgadd setup build_$(PKG_EXT)
build_rpm: specfile = SPECS/$(zspec)
build_rpm:
	$(CD) $(PLATFORM_DIR)/$(zname)/rpm && \
	$(replace-pkginfo) $(specfile) && \
	$(replace-pathinfo) $(specfile) && \
	$(MKDIR) BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(CP) $(psrc_file) SOURCES/$(zname)-$(pvers).tgz && \
	$(PKG_BUILD) $(specfile)

build_deb: z_tgz = $(zname)_$(pvers).orig.tar.gz
build_deb: z_shlibs = $(subst $(zname)/,,$(wildcard $(zname)/debian/z*.shlibs))
build_deb:
	$(CD) $(PLATFORM_DIR)/$(zname) && \
	$(replace-pkginfo) debian/changelog $(z_shlibs) && \
	$(replace-pathinfo) debian/rules && \
	$(CP) $(psrc_file) ../$(z_tgz) && \
	$(TAR) xfz ../$(z_tgz) --strip-components=1 && \
	$(PKG_BUILD)

clean: pkgrm
	$(generic-clean)
