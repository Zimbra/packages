Summary:            Zimbra's Apache HTTPD build
Name:               zimbra-httpd
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            Apache-2.0
Source:             %{name}-%{version}.tar.bz2
BuildRequires:      zimbra-apr-devel
BuildRequires:      zimbra-apr-util-devel
BuildRequires:      zlib-devel
BuildRequires:      pcre-devel
Requires:           zlib, pcre
Requires:           zimbra-apr-libs, zimbra-apr-util-libs, zimbra-apache-base
AutoReqProv:        no
URL:                http://httpd.apache.org/

%description
The Zimbra Apache HTTPD build

%changelog
* Fri Feb 08 2019  Zimbra Packaging Services <packaging-devel@zimbra.com>
-Upgraded to 2.4.46
* Fri Feb 08 2019  Zimbra Packaging Services <packaging-devel@zimbra.com> 
-Updated the version.
* Fri May 01 2015  Zimbra Packaging Services <packaging-devel@zimbra.com>
-Initial Release.

%prep
%setup -n httpd-%{version}

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g"; export CFLAGS; \
./configure --prefix=OZC \
  --with-apr=OZCB/apr-1-config \
  --with-apr-util=OZCB/apu-1-config \
  --mandir=OZCS/man \
  --libexecdir=OZCL/apache2/modules \
  --datadir=/opt/zimbra/data/httpd \
  --enable-so \
  --with-mpm=event \
  --enable-mpms-shared="all"
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}/opt/zimbra/data/httpd/conf
mv ${RPM_BUILD_ROOT}/OZC/conf/mime.types ${RPM_BUILD_ROOT}/opt/zimbra/data/httpd/conf/
mv ${RPM_BUILD_ROOT}/OZC/conf/magic ${RPM_BUILD_ROOT}/opt/zimbra/data/httpd/conf/

%package devel
Summary:        Apache HTTPD Development
Requires: zimbra-httpd = %{version}-%{release}
Requires: zimbra-apr-devel
Requires: zimbra-apr-util-devel
AutoReqProv:        no

%description devel
The zimbra-httpd-devel package contains the linking libraries and include files

%files
%defattr(-,root,root)
OZCB
OZCS
OZCL/apache2/modules
/opt/zimbra/data
%exclude /opt/zimbra/data/httpd/build
%exclude OZCB/apxs

%files devel
%defattr(-,root,root)
OZCI
/opt/zimbra/data/httpd/build
%attr(775, root, zimbra) OZC/conf
OZCB/apxs
