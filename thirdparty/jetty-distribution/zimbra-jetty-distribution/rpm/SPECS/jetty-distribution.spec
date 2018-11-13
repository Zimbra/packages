Summary:            Zimbra's jetty-distribution build
Name:               zimbra-jetty-distribution
Version:            VERSION
Release:            2.%{PKG_OS_TAG}
License:            Apache-2.0
Source:             %{name}-%{version}.tar.gz
Requires:            zimbra-store-base
AutoReqProv:        no
URL:                https://www.eclipse.org/jetty/

%define debug_package %{nil}

%description
The Zimbra jetty-distribution build

%changelog
* Thu Aug 31 2017 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-2.%{PKG_OS_TAG}
- Minor dependency fix.
* Fri Jul 7 2017 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1.%{PKG_OS_TAG}
- Initial Release.

%prep
%setup -n jetty-distribution-%{version}

%build

%install
mkdir -p ${RPM_BUILD_ROOT}/opt/zimbra/common/jetty_home
find -maxdepth 1 -mindepth 1 | grep -v -w -e debian -e rpm | xargs -r '-I{}' cp -a '{}' ${RPM_BUILD_ROOT}/opt/zimbra/common/jetty_home

%files
%defattr(-,root,root)
/opt/zimbra/common/jetty_home
