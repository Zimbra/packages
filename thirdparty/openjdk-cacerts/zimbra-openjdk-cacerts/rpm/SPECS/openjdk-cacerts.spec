Summary:            CA Certs keystore for OpenJDK
Name:               zimbra-openjdk-cacerts
Version:            1.0.6
Release:            ITERATIONZAPPEND
License:            MPL-2
Requires:           zimbra-base, zimbra-openjdk
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%description
CA certs keystore for use with OpenJDK

%changelog
* Tue Aug 24 2021  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.6-ITERATIONZAPPEND
- Update openjdk-cacerts from latest Mozilla certdata.txt
* Thu Feb 11 2016  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.5-ITERATIONZAPPEND
- Relocate cacerts to OZCE/java to avoid conflicts with the OpenJDK package
* Fri Dec 14 2015  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.4-ITERATIONZAPPEND
- Support running zmcertmgr as user zimbra instead of root
* Fri Dec 11 2015  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.3-ITERATIONZAPPEND
- Enhance upgrade check
* Mon Dec 07 2015  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.2-ITERATIONZAPPEND
- Ensure that on upgrades of the zimbra-openjdk-cacerts package, that the keystore is updated
- Ensure that on upgrades of the zimbra-openjdk-cacerts package, that the old keystore is backed up
* Wed Dec 02 2015  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.1-ITERATIONZAPPEND
- Updated to include full CA Certs from Mozilla CA list

%install
mkdir -p ${RPM_BUILD_ROOT}/OZCE/java
cp ../../cacerts ${RPM_BUILD_ROOT}/OZCE/java/cacerts

%files
%attr(644,zimbra,zimbra) OZCE/java/cacerts

%pre -p /bin/bash
if [ "$1" -ge "2" ]; then
  zver=$(rpm -q --queryformat='%%{version}-%%{release}' zimbra-openjdk-cacerts)
  mkdir -p /opt/zimbra/.saveconfig/zimbra-openjdk-cacerts-${zver}
  cacerts=`mktemp --tmpdir=/opt/zimbra/.saveconfig/zimbra-openjdk-cacerts-${zver} cacerts.XXXXXX`
  cp OZCE/java/cacerts $cacerts
fi

%post -p /bin/bash
/bin/chown zimbra:zimbra OZCE/java/cacerts
/bin/chmod 644 OZCE/java/cacerts
if [ "$1" -ge "2" ]; then
  if [ -x /opt/zimbra/bin/zmcertmgr ]; then
    # Run as zimbra, extract CA to /opt/zimbra/conf/ca
    /bin/su - zimbra -c '/opt/zimbra/bin/zmcertmgr createca'
    # Run as zimbra, update OpenJDK cacerts file with the CA stored in LDAP
    /bin/su - zimbra -c '/opt/zimbra/bin/zmcertmgr deployca --localonly'
  fi
fi

