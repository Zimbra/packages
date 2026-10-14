Summary:            Zimbra's Aspell Kinyarwanda dictionary
Name:               zimbra-aspell-rw
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            GPL-2.0-or-later
Source:             %{name}-%{version}.tar.bz2
BuildRequires:      zimbra-aspell
Requires:           zimbra-aspell
AutoReqProv:        no
URL:                http://aspell.net/

%description
The Zimbra Aspell Kinyarwanda dictionary

%define debug_package %{nil}

%prep
%setup -n aspell-rw-ADICT

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
