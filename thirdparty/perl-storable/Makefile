PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(STORABLE)

.PHONY: all checkos getsrc setup build pkgadd pkgrm clean

all: checkos clean getsrc build pkgrm1

files = $(wildcard src/Storable-$(pvers).tar.gz)

checkos:
ifneq ($(BUILD_PLATFORM), RHEL6_64)
	@echo "Skipping OS, not required"
	@exit 0
endif

getsrc:
	mkdir -p src
ifeq ($(files),)
	cd src && \
	wget -q https://cpan.metacpan.org/authors/id/A/AM/AMS/Storable-$(pvers).tar.gz
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
	(cd tmp/$(BUILD_PLATFORM)/zimbra-perl-storable/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
 	$(replace-pkginfo) SPECS/storable.spec && \
 	$(replace-pathinfo) SPECS/storable.spec && \
	cp ../../../../src/Storable-$(pvers).tar.gz SOURCES/zimbra-perl-storable-$(pvers).tar.gz && \
 	$(PKG_BUILD) SPECS/storable.spec \
	)

clean: pkgrm
	$(generic-clean)
