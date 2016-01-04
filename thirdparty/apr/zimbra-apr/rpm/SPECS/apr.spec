Summary:            Zimbra's Apache Portable Runtime build
Name:               zimbra-apr
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            Apache-2.0
Source:             %{name}-%{version}.tar.bz2
Requires:           zimbra-apr-libs = %{version}-%{release}
AutoReqProv:        no
URL:                https://apr.apache.org/

%description
The Zimbra Apache Portable Runtime build

%prep
%setup -n apr-%{version}

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g"; export CFLAGS; \
./configure --prefix=OZC
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}

%package libs
Summary:        Apache Portable Runtime Libaries
Requires:       zimbra-apache-base
AutoReqProv:        no

%description libs
The zimbra-apr-libs package contains the apr libraries

%package devel
Summary:        Apache Portable Runtime Development
Requires: zimbra-apr-libs = %{version}-%{release}
AutoReqProv:        no

%description devel
The zimbra-apr-devel package contains the linking libraries and include files

%files libs
%defattr(-,root,root)
OZCL/*.so.*

%files devel
%defattr(-,root,root)
OZCB/apr-1-config
OZC/build-1
OZCI
OZCL/*.a
OZCL/*.la
OZCL/*.so
OZCL/apr.exp
OZCL/pkgconfig
