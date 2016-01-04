Summary:            Zimbra's libsodium build
Name:               zimbra-libsodium
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            ISC
Source:             %{name}-%{version}.tar.gz
URL:                https://download.libsodium.org/doc/

%description
The Zimbra libsodium build

%prep
%setup -n libsodium-%{version}

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g"; export CFLAGS; \
./configure --prefix=OZC \
  --enable-minimal
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}

%package libs
Summary:        libsodium Libaries
Requires:       zimbra-base
AutoReqProv:        no

%description libs
The zimbra-libsodium-libs package contains the libsodium libraries

%package devel
Summary:        libsodium Development
Requires: zimbra-libsodium-libs = %{version}-%{release}
AutoReqProv:        no

%description devel
The zimbra-libsodium-devel package contains the linking libraries and include files

%files libs
%defattr(-,root,root)
OZCL/*.so.*

%files devel
%defattr(-,root,root)
OZCI
OZCL/pkgconfig
OZCL/*.a
OZCL/*.la
OZCL/*.so
