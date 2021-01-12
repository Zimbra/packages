Summary:            swatchdog - Simple Log Watcher
Name:               zimbra-perl-MODNORMNAME
Version:            VERSION
Release:            1zimbra8.7b2ZAPPEND
License:            GPL-2
Source:             %{name}-%{version}.tar.gz
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
BuildRequires:      zimbra-perl-base, zimbra-perl-date-calc >= 6.4-1zimbra8.7b2ZAPPEND, zimbra-perl-file-tail
BuildRequires:      zimbra-perl-date-manip, zimbra-perl-timedate
Requires:           zimbra-perl-base, zimbra-perl-date-calc >= 6.4-1zimbra8.7b2ZAPPEND, zimbra-perl-file-tail
Requires:           zimbra-perl-date-manip, zimbra-perl-timedate
AutoReqProv:        no
URL:                http://sourceforge.net/projects/swatch/

%description
swatchdog.pl started out as swatch, the "simple watchdog" for activity
monitoring log files produced by UNIX's syslog facility. It has since
been evolving into a utility that can monitor just about any type of
log. The name has been changed to satisfy a request made by the old
Swiss watch company.

%changelog
* Sat Apr 25 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Updated dependency perl-date-calc

%define debug_package %{nil}

%prep
%setup -n MODNAME-%{version}

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
rm -rf %{buildroot}OZCL/perl5/%{perl_archname}

%files
%defattr(-,root,root)
OZCL
OZCS/man
OZCB
