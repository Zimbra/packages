PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(JDK_VERSION)
pname := openjdk
pfile := $(pname)-$(pvers)_linux-x64_bin.tar.gz
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
	(echo "Downloading openjdk binaries.  This may take some time." && \
	cd $(SRC_DIR) && \
	wget https://files.zimbra.com/downloads/openjdk/$(pfile) && \
	tar xvzf $(pfile) && \
	mv jdk-$(pvers) openjdk-$(pvers)-zimbra && \
	tar -czf ../openjdk-$(pvers)-zimbra.tgz  openjdk-$(pvers)-zimbra )
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
	$(TAR) xfz ../$(z_tgz)  && \
	($(PKG_BUILD) -b)

clean: pkgrm
	$(generic-clean)
