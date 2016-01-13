PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(MATH_BIGINT)

.PHONY: all clean build getsrc pkgadd pkgrm setup

all: clean getsrc build pkgrm1

files = $(wildcard src/Math-BigInt-$(pvers).tar.gz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	wget -q http://search.cpan.org/CPAN/authors/id/P/PJ/PJACKLAM/Math-BigInt-$(pvers).tar.gz \
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
	mkdir -p tmp/$(BUILD_PLATFORM)
	cp -prf zimbra-perl-math-bigint tmp/$(BUILD_PLATFORM)

build: setup pkgadd
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-perl-math-bigint/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/math-bigint.spec && \
 	$(replace-pathinfo) SPECS/math-bigint.spec && \
	cp ../../../../src/Math-BigInt-$(pvers).tar.gz SOURCES/zimbra-perl-math-bigint-$(pvers).tar.gz && \
 	$(PKG_BUILD) SPECS/math-bigint.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
 	$(replace-pkginfo) zimbra-perl-math-bigint/debian/changelog && \
 	$(replace-pathinfo) zimbra-perl-math-bigint/debian/rules && \
	$(CHMOD) u+w zimbra-perl-math-bigint/debian/control && \
	cp ../../src/Math-BigInt-$(pvers).tar.gz zimbra-perl-math-bigint_$(pvers).orig.tar.gz && \
	tar xfz zimbra-perl-math-bigint_$(pvers).orig.tar.gz --strip-components=1  -C zimbra-perl-math-bigint && \
	cd zimbra-perl-math-bigint && \
	$(PKG_BUILD) \
	)
endif

clean: pkgrm
	rm -rf tmp/$(BUILD_PLATFORM)/zimbra-perl-math-bigint
	rm -f tmp/$(BUILD_PLATFORM)/zimbra-perl-math-bigint_*
