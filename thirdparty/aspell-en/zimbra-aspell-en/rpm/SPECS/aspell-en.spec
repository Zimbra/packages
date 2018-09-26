Summary:            Zimbra's Aspell English dictionary
Name:               zimbra-aspell-en
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            BSD
Source:             %{name}-%{version}.tar.bz2
BuildRequires:      zimbra-aspell
Requires:            zimbra-aspell
AutoReqProv:        no
URL:                http://aspell.net/

%description
The Zimbra Aspell English dictionary

%define debug_package %{nil}

%prep
%setup -n aspell6-en-ADICT

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g"; export CFLAGS; \
./configure --vars ASPELL=OZCB/aspell \
  PREZIP=OZCB/prezip-bin
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}
echo "add zimbra.rws" >>${RPM_BUILD_ROOT}OZCL/aspell-0.60/en.multi
echo "add zimbra.rws" >>${RPM_BUILD_ROOT}OZCL/aspell-0.60/en_US.multi

%files
%defattr(-,root,root)
OZCL/aspell-0.60
