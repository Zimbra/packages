Summary:            Opensource Licenses
Name:               zimbra-osl
Version:            1.0.8
Release:            ITERATIONZAPPEND
License:            GPL-2
Requires:           zimbra-base
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%description
This file contains the licenses for the open source 3rd party
software used by Zimbra

%changelog
* Tue Jun 07 2016  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.8-ITERATIONZAPPEND
- Update 0MQ to 4.1.4
- Update ClamAV to 0.99.2
- Update libxml2 to 2.9.4
- Update MariaDB to 10.1.14
- Update cURL to 7.49.0
* Wed May 04 2016  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.7-ITERATIONZAPPEND
- Update OpenJDK to 1.0.8u92b14
- Update OpenSSL to 1.0.2h
* Wed Mar 16 2016  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.6-ITERATIONZAPPEND
- Remove converse.js
* Tue Feb 09 2016  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.5-ITERATIONZAPPEND
- Update OpenJDK to 1.0.8u74b02
- Update Selenium to 2.51.0
- Update OpenSSL to 1.0.2g
- Update MariaDB to 10.1.12
- Update Unbound to 1.5.8
- Update Postfix to 3.1.0
- Update ClamAV to 0.99.1
* Mon Feb 08 2016  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.4-ITERATIONZAPPEND
- Update rsync to 3.1.2
- Update openssl to 1.0.1r
- Update MariaDB to 10.1.11
- Add apache-commons-collection 3.2.2
- Add apache-commons-compress 1.10
- Update PHP to 5.6.18
- Update OpenLDAP to 2.4.44
* Mon Jan 11 2016  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.3-ITERATIONZAPPEND
- Update MariaDB to 10.1.10
- Update Selenium to 2.49.0
- Update jquery to 1.11.0
- Add converse.js 0.9.4
- Add perl-file-libmagic 1.15
* Thu Jan 07 2016  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.2-ITERATIONZAPPEND
- Add oauth, guice
* Thu Dec 17 2015  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.1-ITERATIONZAPPEND
- Update for ZCS 8.7.0 release.

%install
mkdir -p ${RPM_BUILD_ROOT}/opt/zimbra/docs
cp ../../open_source_licenses.txt ${RPM_BUILD_ROOT}/opt/zimbra/docs

%files
/opt/zimbra/docs/open_source_licenses.txt
