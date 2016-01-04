Summary:        Zimbra Perl
Name:           zimbra-perl
Version:        1.0.0
Release:        ITERATIONZAPPEND
License:        GPL-2
Packager:       Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:          Development/Languages
Requires:       zimbra-perl-base, zimbra-perl-archive-zip, zimbra-perl-berkeleydb
Requires:       zimbra-perl-bit-vector, zimbra-perl-cache-fastmmap, zimbra-perl-canary-stability
Requires:       zimbra-perl-carp-clan, zimbra-perl-class-inspector, zimbra-perl-compress-raw-bzip2
Requires:       zimbra-perl-compress-raw-zlib, zimbra-perl-config-inifiles, zimbra-perl-convert-asn1
Requires:       zimbra-perl-convert-binhex, zimbra-perl-convert-tnef, zimbra-perl-convert-uulib
Requires:       zimbra-perl-crypt-openssl-random, zimbra-perl-crypt-openssl-rsa, zimbra-perl-crypt-saltedhash
Requires:       zimbra-perl-data-uuid, zimbra-perl-date-calc, zimbra-perl-date-manip, zimbra-perl-dbd-mysql
Requires:       zimbra-perl-dbd-sqlite, zimbra-perl-db-file, zimbra-perl-dbi, zimbra-perl-digest-hmac
Requires:       zimbra-perl-digest-sha1, zimbra-perl-email-date-format, zimbra-perl-encode-detect
Requires:       zimbra-perl-encode-locale, zimbra-perl-error, zimbra-perl-exporter-tiny, zimbra-perl-zmq-libzmq3
Requires:       zimbra-perl-file-grep, zimbra-perl-file-listing, zimbra-perl-filesys-df, zimbra-perl-file-tail
Requires:       zimbra-perl-geography-countries, zimbra-perl-html-parser, zimbra-perl-http-cookies, zimbra-perl-http-daemon
Requires:       zimbra-perl-http-date, zimbra-perl-http-message, zimbra-perl-http-negotiate, zimbra-perl-innotop
Requires:       zimbra-perl-io-compress, zimbra-perl-io-html, zimbra-perl-io-sessiondata, zimbra-perl-io-socket-inet6
Requires:       zimbra-perl-io-socket-ip, zimbra-perl-io-socket-ssl, zimbra-perl-io-stringy, zimbra-perl-ip-country, zimbra-perl-json-pp
Requires:       zimbra-perl-libwww, zimbra-perl-list-moreutils, zimbra-perl-lwp-mediatypes, zimbra-perl-lwp-protocol-https
Requires:       zimbra-perl-mail-dkim, zimbra-perl-mail-spf, zimbra-perl-mailtools, zimbra-perl-math-bigint, zimbra-perl-mime-lite
Requires:       zimbra-perl-mime-tools, zimbra-perl-mime-types, zimbra-perl-mozilla-ca, zimbra-perl-netaddr-ip
Requires:       zimbra-perl-net-cidr, zimbra-perl-net-cidr-lite, zimbra-perl-net-dns, zimbra-perl-net-dns-resolver-programmable
Requires:       zimbra-perl-net-http, zimbra-perl-net-ldap, zimbra-perl-net-ldapapi, zimbra-perl-net-libidn, zimbra-perl-net-server
Requires:       zimbra-perl-net-ssleay, zimbra-perl-parent, zimbra-perl-proc-processtable, zimbra-perl-soap-lite, zimbra-perl-socket
Requires:       zimbra-perl-socket-linux, zimbra-perl-swatchdog, zimbra-perl-task-weaken, zimbra-perl-term-readkey, zimbra-perl-timedate
Requires:       zimbra-perl-unix-getrusage, zimbra-perl-unix-syslog, zimbra-perl-uri, zimbra-perl-www-robotrules
Requires:       zimbra-perl-xml-namespacesupport, zimbra-perl-xml-parser, zimbra-perl-xml-parser-lite, zimbra-perl-xml-sax
Requires:       zimbra-perl-xml-sax-base, zimbra-perl-xml-sax-expat, zimbra-perl-xml-simple, zimbra-perl-zmq-constants
AutoReqProv:        no

%define debug_package %{nil}

%description
Zimbra Perl is a meta package that can be used to install most all
of the Zimbra required perl modules.  The current sole exception is
the Mail::SpamAssassin module, as that is for MTA nodes only

%files
