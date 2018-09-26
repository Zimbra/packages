Summary:            Zimbra's rsync build
Name:               zimbra-rsync
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            GPL-3
Source:             %{name}-%{version}.tar.gz
BuildRequires:      popt-devel
Requires:  zimbra-base
AutoReqProv:        no
URL:                https://rsync.samba.org

%description
The Zimbra rsync build

%prep
%setup -n rsync-%{version}

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g"; export CFLAGS; \
./configure --prefix=OZC \
  --localstatedir=$(ZIMBRA_HOME)/data/tmp
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
OZCB
OZCS
