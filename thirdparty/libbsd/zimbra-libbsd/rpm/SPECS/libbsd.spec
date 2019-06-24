Summary:            Zimbra's libbsd build
Name:               zimbra-libbsd
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            BSD
Source:             %{name}-%{version}.tar.xz
URL:                http://libbsd.freedesktop.org/

%description
The Zimbra libbsd build

%prep
%setup -n libbsd-%{version}

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-fPIC -D_REENTRANT"; export CFLAGS; \
CXXFLAGS="-D_REENTRANT"; export CXXFLAGS;
./configure --prefix=OZC
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}

%package libs
Summary:        libbsd Libaries
Requires:        zimbra-base
AutoReqProv:        no

%description libs
The zimbra-libbsd-libs package contains the libbsd libraries

%package devel
Summary:        libbsd Development
Requires:  zimbra-libbsd-libs = %{version}-%{release}
AutoReqProv:        no

%description devel
The zimbra-libbsd-devel package contains the linking libraries and include files

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
%exclude OZCS
