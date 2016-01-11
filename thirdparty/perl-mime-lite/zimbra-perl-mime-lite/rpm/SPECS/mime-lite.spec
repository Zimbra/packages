Summary:            MIME-Lite - low-calorie MIME generator
Name:               zimbra-perl-mime-lite
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            GPL+ or Artistic
Source:             %{name}-%{version}.tar.gz
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
BuildRequires:      zimbra-perl-base, zimbra-perl-mime-types, zimbra-perl-email-date-format
BuildRequires:      zimbra-perl-mailtools
Requires:           zimbra-perl-base, zimbra-perl-mime-types, zimbra-perl-email-date-format
Requires:           zimbra-perl-mailtools
AutoReqProv:        no
URL:                https://metacpan.org/release/MIME-Lite

%description
Create and send using the default send method for your OS a single-part
message.

%define debug_package %{nil}

%prep
%setup -n MIME-Lite-%{version}

%build
perl -I OZCL/perl5 Makefile.PL INSTALL_BASE=OZC \
 INSTALLSITEMAN1DIR=OZCS/man/man1 INSTALLSITEMAN3DIR=OZCS/man/man3 \
 INSTALLMAN3DIR=OZCS/man/man3 \
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
