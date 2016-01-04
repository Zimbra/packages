Summary:            Zimbra's Berkeley DB build
Name:               zimbra-bdb
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            Sleepycat
Source:             %{name}-%{version}.tar.gz
Requires:           zimbra-bdb-libs = %{version}-%{release}
AutoReqProv:        no
URL:                http://www.oracle.com/technetwork/database/database-technologies/berkeleydb/downloads/index.html

%description
The Zimbra Berkeley DB build

%prep
%setup -n db-%{version}

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g"; export CFLAGS; \
cd build_unix
../dist/configure --enable-posixmutexes --with-mutex=POSIX/pthreads \
  --prefix=OZC --disable-static
make

%install
cd build_unix
make install DESTDIR=${RPM_BUILD_ROOT}

%package libs
Summary:        Berkeley DB Libaries
Requires:       zimbra-base
AutoReqProv:        no

%description libs
The zimbra-bdb-libs package contains the bdb libraries

%package devel
Summary:        Berkeley DB Development
Requires: zimbra-bdb-libs = %{version}-%{release}
AutoReqProv:        no

%description devel
The zimbra-bdb-devel package contains the linking libraries and include files

%files
%defattr(-,root,root)
OZCB
%exclude OZC/docs

%files libs
%defattr(-,root,root)
OZCL/libdb-5.2.so

%files devel
%defattr(-,root,root)
OZCI
OZCL/*.la
OZCL/libdb-5.so
OZCL/libdb.so
