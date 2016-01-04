PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../package.def

pvers := $(LIBEVENT_VERSION)

.PHONY: all getsrc setup build clean

all: clean getsrc build

files = $(wildcard src/libevent-$(pvers)-stable.tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q https://sourceforge.net/projects/levent/files/libevent/libevent-2.0/libevent-$(pvers)-stable.tar.gz \
	)
else
	@echo "Already have the source, skipping download"
endif

setup:
	mkdir -p tmp/$(BUILD_PLATFORM)
	cp -prf zimbra-libevent tmp/$(BUILD_PLATFORM)

build: setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-libevent/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/libevent.spec && \
 	$(replace-pathinfo) SPECS/libevent.spec && \
	cp ../../../../src/libevent-$(pvers)-stable.tar.gz SOURCES/zimbra-libevent-$(pvers)-stable.tar.gz && \
 	$(PKG_BUILD) SPECS/libevent.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-libevent/debian/changelog zimbra-libevent/debian/zimbra-libevent-lib.shlibs && \
 	$(replace-pathinfo) zimbra-libevent/debian/rules && \
	cp ../../src/libevent-$(pvers)-stable.tar.gz zimbra-libevent_$(pvers).orig.tar.gz && \
	tar xfz zimbra-libevent_$(pvers).orig.tar.gz --strip-components=1 -C zimbra-libevent && \
	cd zimbra-libevent && \
	$(PKG_BUILD) \
	)
endif

clean:
	$(generic-clean)
