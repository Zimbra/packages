PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(JDK_VERSION)
pname := openjdk
pfile := $(pname)-$(pvers).tgz
psrc_file := $(SRC_DIR)/$(pfile)
zname := zimbra-$(pname)
zspec := $(pname).spec

# Work around Debian bug 742864 (See comment 99)
# There is a bug in binutils with this release
ifeq ($(BUILD_PLATFORM), UBUNTU12_64)
UB_REPLACE	:= nostrip
endif

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

getsrc: export HGFOREST_REDIRECT=getsource.out
getsrc:
	mkdir -p $(SRC_DIR)
	(echo "Obtaining source for openjdk.  This may take some time." && \
	cd $(SRC_DIR) && \
	mkdir tmp && \
	cd tmp && \
	hg clone -r $(JDK_TAG) http://hg.openjdk.java.net/jdk8u/jdk$(JDK_SUB_TREE) && \
	cd jdk$(JDK_SUB_TREE) && chmod a+rx get_source.sh && \
	chmod a+rx configure && \
	patch -p1 < ../../../../../patches/fix-source.patch && \
	echo "Obtaining source for sub modules.  This make take a very long time." && \
	./get_source.sh -r $(JDK_TAG) || true && \
	cd .. && \
	mv jdk$(JDK_SUB_TREE) $(pname)-$(pvers) && \
	( cd $(pname)-$(pvers) && find . -name ".hg*" | xargs rm -rf ) && \
	tar cfz $(pfile) $(pname)-$(pvers) && \
	mv $(pfile) .. && \
	cd .. && \
	rm -rf tmp \
	)

pkgadd: pkgadd_$(PKG_EXT)

pkgadd_rpm:
	$(PKG_EXTRACT) libX11-devel libXau-devel libXext-devel \
	libXfixes-devel libXtst-devel libXi-devel libxcb-devel \
	xorg-x11-proto-devel libICE-devel libSM-devel libXt \
	libXt-devel libXrender-devel keyutils-libs-devel \
	krb5-devel libcom_err-devel libselinux-devel \
	libsepol-devel openssl-devel cups-devel freetype-devel \
	alsa-lib-devel java-1.7.0-openjdk-devel

pkgadd_deb:
	$(PKG_EXTRACT) libx11-dev x11proto-xext-dev libxext-dev \
	x11proto-render-dev libxrender-dev libxfixes-dev libxi-dev \
	x11proto-fixes-dev x11proto-record-dev libxtst-dev libxt-dev \
	openjdk-7-jdk libcups2-dev libfreetype6-dev libasound2-dev \
	ccache

pkgrm: pkgrm%

pkgrm%:
ifeq ($(PKG_EXT), rpm)
	$(PKG_PURGE) alsa-lib-devel freetype-devel cups-devel openssl-devel \
	libsepol-devel libselinux-devel libcom_err-devel krb5-devel keyutils-libs-devel \
	libXrender-devel libXt-devel libXt libSM-devel libICE-devel xorg-x11-proto-devel \
	libxcb-devel libXi-devel libXtst-devel libXfixes-devel libXext-devel libXau-devel \
	libX11-devel java-1.7.0-openjdk
else
	$(PKG_PURGE) libxt-dev libxtst-dev libxrender-dev libxext-dev libx11-dev \
	libcups2-dev libfreetype6-dev libasound2-dev openjdk-7-jdk ccache
	sudo apt-get -y autoremove
endif
ifeq ($(BUILD_PLATFORM), RHEL7_64)
	$(PKG_PURGE) libverto-devel
endif

setup:
	$(generic-setup)

build: setup pkgadd build_$(PKG_EXT)

build_rpm: specfile = SPECS/$(zspec)
build_rpm:
	$(CD) $(PLATFORM_DIR)/$(zname)/rpm && \
	$(replace-pkginfo) $(specfile) && \
	perl -pi -e 's/JDK_BUILD/$(JDK_BUILD)/; s/JDK_UPDATE/$(JDK_UPDATE)/' $(specfile) && \
	$(replace-pathinfo) $(specfile) && \
	$(MKDIR) BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(CP) $(PKG_ROOT)/$(psrc_file) SOURCES/$(zname)-$(pvers).tgz && \
	$(PKG_BUILD) $(specfile)

build_deb: z_tgz = $(zname)_$(pvers).orig.tar.gz
build_deb: z_shlibs = $(subst $(zname)/,,$(wildcard $(zname)/debian/z*.shlibs))
build_deb:
	$(CD) $(PLATFORM_DIR)/$(zname) && \
	$(replace-pkginfo) debian/changelog $(z_shlibs) && \
	perl -pi -e 's/JDK_BUILD/$(JDK_BUILD)/; s/JDK_UPDATE/$(JDK_UPDATE)/' debian/rules && \
	perl -pi -e 's/DEB_BUILD_OPTIONS=nocheck/DEB_BUILD_OPTIONS=nocheck $(UB_REPLACE)/' debian/rules && \
	$(replace-pathinfo) debian/rules && \
	$(CP) $(PKG_ROOT)/$(psrc_file) ../$(z_tgz) && \
	$(TAR) xfz ../$(z_tgz) --strip-components=1 && \
	$(PKG_BUILD)

clean: pkgrm
	$(generic-clean)
