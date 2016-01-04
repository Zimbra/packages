Summary:            Zimbra's memcached build
Name:               zimbra-memcached
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            BSD
Source:             %{name}-%{version}.tar.gz
BuildRequires:      zimbra-libevent-devel
BuildRequires:      pkgconfig
Requires:           zimbra-libevent-libs, zimbra-memcached-base
AutoReqProv:        no
URL:                http://memcached.org/

%description
The Zimbra memcached build

%prep
%setup -n memcached-%{version}

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g"; export CFLAGS; \
PKG_CONFIG_PATH="OZCL/pkgconfig"; export PKG_CONFIG_PATH; \
./configure --prefix=OZC
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}

%package devel
Summary:        memcached Development
AutoReqProv:        no

%description devel
The zimbra-memcached-devel package contains the linking libraries and include files

%files
%defattr(-,root,root)
OZCB
OZCS

%files devel
%defattr(-,root,root)
OZCI
