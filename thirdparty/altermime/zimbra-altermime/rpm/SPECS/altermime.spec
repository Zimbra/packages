Summary:            Zimbra's altermime build
Name:               zimbra-altermime
Version:            VERSION
Release:            ITERATIONZAPPEND
License:            BSD
Source:             %{name}-%{version}.tar.gz
Patch0:             makefile_nowerror.patch
Patch1:             null.patch
Requires:           zimbra-mta-base
AutoReqProv:        no
URL:                http://www.pldaniels.com/altermime/

%description
The Zimbra altermime build

%prep
%setup -n altermime-0.3-dev
%patch0 -p1
%patch1 -p1

%build
LDFLAGS="-Wl,-rpath,OZCL"; export LDFLAGS; \
CFLAGS="-O2 -g"; export CFLAGS; \
make

%install
mkdir -p ${RPM_BUILD_ROOT}OZCB
cp -f altermime ${RPM_BUILD_ROOT}OZCB

%files
%defattr(-,root,root)
OZCB
