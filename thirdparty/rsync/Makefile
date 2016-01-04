PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../package.def

pvers := $(RSYNC_VERSION)

.PHONY: all getsrc setup build clean

all: clean getsrc build

files = $(wildcard src/rsync-$(RSYNC_VERSION).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q https://download.samba.org/pub/rsync/rsync-$(RSYNC_VERSION).tar.gz \
	)
else
	@echo "Already have the source, skipping download"
endif

setup:
	$(generic-setup)

build: setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-rsync/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/rsync.spec && \
 	$(replace-pathinfo) SPECS/rsync.spec && \
	cp ../../../../src/rsync-$(RSYNC_VERSION).tar.gz SOURCES/zimbra-rsync-$(RSYNC_VERSION).tar.gz && \
 	$(PKG_BUILD) SPECS/rsync.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-rsync/debian/changelog && \
 	$(replace-pathinfo) zimbra-rsync/debian/rules && \
	cp ../../src/rsync-$(RSYNC_VERSION).tar.gz zimbra-rsync_$(RSYNC_VERSION).orig.tar.gz && \
	tar xfz zimbra-rsync_$(RSYNC_VERSION).orig.tar.gz --strip-components=1  -C zimbra-rsync && \
	cd zimbra-rsync && \
	$(PKG_BUILD) \
	)
endif

clean:
	$(generic-clean)
