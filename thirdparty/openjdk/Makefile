PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../package.def

pvers := $(JDK_VERSION)

# Work around Debian bug 742864 (See comment 99)
# There is a bug in binutils with this release
ifeq ($(BUILD_PLATFORM), UBUNTU12_64)
UB_REPLACE	:= nostrip
endif

.PHONY: all getsrc setup build clean pkgadd pkgrm

all: clean getsrc build pkgrm1

files = $(wildcard src/openjdk-$(pvers).tgz)

getsrc: export HGFOREST_REDIRECT=getsource.out
getsrc:
	mkdir -p src
ifeq ($(files),)
	(echo "Obtaining source for openjdk.  This may take some time." && \
	cd src && \
	mkdir tmp && \
	cd tmp && \
	hg clone -r $(JDK_TAG) http://hg.openjdk.java.net/jdk8u/jdk$(JDK_SUB_TREE) && \
	cd jdk$(JDK_SUB_TREE) && chmod a+rx get_source.sh && \
	chmod a+rx configure && \
	patch -p1 < ../../../patches/fix-source.patch && \
	echo "Obtaining source for sub modules.  This make take a very long time." && \
	./get_source.sh -r $(JDK_TAG) || true && \
	cd .. && \
	mv jdk$(JDK_SUB_TREE) openjdk-$(pvers) && \
	( cd openjdk-$(pvers) && find . -name ".hg*" | xargs rm -rf ) && \
	tar cfz openjdk-$(pvers).tgz openjdk-$(pvers) && \
	mv openjdk-$(pvers).tgz .. && \
	cd .. && \
	rm -rf tmp \
	)
else
	@echo "Already have the source, skipping download"
endif

pkgadd:
ifeq ($(PKG_EXT), rpm)
	$(PKG_EXTRACT) libX11-devel libXau-devel libXext-devel \
	libXfixes-devel libXtst-devel libXi-devel libxcb-devel \
	xorg-x11-proto-devel libICE-devel libSM-devel libXt \
	libXt-devel libXrender-devel keyutils-libs-devel \
	krb5-devel libcom_err-devel libselinux-devel \
	libsepol-devel openssl-devel cups-devel freetype-devel \
	alsa-lib-devel java-1.7.0-openjdk-devel
else
	$(PKG_EXTRACT) libx11-dev x11proto-xext-dev libxext-dev \
	x11proto-render-dev libxrender-dev libxfixes-dev libxi-dev \
	x11proto-fixes-dev x11proto-record-dev libxtst-dev libxt-dev \
	openjdk-7-jdk libcups2-dev libfreetype6-dev libasound2-dev \
	ccache
endif

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

build: setup pkgadd
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-openjdk/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/openjdk.spec && \
	perl -pi -e 's/JDK_BUILD/$(JDK_BUILD)/; s/JDK_UPDATE/$(JDK_UPDATE)/' SPECS/openjdk.spec && \
 	$(replace-pathinfo) SPECS/openjdk.spec && \
	cp ../../../../src/openjdk-$(pvers).tgz SOURCES/zimbra-openjdk-$(pvers).tgz && \
 	$(PKG_BUILD) SPECS/openjdk.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-openjdk/debian/changelog && \
	perl -pi -e 's/JDK_BUILD/$(JDK_BUILD)/; s/JDK_UPDATE/$(JDK_UPDATE)/' zimbra-openjdk/debian/rules && \
	perl -pi -e 's/DEB_BUILD_OPTIONS=nocheck/DEB_BUILD_OPTIONS=nocheck $(UB_REPLACE)/' zimbra-openjdk/debian/rules && \
 	$(replace-pathinfo) zimbra-openjdk/debian/rules && \
	cp ../../src/openjdk-$(pvers).tgz zimbra-openjdk_$(pvers).orig.tar.gz && \
	tar xfz zimbra-openjdk_$(pvers).orig.tar.gz --strip-components=1  -C zimbra-openjdk && \
	cd zimbra-openjdk && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
