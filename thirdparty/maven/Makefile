PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def
MAVEN_VERSION := 3.3.9
pvers := $(MAVEN_VERSION)
pname := maven
pfile := apache-$(pname)-$(pvers)-src.tar.gz
psrc_file := $(SRC_DIR)/$(pfile)
purl := http://archive.apache.org/dist/maven/maven-3/$(pvers)/source/$(pfile)
zname := zimbra-$(pname)
zspec := $(pname).spec
export M2_HOME := build

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

# $(@D) == directory part of the target
getsrc: $(psrc_file)
$(psrc_file):
	$(MKDIR) $(@D) && $(CD) $(@D) && $(WGET) $(purl)

pkgadd: pkgadd_$(PKG_EXT)

pkgadd_rpm:
	$(PKG_EXTRACT) zimbra-openjdk ant

pkgadd_deb:
	$(PKG_EXTRACT) ant ant-optional zimbra-openjdk zimbra-openjdk-cacerts java-common libsctp1 \
	libxerces2-java libxml-commons-external-java libxml-commons-resolver1.1-java \
	lksctp-tools tzdata-java

pkgrm: pkgrm%

pkgrm%:
ifeq ($(PKG_EXT), rpm)
	$(PKG_PURGE) zimbra-openjdk ant
else
	$(PKG_PURGE) ant-optional zimbra-openjdk zimbra-openjdk-cacerts java-common libsctp1 \
	libxerces2-java libxml-commons-external-java libxml-commons-resolver1.1-java \
	lksctp-tools tzdata-java
endif

setup:
	$(generic-setup)

build: setup pkgadd build_$(PKG_EXT)

build_rpm: specfile = SPECS/$(zspec)
build_rpm:
	$(CD) $(PLATFORM_DIR)/$(zname)/rpm && \
	$(replace-pkginfo) $(specfile) && \
	$(replace-pathinfo) $(specfile) && \
	$(MKDIR) BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(CP) $(PKG_ROOT)/$(psrc_file) SOURCES/$(zname)-$(pvers).tar.gz && \
	$(CP) $(PKG_ROOT)/patches/*.patch SOURCES/ && \
	$(PKG_BUILD) $(specfile)

build_deb: z_tgz = $(zname)_$(pvers).orig.tar.gz
build_deb: z_shlibs = $(subst $(zname)/,,$(wildcard $(zname)/debian/z*.shlibs))
build_deb:
	$(CD) $(PLATFORM_DIR)/$(zname) && \
	$(replace-pkginfo) debian/changelog $(z_shlibs) && \
	$(replace-pathinfo) debian/rules && \
	$(CP) $(PKG_ROOT)/$(psrc_file) ../$(z_tgz) && \
	$(CP) $(PKG_ROOT)/patches/*.patch debian/patches/ && \
	$(TAR) xfz ../$(z_tgz) --strip-components=1 && \
	$(PKG_BUILD)

clean: pkgrm
	$(generic-clean)
