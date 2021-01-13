Summary:            Zimbra's PHP build
Name:               zimbra-php
Version:            VERSION
Release:            1zimbra8.7b3ZAPPEND
License:            BSD
Source:             %{name}-%{version}.tar.bz2
BuildRequires:      zlib-devel
BuildRequires:      zimbra-httpd-devel
BuildRequires:      zimbra-aspell-devel
BuildRequires:      zimbra-aspell
BuildRequires:      zimbra-libxml2-devel
Requires:           zimbra-aspell-libs
Requires:           zimbra-libxml2-libs
Requires:           zlib, zimbra-spell-base
AutoReqProv:        no
URL:                http://php.net

%description
The Zimbra PHP build

%changelog
* Fri Jan 08 2021  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b3ZAPPEND
-Updated PHP version.
* Wed Feb 08 2019  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b3ZAPPEND
-Updated PHP version.
* Wed Jul 28 2017  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
-Bug 106089: Updated PHP.
* Fri May 01 2015  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b1ZAPPEND
-Initial Release.

%prep
%setup -n php-%{version}

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g"; export CFLAGS; \
./configure --prefix=OZC \
  --with-apxs2=OZCB/apxs \
  --with-config-file-path=/opt/zimbra/conf \
  --with-pspell=OZC \
  --with-libxml-dir=OZC \
  --enable-maintainer-zts
sed -i.bak -e 's|SYSCONFDIR=\x27\x24\x28INSTALL_ROOT\x29OZC/conf\x27|SYSCONFDIR=\x27OZC/conf\x27|g' Makefile
make

%install
make install INSTALL_ROOT=${RPM_BUILD_ROOT}
rm -rf ${RPM_BUILD_ROOT}/.channels
rm -rf ${RPM_BUILD_ROOT}/.depdb
rm -rf ${RPM_BUILD_ROOT}/.depdblock
rm -rf ${RPM_BUILD_ROOT}/.filemap
rm -rf ${RPM_BUILD_ROOT}/.lock

%files
%defattr(-,root,root)
OZCL/apache2/modules
%exclude OZCB
%exclude OZCE
%exclude OZCI
%exclude OZCL/php
%exclude OZC/php
