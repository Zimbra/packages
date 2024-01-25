Summary:            Zimbra's Curl build
Name:               zimbra-curl
Version:            10.0.0
Release:            1zimbra10.0b1ZAPPEND
License:            MIT
BuildRequires:      libcurl, curl
Requires:           zimbra-curl-libs = %{version}-%{release}, curl
AutoReqProv:        no
URL:                http://curl.haxx.se/

%description
The Zimbra Curl build

%define debug_package %{nil}

%changelog
* Tue Jan 23 2024 Zimbra Packaging Services <packaging-devel@zimbra.com> - 10.0.0-1zimbra10.0b1ZAPPEND
- Updated Zimbra curl packages so that it depends on OS version of curl and provide symbolic links from the Zimbra curl to the OS version of curl
* Mon Jun 12 2023 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b4ZAPPEND
- ZBUG-3355, Upgraded OpenSSL to 3.0.9 and updated dependency heimdal
* Wed Dec 02 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b3ZAPPEND
- Upgraded dependency openssl to 1.1.1h and updated dependency heimdal
* Thu Sep 10 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Upgraded dependency openssl to 1.1.1g and updated dependency heimdal

%install
mkdir -p ${RPM_BUILD_ROOT}/opt/zimbra/common/bin
mkdir -p ${RPM_BUILD_ROOT}/opt/zimbra/common/lib
ln -s /usr/bin/curl ${RPM_BUILD_ROOT}/opt/zimbra/common/bin/curl
ln -s /usr/lib64/libcurl.so.4 ${RPM_BUILD_ROOT}/opt/zimbra/common/lib/libcurl.so.4

%package libs
Summary:        Curl Libaries
Requires: zimbra-base, libcurl
AutoReqProv:        no

%description libs
The zimbra-curl-libs package contains the curl libraries

%package devel
Summary:        Curl Development
Requires: zimbra-curl-libs = %{version}-%{release}, libcurl-devel
AutoReqProv:        no

%description devel
The zimbra-curl-devel package contains the linking libraries and include files

%files
%defattr(-,root,root)
/opt/zimbra/common/bin

%files libs
%defattr(-,root,root)
/opt/zimbra/common/lib

%files devel
%defattr(-,root,root)

