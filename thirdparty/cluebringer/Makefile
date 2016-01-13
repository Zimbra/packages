PKG_ROOT := $(shell pwd)

include $(PKG_ROOT)/../../package.def

pvers := $(CLUEBRINGER_VERSION).$(CLUEBRINGER_GIT)

.PHONY: all getsrc setup build clean

all: clean getsrc build

files = $(wildcard src/cluebringer-$(pvers).tgz)

getsrc:
	mkdir -p src
ifeq ($(files),)
	(cd src && \
	git clone https://gitlab.devlabs.linuxassist.net/policyd/policyd.git cluebringer >/dev/null 2>&1 && \
	cd cluebringer && \
	git reset --hard $(CLUEBRINGER_GIT) >/dev/null 2>&1 && \
	./update-git-modules >/dev/null 2>&1 && \
	rm -rf .git awitpt/.git && \
	rm -rf awitpt/CPAN* awitpt/doxygen awitpt/SOAP && \
	mv -f awitpt/awitpt/db awitpt/ && \
	mv -f awitpt/awitpt/cache.pm awitpt/ && \
	mv -f awitpt/awitpt/netip.pm awitpt/ && \
	rmdir awitpt/awitpt && \
	rm -rf debian && \
	rm -f cluebringer.spec && \
	cd .. && \
	mv cluebringer cluebringer-$(pvers) && \
	tar cfz cluebringer-$(pvers).tgz cluebringer-$(pvers) && \
	rm -rf cluebringer-$(pvers) \
	)
else
	@echo "Already have the source, skipping download"
endif

setup:
	$(generic-setup)

build: setup
ifeq ($(PKG_EXT), rpm)
	(cd tmp/$(BUILD_PLATFORM)/zimbra-cluebringer/rpm && \
	mkdir -p BUILD BUILDROOT RPMS SOURCES SRPMS && \
	$(replace-pkginfo) SPECS/cluebringer.spec && \
	$(replace-pathinfo) SPECS/cluebringer.spec && \
	cp ../../../../src/cluebringer-$(pvers).tgz SOURCES/zimbra-cluebringer-$(pvers).tgz && \
	$(PKG_BUILD) SPECS/cluebringer.spec \
	)
else
	(cd tmp/$(BUILD_PLATFORM) && \
	$(replace-pkginfo) zimbra-cluebringer/debian/changelog && \
	$(replace-pathinfo) zimbra-cluebringer/debian/rules && \
	cp ../../src/cluebringer-$(pvers).tgz zimbra-cluebringer_$(pvers).orig.tar.gz && \
	tar xfz zimbra-cluebringer_$(pvers).orig.tar.gz --strip-components=1  -C zimbra-cluebringer && \
	cd zimbra-cluebringer && \
	chmod u+w debian/control && \
	$(PKG_BUILD) \
	)
endif

clean:
	$(generic-clean)
