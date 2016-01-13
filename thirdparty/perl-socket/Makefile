PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(SOCKET)

.PHONY: all getsrc setup build clean pkgadd pkgrm

PERL_REQ :=

ifeq ($(BUILD_PLATFORM), RHEL6_64)
	PERL_REQ := zimbra-perl-extutils-constant
endif

all: clean getsrc build pkgrm1

files = $(wildcard src/Socket-$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	cd src && \
	wget -q https://cpan.metacpan.org/authors/id/P/PE/PEVANS/Socket-$(pvers).tar.gz
else
	@echo "Already have the source, skipping download"
endif

pkgadd:
	$(PKG_EXTRACT) zimbra-perl-base $(PERL_REQ)

pkgrm: pkgrm%

pkgrm%:
	$(PKG_PURGE) zimbra-base

setup:
	mkdir -p tmp/$(BUILD_PLATFORM)
	cp -prf zimbra-perl-socket tmp/$(BUILD_PLATFORM)

build: setup pkgadd
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-perl-socket/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/socket.spec && \
 	$(replace-pathinfo) SPECS/socket.spec && \
	perl -pi -e 's|BuildRequires:      perl|BuildRequires:      perl, $(PERL_REQ)|' SPECS/socket.spec && \
	perl -pi -e 's|Requires:           perl, perl-core|Requires:           perl, perl-core, $(PERL_REQ)|' SPECS/socket.spec && \
	cp ../../../../src/Socket-$(pvers).tar.gz SOURCES/zimbra-perl-socket-$(pvers).tar.gz && \
 	$(PKG_BUILD) SPECS/socket.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-perl-socket/debian/changelog && \
 	$(replace-pathinfo) zimbra-perl-socket/debian/rules && \
	$(CHMOD) u+w zimbra-perl-socket/debian/control && \
	cp ../../src/Socket-$(pvers).tar.gz zimbra-perl-socket_$(pvers).orig.tar.gz && \
	tar xfz zimbra-perl-socket_$(pvers).orig.tar.gz --strip-components=1  -C zimbra-perl-socket && \
	cd zimbra-perl-socket && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	rm -rf tmp/$(BUILD_PLATFORM)/zimbra-perl-socket
	rm -f tmp/$(BUILD_PLATFORM)/zimbra-perl-socket_*
