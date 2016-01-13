PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(SENDMAIL_VERSION)

.PHONY: all getsrc setup build clean

all: clean getsrc build

files = $(wildcard src/sendmail.$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q ftp://ftp.sendmail.org/pub/sendmail/sendmail.$(pvers).tar.gz \
	)
else
	@echo "Already have the source, skipping download"
endif

setup:
	$(generic-setup)

build: setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-libmilter/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/libmilter.spec && \
 	$(replace-pathinfo) SPECS/libmilter.spec && \
	cp ../../../../src/sendmail.$(pvers).tar.gz SOURCES/zimbra-libmilter-$(pvers).tar.gz && \
        cp ../../../../patches/ipv6.patch SOURCES/ipv6.patch && \
 	$(PKG_BUILD) SPECS/libmilter.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-libmilter/debian/changelog && \
 	$(replace-pathinfo) zimbra-libmilter/debian/rules && \
	cp ../../src/sendmail.$(pvers).tar.gz zimbra-libmilter_$(pvers).orig.tar.gz && \
        cp ../../patches/ipv6.patch zimbra-libmilter/debian/patches && \
	tar xfz zimbra-libmilter_$(pvers).orig.tar.gz --strip-components=1 -C zimbra-libmilter && \
	cd zimbra-libmilter && \
	chmod u+w debian/control && \
	$(PKG_BUILD) \
	)
endif

clean:
	$(generic-clean)
