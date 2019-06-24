Summary:            Zimbra's libltdl build
Name:               zimbra-libltdl
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            LGPL-2.1
Source:             %{name}-%{version}.tar.gz
URL:                https://www.gnu.org/software/libtool

%description
The Zimbra libltdl build

%prep
%setup -n libtool-%{version}

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g"; export CFLAGS; \
./configure --prefix=OZC \
  --disable-static --datarootdir=OZCS
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}
rm -rf ${RPM_BUILD_ROOT}OZCS
rm -rf ${RPM_BUILD_ROOT}OZCB

%package libs
Summary:        libltdl Libaries
Requires:        zimbra-ldap-base
AutoReqProv:    no

%description libs
The zimbra-libltdl-libs package contains the libltdl libraries

%package devel
Summary:        libltdl Development
Requires:  zimbra-libltdl-libs = %{version}-%{release}
AutoReqProv:        no

%description devel
The zimbra-libltdl-devel package contains the linking libraries and include files

%files libs
%defattr(-,root,root)
OZCL/*.so.*

%files devel
%defattr(-,root,root)
OZCI
OZCL/*.la
OZCL/*.so
