PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(CLUEBRINGER_VERSION).$(CLUEBRINGER_GIT)
pname := cluebringer
pfile := $(pname)-$(pvers).tgz
psrc_file := $(SRC_DIR)/$(pfile)
zname := zimbra-$(pname)
zspec := $(pname).spec

# Primary and fallback upstream locations (override on the make command line:
#   make CLUEBRINGER_REPO=https://your.mirror/policyd.git)
CLUEBRINGER_REPO      ?= https://gitlab.devlabs.linuxassist.net/policyd/policyd.git
CLUEBRINGER_REPO_ALT  ?= https://github.com/<your-org-or-mirror>/policyd.git
GIT_RETRIES           ?= 3

.PHONY: all getsrc setup build clean

all: clean getsrc build

getsrc:
	mkdir -p $(SRC_DIR)
	@if [ -s "$(psrc_file)" ]; then \
	    echo ">>> Using existing source tarball: $(psrc_file)"; \
	    exit 0; \
	fi; \
	set -e; \
	cd $(SRC_DIR); \
	rm -rf $(pname) $(pname)-$(pvers); \
	cloned=0; \
	for repo in "$(CLUEBRINGER_REPO)" "$(CLUEBRINGER_REPO_ALT)"; do \
	    i=1; \
	    while [ $$i -le $(GIT_RETRIES) ]; do \
	        echo ">>> git clone $$repo (attempt $$i/$(GIT_RETRIES))"; \
	        if git clone "$$repo" $(pname); then cloned=1; break 2; fi; \
	        rm -rf $(pname); \
	        i=$$((i+1)); \
	        sleep 3; \
	    done; \
	done; \
	if [ $$cloned -ne 1 ]; then \
	    echo "ERROR: could not clone cluebringer from any source."; \
	    echo "Place a prepared tarball at $(psrc_file) and re-run make."; \
	    exit 1; \
	fi; \
	cd $(pname); \
	git reset --hard $(CLUEBRINGER_GIT) || { \
	    echo "ERROR: commit $(CLUEBRINGER_GIT) not found in cloned repo"; exit 1; }; \
	./update-git-modules; \
	rm -rf .git awitpt/.git; \
	rm -rf awitpt/CPAN* awitpt/doxygen awitpt/SOAP; \
	mv -f awitpt/awitpt/db awitpt/; \
	mv -f awitpt/awitpt/cache.pm awitpt/; \
	mv -f awitpt/awitpt/netip.pm awitpt/; \
	rmdir awitpt/awitpt; \
	rm -rf debian; \
	rm -f $(pname).spec; \
	cd ..; \
	mv $(pname) $(pname)-$(pvers); \
	tar cfz $(pfile) $(pname)-$(pvers); \
	rm -rf $(pname)-$(pvers)

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
