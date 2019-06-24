Summary:            Zimbra's ClamAV build
Name:               zimbra-clamav
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            GPL-2
Source:             %{name}-%{version}.tar.gz
BuildRequires:      zlib-devel
BuildRequires:      ncurses-devel
BuildRequires:      zimbra-openssl-devel
BuildRequires:      zimbra-libxml2-devel
BuildRequires:      zimbra-libmilter-devel
Requires:  zimbra-clamav-libs = %{version}-%{release}, zimbra-openssl-libs
Requires:            zimbra-libxml2-libs
AutoReqProv:        no
URL:                http://www.clamav.net/

%description
The Zimbra ClamAV build

%prep
%setup -n clamav-%{version}

%build
LDFLAGS="-LOZCL -Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g"; export CFLAGS; \
CPPFLAGS="-IOZCI"; export CPPFLAGS; \
 ./configure --prefix=OZC \
  --libdir=OZCL \
  --with-openssl=OZC \
  --with-xml=OZC \
  --with-user=zimbra \
  --with-group=zimbra \
  --with-included-ltdl \
  --disable-clamav \
  --enable-milter
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}
rm -f ${RPM_BUILD_ROOT}OZCE/*.sample
rm -rf ${RPM_BUILD_ROOT}/usr/lib/systemd

%package libs
Summary:        ClamAV Libaries
Requires:  zimbra-openssl-libs, zimbra-libxml2-libs, zimbra-mta-base
AutoReqProv:        no

%description libs
The zimbra-clamav-libs package contains the clamav libraries

%package devel
Summary:        ClamAV Development
Requires:  zimbra-clamav-libs = %{version}-%{release}
AutoReqProv:        no

%description devel
The zimbra-clamav-devel package contains the linking libraries and include files

%files
%defattr(-,root,root)
OZCB
OZC/sbin
OZCS
%exclude OZCB/clamav-config

%files libs
%defattr(-,root,root)
OZCL/*.so.*

%files devel
%defattr(-,root,root)
OZCB/clamav-config
OZCL/*.la
OZCL/*.so
OZCL/pkgconfig
OZCI

