Summary:            Zimbra's LibXML2 build
Name:               zimbra-libxml2
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            MIT
Source:             %{name}-%{version}.tar.gz
BuildRequires:      zlib-devel
Requires:  zimbra-libxml2-libs = %{version}-%{release}
AutoReqProv:        no
URL:                http://www.xmlsoft.org

%description
The Zimbra LibXML2 build

%prep
%setup -n libxml2-%{version}

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g"; export CFLAGS; \
./configure --prefix=OZC \
  --enable-shared=yes --enable-static=no --without-python
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}

%package libs
Summary:        LibXML2 Libaries
Requires:  zimbra-base
AutoReqProv:        no

%description libs
The zimbra-libxml2-libs package contains the libxml2 libraries

%package devel
Summary:        LibXML2 Development
Requires:  zimbra-libxml2-libs = %{version}-%{release}
AutoReqProv:        no

%description devel
The zimbra-libxml2-devel package contains the linking libraries and include files

%files
%defattr(-,root,root)
OZCB
OZCS
%exclude OZCB/xml2-config

%files libs
%defattr(-,root,root)
OZCL/*.so.*

%files devel
%defattr(-,root,root)
OZCB/xml2-config
OZCI
OZCL/*.la
OZCL/*.so
OZCL/cmake
OZCL/pkgconfig
OZCL/xml2Conf.sh

