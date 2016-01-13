PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(EXTUTILS_CONSTANT)

.PHONY: all clean build getsrc pkgadd pkgrm setup checkos

all: checkos clean getsrc build pkgrm1

files = $(wildcard src/ExtUtils-Constant-$(pvers).tar.gz)

checkos:
ifneq ($(BUILD_PLATFORM), RHEL6_64)
	@echo "Skipping OS, not required"
	@exit 0
endif

getsrc:
	mkdir -p src
ifeq ($(files),)
	cd src && \
	wget -q https://cpan.metacpan.org/authors/id/N/NW/NWCLARK/ExtUtils-Constant-$(pvers).tar.gz
else
	@echo "Already have the source, skipping download"
endif

pkgadd:
	$(PKG_EXTRACT) zimbra-perl-base

pkgrm: pkgrm%
pkgrm%:
	$(PKG_PURGE) zimbra-base

setup:
	mkdir -p tmp/$(BUILD_PLATFORM)
	cp -prf zimbra-perl-extutils-constant tmp/$(BUILD_PLATFORM)

build: setup pkgadd
	(cd tmp/$(BUILD_PLATFORM)/zimbra-perl-extutils-constant/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/extutils-constant.spec && \
 	$(replace-pathinfo) SPECS/extutils-constant.spec && \
	cp ../../../../src/ExtUtils-Constant-$(pvers).tar.gz SOURCES/zimbra-perl-extutils-constant-$(pvers).tar.gz && \
 	$(PKG_BUILD) SPECS/extutils-constant.spec \
	)

clean: pkgrm
	rm -rf tmp/$(BUILD_PLATFORM)/zimbra-perl-extutils-constant
	rm -f tmp/$(BUILD_PLATFORM)/zimbra-perl-extutils-constant_*
