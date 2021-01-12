Summary:            Zimbra's Aspell Dutch dictionary
Name:               zimbra-aspell-nl
Version:            VERSION
Release:            1zimbra8.7b2ZAPPEND
License:            Public Domain
Patch0:             aspell-nl.patch
Source:             %{name}-%{version}.tar.bz2
BuildRequires:      zimbra-aspell >= 0.60.8-1zimbra8.7b1ZAPPEND
Requires:           zimbra-aspell >= 0.60.8-1zimbra8.7b1ZAPPEND
AutoReqProv:        no
URL:                http://aspell.net/

%description
The Zimbra Aspell Dutch dictionary

%changelog
* Tue Apr 24 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-1zimbra8.7b2ZAPPEND
- Upgraded dependency aspell to 0.60.8

%define debug_package %{nil}

%prep
%setup -n aspell-nl-ADICT
%patch0 -p1

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g"; export CFLAGS; \
./configure --vars ASPELL=OZCB/aspell \
 WORD_LIST_COMPRESS=OZCB/word-list-compress
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
OZCL/aspell-0.60
