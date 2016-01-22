PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(LOGWATCH_AMAVIS)

.PHONY: all getsrc setup build clean

all: clean getsrc build

files = $(wildcard src/amavis-logwatch-$(pvers).tgz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q http://sourceforge.net/projects/logreporters/files/amavis-logwatch-$(pvers).tgz \
	)
else
	@echo "Already have the source, skipping download"
endif

setup:
	$(generic-setup)

build: setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-amavis-logwatch/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/amavis-logwatch.spec && \
 	$(replace-pathinfo) SPECS/amavis-logwatch.spec && \
	cp ../../../../src/amavis-logwatch-$(pvers).tgz SOURCES/zimbra-amavis-logwatch-$(pvers).tgz && \
 	$(PKG_BUILD) SPECS/amavis-logwatch.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-amavis-logwatch/debian/changelog && \
 	$(replace-pathinfo) zimbra-amavis-logwatch/debian/rules && \
	cp ../../src/amavis-logwatch-$(pvers).tgz zimbra-amavis-logwatch_$(pvers).orig.tar.gz && \
	tar xfz zimbra-amavis-logwatch_$(pvers).orig.tar.gz --strip-components=1  -C zimbra-amavis-logwatch && \
	cd zimbra-amavis-logwatch && \
	$(PKG_BUILD) \
	)
endif

clean:
	$(generic-clean)
