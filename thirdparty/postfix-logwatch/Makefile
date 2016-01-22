PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(LOGWATCH_POSTFIX)

.PHONY: all getsrc setup build clean

all: clean getsrc build

files = $(wildcard src/postfix-logwatch-$(pvers).tgz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q http://sourceforge.net/projects/logreporters/files/postfix-logwatch-$(pvers).tgz \
	)
else
	@echo "Already have the source, skipping download"
endif

setup:
	$(generic-setup)

build: setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-postfix-logwatch/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/postfix-logwatch.spec && \
 	$(replace-pathinfo) SPECS/postfix-logwatch.spec && \
	cp ../../../../src/postfix-logwatch-$(pvers).tgz SOURCES/zimbra-postfix-logwatch-$(pvers).tgz && \
 	$(PKG_BUILD) SPECS/postfix-logwatch.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-postfix-logwatch/debian/changelog && \
 	$(replace-pathinfo) zimbra-postfix-logwatch/debian/rules && \
	cp ../../src/postfix-logwatch-$(pvers).tgz zimbra-postfix-logwatch_$(pvers).orig.tar.gz && \
	tar xfz zimbra-postfix-logwatch_$(pvers).orig.tar.gz --strip-components=1  -C zimbra-postfix-logwatch && \
	cd zimbra-postfix-logwatch && \
	$(PKG_BUILD) \
	)
endif

clean:
	$(generic-clean)
