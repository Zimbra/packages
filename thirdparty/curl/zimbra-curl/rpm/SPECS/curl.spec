Summary:            Zimbra's Curl build
Name:               zimbra-curl
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            MIT
Source:             %{name}-%{version}.tar.gz
BuildRequires:      zlib-devel
BuildRequires:      zimbra-openssl-devel
BuildRequires:      zimbra-heimdal-devel
Requires:  zimbra-curl-libs = %{version}-%{release}, zimbra-openssl-libs, zimbra-heimdal-libs
AutoReqProv:        no
URL:                http://curl.haxx.se/

%description
The Zimbra Curl build

%prep
%setup -n curl-%{version}

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g"; export CFLAGS; \
./configure --prefix=OZC \
  --disable-ldap --disable-ldaps \
  --with-gssapi=OZC \
  --with-ssl=OZC \
  --without-gnutls \
  --with-ca-bundle=OZCS/curl/ca-bundle.crt \
  --enable-ipv6 \
  --with-zlib \
  --without-libidn \
  --disable-static
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}
make ca-bundle
mkdir -p ${RPM_BUILD_ROOT}OZCS/curl
cp -f lib/ca-bundle.crt ${RPM_BUILD_ROOT}OZCS/curl/ca-bundle.crt

%package libs
Summary:        Curl Libaries
Requires:  zimbra-openssl-libs, zimbra-heimdal-libs, zimbra-base
AutoReqProv:        no

%description libs
The zimbra-curl-libs package contains the curl libraries

%package devel
Summary:        Curl Development
Requires:  zimbra-curl-libs = %{version}-%{release}
AutoReqProv:        no

%description devel
The zimbra-curl-devel package contains the linking libraries and include files

%files
%defattr(-,root,root)
OZCB
OZCS
%exclude OZCB/curl-config

%files libs
%defattr(-,root,root)
OZCL/*.so.*

%files devel
%defattr(-,root,root)
OZCB/curl-config
OZCL/*.la
OZCL/*.so
OZCL/pkgconfig
OZCI

