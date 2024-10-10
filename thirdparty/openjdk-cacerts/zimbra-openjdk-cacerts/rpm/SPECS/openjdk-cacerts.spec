Summary:            CA Certs keystore for OpenJDK
Name:               zimbra-openjdk-cacerts
Version:            1.0.11
Release:            1zimbra8.7b1ZAPPEND
License:            MPL-2
Requires:           zimbra-base, zimbra-openjdk
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%description
CA certs keystore for use with OpenJDK

%changelog
* Mon Jul 22 2024 Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.11-1zimbra8.7b1ZAPPEND
- Updated zimbra-openjdk-cacerts CA root store
* Thu Nov 23 2023  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.10-1zimbra8.7b1ZAPPEND
- ZBUG-3696, Update zimbra-openjdk-cacerts CA root store
* Fri Oct 06 2023  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.9-1zimbra8.7b1ZAPPEND
- ZRFE-1328, Update zimbra-openjdk-cacerts CA root store
* Fri Sep 17 2021  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.8-ITERATIONZAPPEND
- Fix for ZBUG-2425
* Thu Sep 02 2021  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.7-ITERATIONZAPPEND
- Fix for ZBUG-2400
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
mailboxd_truststore_password=$(/bin/su - zimbra -c "zmlocalconfig -s -m nokey mailboxd_truststore_password")
/bin/chown zimbra:zimbra OZCE/java/cacerts
/bin/chmod 644 OZCE/java/cacerts
if [ "$1" -ge "2" ]; then
  if [ -x /opt/zimbra/bin/zmcertmgr ]; then
    # Run as zimbra, extract CA to /opt/zimbra/conf/ca
    /bin/su - zimbra -c '/opt/zimbra/bin/zmcertmgr createca'
    # Run as zimbra, update OpenJDK cacerts file with the CA stored in LDAP
    /bin/su - zimbra -c '/opt/zimbra/bin/zmcertmgr deployca --localonly'
    if [ $mailboxd_truststore_password != "changeit" ]; then
       /bin/su - zimbra -c "/opt/zimbra/common/bin/keytool -storepasswd -keystore /opt/zimbra/common/etc/java/cacerts -storepass changeit -new $mailboxd_truststore_password"
    fi
    for dir in /opt/zimbra/.saveconfig/zimbra-openjdk-cacerts-1.0.{5..10}*; do
        if [ -d "$dir" ]; then
        /bin/chown zimbra:zimbra $dir/cacerts.*
        /bin/chmod 644 $dir/cacerts.*
        for cert in `/opt/zimbra/common/bin/keytool -list -keystore $dir/cacerts.*  -storepass $mailboxd_truststore_password | grep trustedCertEntry | grep -v 'openjdk-cacerts/build/ubuntu'| grep -v 'tmp/rhel'| grep -v 'openjdk-cacerts/build/rhel'|  grep -Eo "^[^,]*"`;do
            /opt/zimbra/common/bin/keytool -exportcert -keystore $dir/cacerts.* -storepass $mailboxd_truststore_password -alias $cert -file $dir/${cert}.crt
            /bin/chown zimbra:zimbra $dir/${cert}.crt
            /bin/su - zimbra -c "/opt/zimbra/bin/zmcertmgr addcacert $dir/${cert}.crt"
            done
        fi
    done
  fi
fi
