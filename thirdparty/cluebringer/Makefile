PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(CLUEBRINGER_VERSION).$(CLUEBRINGER_GIT)
pname := cluebringer
pfile := $(pname)-$(pvers).tgz
psrc_file := $(SRC_DIR)/$(pfile)
zname := zimbra-$(pname)
zspec := $(pname).spec

.PHONY: all getsrc setup build clean

all: clean getsrc build

getsrc:
	mkdir -p $(SRC_DIR)
	(cd $(SRC_DIR) && \
	git clone https://gitlab.devlabs.linuxassist.net/policyd/policyd.git $(pname) >/dev/null 2>&1 && \
	cd $(pname) && \
	git reset --hard $(CLUEBRINGER_GIT) >/dev/null 2>&1 && \
	./update-git-modules >/dev/null 2>&1 && \
	rm -rf .git awitpt/.git && \
	rm -rf awitpt/CPAN* awitpt/doxygen awitpt/SOAP && \
	mv -f awitpt/awitpt/db awitpt/ && \
	mv -f awitpt/awitpt/cache.pm awitpt/ && \
	mv -f awitpt/awitpt/netip.pm awitpt/ && \
	rmdir awitpt/awitpt && \
	rm -rf debian && \
	rm -f $(pname).spec && \
	cd .. && \
	mv $(pname) $(pname)-$(pvers) && \
	tar cfz $(pfile) $(pname)-$(pvers) && \
	rm -rf $(pname)-$(pvers) \
	)

setup:
	$(generic-setup)

build: setup build_$(PKG_EXT)
build_rpm: specfile = SPECS/$(zspec)
build_rpm:
	$(CD) $(PLATFORM_DIR)/$(zname)/rpm && \
	$(replace-pkginfo) $(specfile) && \
	$(replace-pathinfo) $(specfile) && \
	$(MKDIR) BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(CP) $(PKG_ROOT)/$(psrc_file) SOURCES/$(zname)-$(pvers).tar.gz && \
	$(PKG_BUILD) $(specfile)

build_deb: z_tgz = $(zname)_$(pvers).orig.tar.gz
build_deb: z_shlibs = $(subst $(zname)/,,$(wildcard $(zname)/debian/z*.shlibs))
build_deb:
	$(CD) $(PLATFORM_DIR)/$(zname) && \
	$(replace-pkginfo) debian/changelog $(z_shlibs) && \
	$(replace-pathinfo) debian/rules && \
	$(CP) $(PKG_ROOT)/$(psrc_file) ../$(z_tgz) && \
	$(TAR) xfz ../$(z_tgz) --strip-components=1 && \
	$(PKG_BUILD)

clean:
	$(generic-clean)
