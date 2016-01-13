PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(PFLOGSUMM_VERSION)

.PHONY: all getsrc setup build clean

all: clean getsrc build

files = $(wildcard src/pflogsumm-$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q http://jimsun.linxnet.com/downloads/pflogsumm-$(PFLOGSUMM_VERSION).tar.gz \
	)
else
	@echo "Already have the source, skipping download"
endif

setup:
	$(generic-setup)

build: setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-pflogsumm/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(replace-pkginfo) SPECS/pflogsumm.spec && \
	$(replace-pathinfo) SPECS/pflogsumm.spec && \
	cp ../../../../src/pflogsumm-$(pvers).tar.gz SOURCES/zimbra-pflogsumm-$(pvers).tar.gz && \
	$(PKG_BUILD) SPECS/pflogsumm.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
	$(replace-pkginfo) zimbra-pflogsumm/debian/changelog && \
	$(replace-pathinfo) zimbra-pflogsumm/debian/rules && \
	cp ../../src/pflogsumm-$(pvers).tar.gz zimbra-pflogsumm_$(pvers).orig.tar.gz && \
	tar xfz zimbra-pflogsumm_$(pvers).orig.tar.gz --strip-components=1  -C zimbra-pflogsumm && \
	cd zimbra-pflogsumm && \
	chmod u+w debian/control && \
	$(PKG_BUILD) \
	)
endif

clean:
	$(generic-clean)
