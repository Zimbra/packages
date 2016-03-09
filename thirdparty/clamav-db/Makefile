PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pname_lc := clamav-db
zname := zimbra-$(pname_lc)
zspec := $(pname_lc).spec
bcvd := bytecode.cvd
dcvd := daily.cvd
mcvd := main.cvd
bcvd_file := $(SRC_DIR)/$(bcvd)
dcvd_file := $(SRC_DIR)/$(dcvd)
mcvd_file := $(SRC_DIR)/$(mcvd)
burl := http://database.clamav.net/$(bcvd)
durl := http://database.clamav.net/$(dcvd)
murl := http://database.clamav.net/$(mcvd)

.PHONY: all getsrc clean build setup

all: clean getsrc build

# $(@D) == directory part of the target
getsrc: $(mcvd_file) $(dcvd_file) $(bcvd_file)
$(bcvd_file):
	$(MKDIR) $(@D) && $(CD) $(@D) && $(WGET) $(burl)

$(dcvd_file):
	$(MKDIR) $(@D) && $(CD) $(@D) && $(WGET) $(durl)

$(mcvd_file):
	$(MKDIR) $(@D) && $(CD) $(@D) && $(WGET) $(murl)

build: setup build_$(PKG_EXT)

setup:
	$(generic-setup)

build_rpm: specfile = SPECS/$(zspec)
build_rpm:
	$(CD) $(PLATFORM_DIR)/$(zname)/rpm && \
	$(replace-pkginfo) $(specfile) && \
	$(replace-pathinfo) $(specfile) && \
	$(MKDIR) BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(PKG_BUILD) $(specfile)

build_deb:
	$(CD) $(PLATFORM_DIR)/$(zname) && \
	$(replace-pkginfo) debian/changelog && \
	$(replace-pathinfo) debian/rules && \
	$(PKG_BUILD)

clean:
	$(generic-clean)
