Summary:            Zimbra's freetype build
Name:               zimbra-freetype
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            GPL-2.0
BuildRequires:      zlib-devel, bzip2-devel
Source:             %{name}-%{version}.tar.gz
URL:                http://www.freetype.org

%description
The Zimbra freetype build

%prep
%setup -n freetype-%{version}

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-fPIC -O2 -g"; export CFLAGS; \
./configure --prefix=OZC
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}

%package libs
Summary:        freetype Libaries
Requires:           zlib, bzip2-libs, zimbra-base
AutoReqProv:        no

%description libs
The zimbra-freetype-libs package contains the freetype libraries

%package devel
Summary:        freetype Development
Requires: zimbra-freetype-libs = %{version}-%{release}
AutoReqProv:        no

%description devel
The zimbra-freetype-devel package contains the linking libraries and include files

%files libs
%defattr(-,root,root)
OZCL/*.so.*

%files devel
%defattr(-,root,root)
OZCB
OZCI
OZCL/pkgconfig
OZCL/*.a
OZCL/*.la
OZCL/*.so
OZCS
