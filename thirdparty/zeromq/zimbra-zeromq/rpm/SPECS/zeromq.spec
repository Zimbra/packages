Summary:            Zimbra's 0MQ build
Name:               zimbra-zeromq
Version:            VERSION
Release:            1zimbra8.7b2ZAPPEND
License:            LGPL-3
Source:             %{name}-%{version}.tar.gz
BuildRequires:      zimbra-libsodium-devel >= 1.0.18-1zimbra8.7b1ZAPPEND
BuildRequires:      pkgconfig
Requires:           zimbra-zeromq-libs = %{version}-%{release}
AutoReqProv:        no
URL:                http://zeromq.org/

%description
The Zimbra 0MQ build

%changelog
* Wed Dec 28 2022 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Upgraded libsodium to 1.0.18

%prep
%setup -n zeromq-%{version}

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O0 -g"; export CFLAGS; \
PKG_CONFIG_PATH="OZCL/pkgconfig"; export PKG_CONFIG_PATH; \
./configure --prefix=OZC \
  --with-libsodium=OZC \
  --with-relaxed
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}

%package libs
Summary:        0MQ Libaries
Requires:       zimbra-libsodium-libs >= 1.0.18-1zimbra8.7b1ZAPPEND, zimbra-base
AutoReqProv:        no

%description libs
The zimbra-zeromq-libs package contains the zeromq libraries

%package devel
Summary:        0MQ Development
Requires: zimbra-zeromq-libs = %{version}-%{release}
AutoReqProv:        no

%description devel
The zimbra-zeromq-devel package contains the linking libraries and include files

%files
%defattr(-,root,root)
OZCB
OZCS

%files libs
%defattr(-,root,root)
OZCL/*.so.*

%files devel
%defattr(-,root,root)
OZCI
OZCL/*.a
OZCL/*.la
OZCL/*.so
OZCL/pkgconfig
