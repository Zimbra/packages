Summary:            Zimbra's Apache Portable Runtime Utilities build
Name:               zimbra-apr-util
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            Apache-2.0
Source:             %{name}-%{version}.tar.bz2
BuildRequires:      zimbra-apr-devel, expat-devel
BuildRequires:      zimbra-openssl-devel
Requires:            zimbra-apr-util-libs = %{version}-%{release}
AutoReqProv:        no
URL:                https://apr.apache.org/

%description
The Zimbra Apache Portable Runtime Utilities build

%prep
%setup -n apr-util-%{version}

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g"; export CFLAGS; \
./configure --prefix=OZC \
 --with-apr=OZCB/apr-1-config \
 --with-crypto \
 --with-openssl=OZC
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}

%package libs
Summary:        Apache Portable Runtime Utilities Libaries
Requires: 	zimbra-apr-libs, zimbra-apache-base
Requires:        zimbra-openssl-libs
AutoReqProv:        no

%description libs
The zimbra-apr-util-libs package contains the apr utilities libraries

%package devel
Summary:        Apache Portable Runtime Utilities Development
Requires:  zimbra-apr-util-libs = %{version}-%{release}
AutoReqProv:        no

%description devel
The zimbra-apr-util-devel package contains the linking libraries and include files

%files libs
%defattr(-,root,root)
OZCL/*.so.*
OZCL/apr-util-1/*.so

%files devel
%defattr(-,root,root)
OZCB/apu-1-config
OZCI
OZCL/*.a
OZCL/*.la
OZCL/*.so
OZCL/apr-util-1/*.la
OZCL/apr-util-1/*.a
OZCL/aprutil.exp
OZCL/pkgconfig
