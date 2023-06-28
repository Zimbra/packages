Summary:            Initial ClamAV Databases for ClamAV
Name:               zimbra-clamav-db
Version:            1.0.0
Release:            1zimbra8.7b2ZAPPEND
License:            GPL-2
Requires:           zimbra-base
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%description
Initial ClamAV Databases for ClamAV

%changelog
* Fri Jun 23 2023  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- ZCS-13605, Updated clamav-db for ClamAV-1.0.1
* Wed Mar 09 2016  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.0-ITERATIONZAPPEND
- Initial version

%install
mkdir -p ${RPM_BUILD_ROOT}/opt/zimbra/data/clamav/init
cp ../../../src/bytecode.cvd ${RPM_BUILD_ROOT}/opt/zimbra/data/clamav/init/bytecode.cvd.init
cp ../../../src/daily.cvd ${RPM_BUILD_ROOT}/opt/zimbra/data/clamav/init/daily.cvd.init
cp ../../../src/main.cvd ${RPM_BUILD_ROOT}/opt/zimbra/data/clamav/init/main.cvd.init

%files
%attr(644,zimbra,zimbra) /opt/zimbra/data/clamav/init/bytecode.cvd.init
%attr(644,zimbra,zimbra) /opt/zimbra/data/clamav/init/daily.cvd.init
%attr(644,zimbra,zimbra) /opt/zimbra/data/clamav/init/main.cvd.init

%post -p /bin/bash
if [ -f /opt/zimbra/data/clamav/db/daily.cvd ]; then
        rm -rf /opt/zimbra/data/clamav/db/daily.cvd
fi
if [ -f /opt/zimbra/data/clamav/db/main.cvd ]; then
        rm -rf /opt/zimbra/data/clamav/db/main.cvd
fi
if [ -f /opt/zimbra/data/clamav/db/bytecode.cvd ]; then
        rm -rf /opt/zimbra/data/clamav/db/bytecode.cvd
fi
