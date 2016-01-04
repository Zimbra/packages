Summary:            CA Certs keystore for OpenJDK
Name:               zimbra-openjdk-cacerts
Version:            1.0.4
Release:            ITERATIONZAPPEND
License:            MPL-2
Requires:           zimbra-base, zimbra-openjdk
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%description
CA certs keystore for use with OpenJDK

%install
mkdir -p ${RPM_BUILD_ROOT}/OZCL/jvm/java/jre/lib/security/
cp ../../cacerts ${RPM_BUILD_ROOT}/OZCL/jvm/java/jre/lib/security/cacerts

%files
OZCL/jvm/java/jre/lib/security

%pre -p /bin/bash
if [ "$1" -ge "2" ]; then
  zver=$(rpm -q --queryformat='%%{version}-%%{release}' zimbra-openjdk-cacerts)
  mkdir -p /opt/zimbra/.saveconfig/zimbra-openjdk-cacerts-${zver}
  cacerts=`mktemp --tmpdir=/opt/zimbra/.saveconfig/zimbra-openjdk-cacerts-${zver} cacerts.XXXXXX`
  cp /opt/zimbra/common/lib/jvm/java/jre/lib/security/cacerts $cacerts
fi

%post -p /bin/bash
/bin/chown zimbra:zimbra /opt/zimbra/common/lib/jvm/java/jre/lib/security/cacerts
/bin/chmod 644 /opt/zimbra/common/lib/jvm/java/jre/lib/security/cacerts
if [ "$1" -ge "2" ]; then
  if [ -x /opt/zimbra/bin/zmcertmgr ]; then
    # Run as zimbra, extract CA to /opt/zimbra/conf/ca
    /bin/su - zimbra -c '/opt/zimbra/bin/zmcertmgr createca'
    # Run as zimbra, update OpenJDK cacerts file with the CA stored in LDAP
    /bin/su - zimbra -c '/opt/zimbra/bin/zmcertmgr deployca --localonly'
  fi
fi

%changelog
* Fri Dec 14 2015  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.4
- Support running zmcertmgr as user zimbra instead of root
* Fri Dec 11 2015  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.3
- Enhance upgrade check
* Mon Dec 07 2015  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.2
- Ensure that on upgrades of the zimbra-openjdk-cacerts package, that the keystore is updated
- Ensure that on upgrades of the zimbra-openjdk-cacerts package, that the old keystore is backed up
* Wed Dec 02 2015  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.1
- Updated to include full CA Certs from Mozilla CA list
