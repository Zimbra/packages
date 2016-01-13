PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(PREPFLOG_VERSION)

.PHONY: all getsrc setup build clean

all: clean getsrc build

files = $(wildcard src/prepflog-$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget http://github.com/johnfawcett/prepflog/archive/$(pvers).tar.gz && \
	mv $(pvers).tar.gz prepflog-$(pvers).tar.gz \
	)
else
	@echo "Already have the source, skipping download"
endif

setup:
	$(generic-setup)

build: setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-prepflog/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(replace-pkginfo) SPECS/prepflog.spec && \
	$(replace-pathinfo) SPECS/prepflog.spec && \
	cp ../../../../src/prepflog-$(pvers).tar.gz SOURCES/zimbra-prepflog-$(pvers).tar.gz && \
	$(PKG_BUILD) SPECS/prepflog.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
	$(replace-pkginfo) zimbra-prepflog/debian/changelog && \
	$(replace-pathinfo) zimbra-prepflog/debian/rules && \
	cp ../../src/prepflog-$(pvers).tar.gz zimbra-prepflog_$(pvers).orig.tar.gz && \
	tar xfz zimbra-prepflog_$(pvers).orig.tar.gz --strip-components=1  -C zimbra-prepflog && \
	cd zimbra-prepflog && \
	chmod u+w debian/control && \
	$(PKG_BUILD) \
	)
endif

clean:
	$(generic-clean)
