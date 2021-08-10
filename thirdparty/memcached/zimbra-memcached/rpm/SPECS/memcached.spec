Summary:            Zimbra's memcached build
Name:               zimbra-memcached
Epoch:              1
Version:            VERSION
Release:            1zimbra8.7b1ZAPPEND
License:            BSD
Source:             %{name}-%{version}.tar.gz
BuildRequires:      zimbra-libevent-devel
BuildRequires:      pkgconfig
Requires:           zimbra-libevent-libs, zimbra-memcached-base
AutoReqProv:        no
URL:                http://memcached.org/

%description
The Zimbra memcached build

%changelog
* Tue Aug 10 2021 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b1ZAPPEND
- Upgrade to memcached 1.6.5 .
* Sat Jun 24 2017 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-2.PKG_OS_TAG
- Upgrade to memcached 1.4.37 for Bug 107246.

%prep
%setup -n memcached-%{version}

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g"; export CFLAGS; \
PKG_CONFIG_PATH="OZCL/pkgconfig"; export PKG_CONFIG_PATH; \
./configure --prefix=OZC
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}

%package devel
Summary:        memcached Development
AutoReqProv:        no

%description devel
The zimbra-memcached-devel package contains the linking libraries and include files

%files
%defattr(-,root,root)
OZCB
OZCS

%files devel
%defattr(-,root,root)
OZCI
