PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(SOCKET_LINUX)

.PHONY: all getsrc setup build pkgadd pkgrm clean

all: clean getsrc build pkgrm1

files = $(wildcard src/Socket-Linux-$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q http://search.cpan.org/CPAN/authors/id/S/SA/SALVA/Socket-Linux-$(pvers).tar.gz \
	)
else
	@echo "Already have the source, skipping download"
endif

pkgadd:
	$(PKG_EXTRACT) zimbra-perl-base

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base

setup:
	$(generic-setup)

build: setup pkgadd
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-perl-socket-linux/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/socket-linux.spec && \
 	$(replace-pathinfo) SPECS/socket-linux.spec && \
	cp ../../../../src/Socket-Linux-$(pvers).tar.gz SOURCES/zimbra-perl-socket-linux-$(pvers).tar.gz && \
 	$(PKG_BUILD) SPECS/socket-linux.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-perl-socket-linux/debian/changelog && \
 	$(replace-pathinfo) zimbra-perl-socket-linux/debian/rules && \
	cp ../../src/Socket-Linux-$(pvers).tar.gz zimbra-perl-socket-linux_$(pvers).orig.tar.gz && \
	tar xfz zimbra-perl-socket-linux_$(pvers).orig.tar.gz --strip-components=1  -C zimbra-perl-socket-linux && \
	cd zimbra-perl-socket-linux && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	$(generic-clean)
