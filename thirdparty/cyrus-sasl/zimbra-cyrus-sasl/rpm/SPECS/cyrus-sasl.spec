Summary:            Zimbra's Cyrus-SASL build
Name:               zimbra-cyrus-sasl
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            MIT
Source:             %{name}-%{version}.tar.gz
Patch0:             sasl-auth-zimbra-2.1.26.patch
Patch1:             saslauthd-conf.patch
Patch2:             auxprop.patch
BuildRequires:      zlib-devel
BuildRequires:      zimbra-openssl-devel
BuildRequires:      zimbra-heimdal-devel
BuildRequires:      zimbra-libxml2-devel
BuildRequires:      zimbra-curl-devel
Requires:  zimbra-cyrus-sasl-libs = %{version}-%{release}, zimbra-openssl-libs, zimbra-heimdal-libs
Requires:            zimbra-libxml2-libs, zimbra-curl-libs
AutoReqProv:        no
URL:                https://cyrusimap.org/

%description
The Zimbra Cyrus-SASL build

%prep
%setup -n cyrus-sasl-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS;
CFLAGS="-O2 -g -D_REENTRANT"; export CFLAGS;
PATH=OZCB:$PATH; export PATH;
rm -f config/ltconfig config/libtool.m4
libtoolize -f -c
aclocal -I config -I cmulocal
automake -a -c -f
autoheader
autoconf -f
rm -f saslauthd/config/ltconfig
cd saslauthd && libtoolize -f -c && \
  aclocal -I config -I ../cmulocal -I ../config && \
  automake -a -c -f && \
  autoheader && \
  autoconf -f
cd ..
sed -i.bak 's/-lRSAglue //' configure
./configure --prefix=OZC \
  --with-saslauthd=/opt/zimbra/data/sasl2/state \
  --with-plugindir=OZCL/sasl2 \
  --with-dblib=no \
  --with-devrandom=/dev/urandom \
  --with-gss_impl=heimdal \
  --with-lib-subdir=lib \
  --with-openssl=OZC \
  --with-configdir=/opt/zimbra/conf/sasl2 \
  --enable-gssapi=OZC \
  --enable-login \
  --enable-shared=yes --enable-static=no --without-python
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}

%package libs
Summary:        Cyrus-SASL Libaries
Requires:  zimbra-openssl-libs, zimbra-heimdal-libs, zimbra-base
AutoReqProv:        no

%description libs
The zimbra-cyrus-sasl-libs package contains the curl libraries

%package devel
Summary:        Cyrus-SASL Development
Requires:  zimbra-cyrus-sasl-libs = %{version}-%{release}
AutoReqProv:        no

%description devel
The zimbra-cyrus-sasl-devel package contains the linking libraries and include files

%files
%defattr(-,root,root)
OZC/sbin
OZCS

%files libs
%defattr(-,root,root)
%dir OZCL/sasl2
OZCL/*.so.*
OZCL/sasl2

%files devel
%defattr(-,root,root)
OZCI
OZCL/*.la
OZCL/*.so
OZCL/pkgconfig
