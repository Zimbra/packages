Summary:            Zimbra's Aspell Polish dictionary
Name:               zimbra-aspell-pl
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            GPL-2.0
Source:             %{name}-%{version}.tar.bz2
BuildRequires:      zimbra-aspell
Requires:           zimbra-aspell
AutoReqProv:        no
URL:                http://aspell.net/

%description
The Zimbra Aspell Polish dictionary

%define debug_package %{nil}

%prep
%setup -n aspell6-pl-ADICT

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g"; export CFLAGS; \
./configure --vars ASPELL=OZCB/aspell \
  PREZIP=OZCB/prezip-bin
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
OZCL/aspell-0.60
