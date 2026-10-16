PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(CLUEBRINGER_VERSION).$(CLUEBRINGER_GIT)
pname := cluebringer
pfile := $(pname)-$(pvers).tgz
psrc_file := $(SRC_DIR)/$(pfile)
zname := zimbra-$(pname)
zspec := $(pname).spec

# The original upstream (gitlab.devlabs.linuxassist.net) no longer hosts git.
# Set CLUEBRINGER_REPO (env var or package.def) to a git mirror that contains
# the pinned commit (CLUEBRINGER_GIT) and provides the awitpt submodule via
# ./update-git-modules. The mirrors are tried in order.
cluebringer-repos = $(CLUEBRINGER_REPO) \
	https://gitlab.devlabs.linuxassist.net/policyd/policyd.git

# Optional: set CLUEBRINGER_SRC_URL (env var or package.def) to a prebuilt
# source tarball (same layout as the one generated below) to skip git entirely.

.PHONY: all getsrc setup build clean

all: clean getsrc build

getsrc:
	mkdir -p $(SRC_DIR)
ifneq ($(strip $(CLUEBRINGER_SRC_URL)),)
	cd $(SRC_DIR) && $(WGET) -O $(pfile) $(CLUEBRINGER_SRC_URL)
else
	cd $(SRC_DIR) && \
	rm -rf $(pname) && \
	found=0 && \
	for repo in $(cluebringer-repos); do \
	  rm -rf $(pname); \
	  echo "getsrc: trying $$repo"; \
	  if git clone $$repo $(pname) && (cd $(pname) && git reset --hard $(CLUEBRINGER_GIT)); then found=1; break; fi; \
	done; \
	if [ "$$found" != 1 ]; then \
	  echo "ERROR: no git mirror provides commit $(CLUEBRINGER_GIT); set CLUEBRINGER_SRC_URL to a source tarball" >&2; \
	  exit 1; \
	fi && \
	cd $(pname) && \
	./update-git-modules && \
	{ test -d awitpt/awitpt || { echo "ERROR: awitpt submodule missing" >&2; exit 1; }; } && \
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
	rm -rf $(pname)-$(pvers)
endif

setup:
	$(generic-setup)

build: setup build_$(PKG_EXT)
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

clean:
	$(generic-clean)
