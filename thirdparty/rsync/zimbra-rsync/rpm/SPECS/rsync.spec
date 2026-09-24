Summary:            Zimbra's rsync build
Name:               zimbra-rsync
Version:            3.4.1
Release:            1zimbra8.7b2ZAPPEND
License:            GPL-3
Source:             %{name}-%{version}.tar.gz
BuildRequires:      popt-devel, xxhash-devel
Requires:           popt, zimbra-base, xxhash-libs
AutoReqProv:        no
URL:                https://rsync.samba.org

%description
The Zimbra rsync build

%prep
%setup -n rsync-%{version}

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g"; export CFLAGS; \
./configure --prefix=OZC \
  --localstatedir=$(ZIMBRA_HOME)/data/tmp
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
OZCB
OZCS

%changelog
* Wed Aug 06 2025 Zimbra new Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- ZBUG-5062, Bumped-up rsync version due to addition of missing dependencies
* Wed Feb 05 2025 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b1ZAPPEND
- ZBUG-4670, Upgraded rsync to 3.4.1
