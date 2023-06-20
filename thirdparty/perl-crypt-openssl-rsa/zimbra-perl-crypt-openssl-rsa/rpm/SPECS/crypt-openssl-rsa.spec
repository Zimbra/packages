Summary:            Zimbra's Crypt::OpenSSL::RSA build
Name:               zimbra-perl-crypt-openssl-rsa
Version:            VERSION
Release:            1zimbra8.8b1ZAPPEND
License:            GPL-2
Source:             %{name}-%{version}.tar.gz
BuildRequires:      zimbra-perl-base, zimbra-openssl-devel >= 3.0.9-1zimbra8.8b1ZAPPEND
Requires:           zimbra-perl-base, zimbra-openssl-libs >= 3.0.9-1zimbra8.8b1ZAPPEND
AutoReqProv:        no
URL:                http://search.cpan.org/dist/Crypt-OpenSSL-RSA/

%define perl_archname %(eval "`perl -V:archname`"; echo $archname)

%description
The Zimbra Crypt::OpenSSL::RSA build

%define debug_package %{nil}

%changelog
* Mon Jun 12 2023 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.8b1ZAPPEND
- ZBUG-3355, Upgraded OpenSSL to 3.0.9 and Upgraded Crypt::OpenSSL::RSA to 0.33
* Wed Dec 02 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Upgraded dependency openssl to 1.1.1h
* Thu Sep 10 2020 Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-ITERATIONZAPPEND
- Upgraded perl-crypt-openssl-rsa to 0.31

%prep
%setup -n Crypt-OpenSSL-RSA-%{version}

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g"; export CFLAGS; \
perl -I OZCL/perl5 Makefile.PL INSTALL_BASE=OZC \
 INSTALLSITEMAN1DIR=OZCS/man/man1 INSTALLSITEMAN3DIR=OZCS/man/man3 \
 LIB=OZCL/perl5 LIBS="-LOZCL -lssl -lcrypto" INC="-IOZCI"
LD_RUN_PATH=OZCL make

%install
make install DESTDIR=${RPM_BUILD_ROOT}
rm -f %{buildroot}OZCL/perl5/%{perl_archname}/perllocal.pod
rm -f %{buildroot}OZCL/perl5/%{perl_archname}/auto/*/*/*/.packlist

%files
%defattr(-,root,root)
OZCL
OZCS/man
