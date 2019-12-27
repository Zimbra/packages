PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(JDK_VERSION)
pname := openjdk
pfile := $(pname)-$(pvers).tgz
psrc_file := $(SRC_DIR)/$(pfile)
zname := zimbra-$(pname)
zspec := $(pname).spec

openjdk = $(openjdk.$(BUILD_PLATFORM))
openjdk-purge = $(openjdk-purge.$(BUILD_PLATFORM))

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
	patch -p1 < $(PKG_ROOT)/patches/fix-source.patch && \
	echo "Obtaining source for sub modules.  This make take a very long time." && \
	./get_source.sh -r $(JDK_TAG) || true && \
	cd .. && \
	mv jdk$(JDK_SUB_TREE) $(pname)-$(pvers) && \
	( cd $(pname)-$(pvers) && find . -name ".hg*" | xargs rm -rf ) && \
	tar cfz $(pfile) $(pname)-$(pvers) && \
	mv $(pfile) .. && \
	cd .. && \
	rm -rf tmp && \
	wget http://ftp.de.debian.org/debian/pool/main/o/openjdk-7/openjdk-7-jdk_7u161-2.6.12-1_amd64.deb && \
        wget http://ftp.de.debian.org/debian/pool/main/o/openjdk-7/openjdk-7-jre_7u161-2.6.12-1_amd64.deb && \
        wget http://ftp.de.debian.org/debian/pool/main/o/openjdk-7/openjdk-7-jre-headless_7u161-2.6.12-1_amd64.deb && \
        wget http://ftp.de.debian.org/debian/pool/main/libj/libjpeg-turbo/libjpeg62-turbo_1.5.2-2+b1_amd64.deb && \
        dpkg -i openjdk-7-* libjpeg62-turbo* \
	)

pkgadd:
	$(PKG_EXTRACT) $(openjdk)

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) $(openjdk-purge)

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
	$(CP) $(psrc_file) SOURCES/$(zname)-$(pvers).tgz && \
	$(PKG_BUILD) $(specfile)

build_deb: z_tgz = $(zname)_$(pvers).orig.tar.gz
build_deb: z_shlibs = $(subst $(zname)/,,$(wildcard $(zname)/debian/z*.shlibs))
build_deb:
	$(CD) $(PLATFORM_DIR)/$(zname) && \
	$(replace-pkginfo) debian/changelog $(z_shlibs) && \
	perl -pi -e 's/JDK_BUILD/$(JDK_BUILD)/; s/JDK_UPDATE/$(JDK_UPDATE)/' debian/rules && \
	perl -pi -e 's/DEB_BUILD_OPTIONS=nocheck/DEB_BUILD_OPTIONS=nocheck $(UB_REPLACE)/' debian/rules && \
	$(replace-pathinfo) debian/rules && \
	$(CP) $(psrc_file) ../$(z_tgz) && \
	$(TAR) xfz ../$(z_tgz) --strip-components=1 && \
	$(PKG_BUILD)

clean: pkgrm
	$(generic-clean)
