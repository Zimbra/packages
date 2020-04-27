Summary:            innotop - mariadb monitor
Name:               zimbra-perl-MODNORMNAME
Version:            VERSION
Release:            1zimbra8.7b2ZAPPEND
License:            GPL-2
Source:             %{name}-%{version}.tar.gz
Patch0:             inno.patch
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
BuildRequires:      zimbra-perl-base, zimbra-perl-dbd-mysql >= 4.043-1zimbra8.7b2ZAPPEND, zimbra-perl-term-readkey
Requires:           zimbra-perl-base, zimbra-perl-dbd-mysql >= 4.043-1zimbra8.7b2ZAPPEND, zimbra-perl-term-readkey
AutoReqProv:        no
URL:                https://github.com/innotop/innotop

%description
innotop monitors MySQL/MariaDB servers.  Each of its modes shows you a different
aspect of what's happening in the server.  For example, there's a mode for monitoring
replication, one for queries, and one for transactions.  innotop refreshes its
data periodically, so you see an updating view.

%changelog
* Sat Apr 25 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Updated dependency zimbra-perl-dbd-mysql

%define debug_package %{nil}

%prep
%setup -n MODNAME-%{version}
%patch0 -p1

%build
perl -I OZCL/perl5 Makefile.PL INSTALL_BASE=OZC \
 INSTALLSITEMAN1DIR=OZCS/man/man1 INSTALLSITEMAN3DIR=OZCS/man/man3 \
 INSTALLMAN3DIR=OZCS/man/man1 INSTALLVENDORMAN3DIR=OZCS/man/man1 \
 INSTALLMAN3DIR=OZCS/man/man3 INSTALLVENDORMAN3DIR=OZCS/man/man3 \
 LIB=OZCL/perl5
PERL5LIB=OZCL/perl5 make test

# remove .packlist and perllocal.pod
#  $(DESTINSTALLSITEARCH)/auto/$(FULLEXT)/.packlist
#  $(DESTINSTALLSITEARCH)/perllocal.pod
%define perl_archname %(perl -MConfig -e 'print $Config{archname}')
%install
make install DESTDIR=${RPM_BUILD_ROOT}
rm -rf %{buildroot}OZCL

%files
%defattr(-,root,root)
OZCB
OZCS/man
