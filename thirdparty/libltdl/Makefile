PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(LIBTOOL_VERSION)

.PHONY: all getsrc setup build clean

all: clean getsrc build

files = $(wildcard src/libtool-$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q http://reflection.oss.ou.edu/gnu/gnu/libtool/libtool-$(pvers).tar.gz \
	)
else
	@echo "Already have the source, skipping download"
endif

setup:
	$(generic-setup)

build: setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-libltdl/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(replace-pkginfo) SPECS/libltdl.spec && \
	$(replace-pathinfo) SPECS/libltdl.spec && \
	cp ../../../../src/libtool-$(pvers).tar.gz SOURCES/zimbra-libltdl-$(pvers).tar.gz && \
	$(PKG_BUILD) SPECS/libltdl.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
	$(replace-pkginfo) zimbra-libltdl/debian/changelog zimbra-libltdl/debian/zimbra-libltdl-lib.shlibs && \
	$(replace-pathinfo) zimbra-libltdl/debian/rules && \
	cp ../../src/libtool-$(pvers).tar.gz zimbra-libltdl_$(pvers).orig.tar.gz && \
	tar xfz zimbra-libltdl_$(pvers).orig.tar.gz --strip-components=1 -C zimbra-libltdl && \
	cd zimbra-libltdl && \
	chmod u+w debian/control && \
	$(PKG_BUILD) \
	)
endif

clean:
	$(generic-clean)
