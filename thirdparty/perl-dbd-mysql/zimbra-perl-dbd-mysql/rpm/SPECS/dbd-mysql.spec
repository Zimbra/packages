Summary:            DBD::mysql - MySQL driver for the Perl5 Database Interface (DBI)
Name:               zimbra-perl-MODNORMNAME
Version:            VERSION
Release:            1zimbra8.7b5ZAPPEND
License:            GPL+ or Artistic
Source:             %{name}-%{version}.tar.gz
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
BuildRequires:      zimbra-perl-base, zimbra-perl-dbi, zimbra-mariadb-devel
BuildRequires:      zimbra-openssl-devel >= 3.0.9-1zimbra8.8b1ZAPPEND
Requires:           zimbra-perl-base, zimbra-perl-dbi, zimbra-mariadb-libs >= 10.1.25-1zimbra8.7b3ZAPPEND
AutoReqProv:        no
URL:                https://metacpan.org/release/MODNAME

%description
DBD::mysql is the Perl5 Database Interface driver for the MySQL database.
In other words: DBD::mysql is an interface between the Perl programming
language and the MySQL programming API that comes with the MySQL relational
database management system. Most functions provided by this programming API
are supported.

%changelog
* Mon Jun 12 2023 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b5ZAPPEND
- ZBUG-3355, Upgraded OpenSSL to 3.0.9
* Wed Dec 02 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b4ZAPPEND
- Upgraded dependency openssl to 1.1.1h
* Thu Sep 10 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b3ZAPPEND
- Upgraded perl-dbd-mysql to 4.050
* Thu Sep 7 2017  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Bug-107311: Updated perl-dbd-mysql version.
* Wed Sep 9 2015 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b1ZAPPEND
- Initial Release.

%define debug_package %{nil}

%prep
%setup -n MODNAME-%{version}

%build
perl -I OZCL/perl5 Makefile.PL INSTALL_BASE=OZC \
 INSTALLSITEMAN1DIR=OZCS/man/man1 INSTALLSITEMAN3DIR=OZCS/man/man3 \
 INSTALLMAN3DIR=OZCS/man/man1 INSTALLVENDORMAN3DIR=OZCS/man/man1 \
 INSTALLMAN3DIR=OZCS/man/man3 INSTALLVENDORMAN3DIR=OZCS/man/man3 \
 LIB=OZCL/perl5  --ssl --nocatchstderr --mysql_config=OZCB/mysql_config \
 --libs="-LOZCL -lmysqlclient -lpthread -lz -lm -lrt -lssl -lcrypto -ldl"
LD_RUN_PATH=OZCL PERL5LIB=OZCL/perl5 make test

# remove .packlist and perllocal.pod
#  $(DESTINSTALLSITEARCH)/auto/$(FULLEXT)/.packlist
#  $(DESTINSTALLSITEARCH)/perllocal.pod
%define perl_archname %(perl -MConfig -e 'print $Config{archname}')
%install
make install DESTDIR=${RPM_BUILD_ROOT}
rm -f %{buildroot}OZCL/perl5/%{perl_archname}/perllocal.pod
rm -f %{buildroot}OZCL/perl5/%{perl_archname}/auto/*/*/.packlist

%files
%defattr(-,root,root)
OZCL
OZCS/man
