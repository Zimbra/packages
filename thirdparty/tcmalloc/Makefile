PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../package.def

pvers := $(TCMALLOC_VERSION)

.PHONY: all getsrc setup build clean

all: clean getsrc build

files = $(wildcard src/gperftools-$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q https://github.com/gperftools/gperftools/releases/download/gperftools-$(pvers)/gperftools-$(pvers).tar.gz \
	)
else
	@echo "Already have the source, skipping download"
endif

setup:
	$(generic-setup)

build: setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-tcmalloc/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/tcmalloc.spec && \
 	$(replace-pathinfo) SPECS/tcmalloc.spec && \
	cp ../../../../src/gperftools-$(pvers).tar.gz SOURCES/zimbra-tcmalloc-$(pvers).tar.gz && \
 	$(PKG_BUILD) SPECS/tcmalloc.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-tcmalloc/debian/changelog zimbra-tcmalloc/debian/zimbra-tcmalloc-lib.shlibs && \
 	$(replace-pathinfo) zimbra-tcmalloc/debian/rules && \
	cp ../../src/gperftools-$(pvers).tar.gz zimbra-tcmalloc_$(pvers).orig.tar.gz && \
	tar xfz zimbra-tcmalloc_$(pvers).orig.tar.gz --strip-components=1 -C zimbra-tcmalloc && \
	cd zimbra-tcmalloc && \
	$(PKG_BUILD) \
	)
endif

clean:
	$(generic-clean)
