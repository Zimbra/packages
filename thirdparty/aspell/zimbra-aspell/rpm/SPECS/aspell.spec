Summary:            Zimbra's Aspell build
Name:               zimbra-aspell
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            LGPL-2.1
Source:             %{name}-%{version}.tar.gz
BuildRequires:      ncurses-devel
Requires:           ncurses-libs, zimbra-aspell-libs = %{version}-%{release}
AutoReqProv:        no
URL:                http://aspell.net/

%description
The Zimbra Aspell build

%changelog
* Tue Apr 24 2020  Zimbra Packaging Services <packaging-devel@zimbra.com> - VERSION-ITERATIONZAPPEND
- Upgraded aspell to 0.60.8

%prep
%setup -n aspell-%{version}

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g"; export CFLAGS; \
./configure --prefix=OZC
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}

%package libs
Summary:        Aspell Libaries
Requires:       zimbra-spell-base
AutoReqProv:        no

%description libs
The zimbra-aspell-libs package contains the aspell libraries

%package devel
Summary:        Aspell Development
Requires: zimbra-aspell-libs = %{version}-%{release}
AutoReqProv:        no

%description devel
The zimbra-aspell-devel package contains the linking libraries and include files

%files
%defattr(-,root,root)
OZCB
OZCS

%files libs
%defattr(-,root,root)
%dir OZCL/aspell-0.60
OZCL/*.so.*
OZCL/aspell-0.60

%files devel
%defattr(-,root,root)
OZCI
OZCL/*.la
OZCL/*.so

