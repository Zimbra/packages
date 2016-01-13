PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(ALTMIME_VERSION)

.PHONY: all getsrc setup build clean

all: clean getsrc build

files = $(wildcard src/altermime-0.3-dev.tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q http://www.pldaniels.com/altermime/altermime-0.3-dev.tar.gz \
	)
else
	@echo "Already have the source, skipping download"
endif

setup:
	$(generic-setup)

build: setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-altermime/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/altermime.spec && \
 	$(replace-pathinfo) SPECS/altermime.spec && \
	cp ../../../../src/altermime-0.3-dev.tar.gz SOURCES/zimbra-altermime-$(pvers).tar.gz && \
	cp ../../../../patches/*.patch SOURCES/ && \
 	$(PKG_BUILD) SPECS/altermime.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-altermime/debian/changelog && \
 	$(replace-pathinfo) zimbra-altermime/debian/rules && \
	cp ../../src/altermime-0.3-dev.tar.gz zimbra-altermime_$(pvers).orig.tar.gz && \
	cp ../../patches/*.patch zimbra-altermime/debian/patches && \
	tar xfz zimbra-altermime_$(pvers).orig.tar.gz --strip-components=1  -C zimbra-altermime && \
	cd zimbra-altermime && \
	$(PKG_BUILD) \
	)
endif

clean:
	$(generic-clean)
