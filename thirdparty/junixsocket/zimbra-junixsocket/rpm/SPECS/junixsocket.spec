Summary:            Zimbra's junixsocket build
Name:               zimbra-junixsocket
Version:            VERSION
Release:            ITERATIONZAPPEND
Requires:           zimbra-base
BuildRequires:      zimbra-maven
License:            Apache-2.0
Source:             %{name}-%{version}.tgz
URL:                https://github.com/kohlschutter/junixsocket

%description
The Zimbra junixsocket build

%prep
%setup -n junixsocket-%{version}

%build
LDFLAGS="-Wl,-rpath,/opt/zimbra/common/lib"; export LDFLAGS; \
CFLAGS="-fPIC -O2 -g"; export CFLAGS; \
mvn -Dmaven.repo.local=%{buildroot}/.m2/repository -P with-native package

# This does generate a lib but it isn't clear how to get maven to generate
# libraries for debug. junixsocket also doesn't deliever any .so files only
# .nar files which hold the .so so it isn't exactly clear what expectations
# are for this context. Because of this just going to block generation for now
# since the current default generated package contains nothing.
%global debug_package %{nil}

%install
mkdir -p $RPM_BUILD_ROOT/opt/zimbra/lib/jars
cp junixsocket-native-common/target/*.jar $RPM_BUILD_ROOT/opt/zimbra/lib/jars
cp junixsocket-mysql/target/*.jar $RPM_BUILD_ROOT/opt/zimbra/lib/jars
cp junixsocket-common/target/*.jar $RPM_BUILD_ROOT/opt/zimbra/lib/jars
cp junixsocket-rmi/target/*.jar $RPM_BUILD_ROOT/opt/zimbra/lib/jars
cp junixsocket-demo/target/*.jar $RPM_BUILD_ROOT/opt/zimbra/lib/jars
cp junixsocket-native/target/*.jar $RPM_BUILD_ROOT/opt/zimbra/lib/jars
cp junixsocket-native/target/*.nar $RPM_BUILD_ROOT/opt/zimbra/lib/jars
mkdir -p $RPM_BUILD_ROOT/opt/zimbra/jetty/common/lib
cp junixsocket-native-common/target/*.jar $RPM_BUILD_ROOT/opt/zimbra/jetty/common/lib
cp junixsocket-mysql/target/*.jar $RPM_BUILD_ROOT/opt/zimbra/jetty/common/lib
cp junixsocket-common/target/*.jar $RPM_BUILD_ROOT/opt/zimbra/jetty/common/lib
cp junixsocket-rmi/target/*.jar $RPM_BUILD_ROOT/opt/zimbra/jetty/common/lib
cp junixsocket-demo/target/*.jar $RPM_BUILD_ROOT/opt/zimbra/jetty/common/lib
cp junixsocket-native/target/*.jar $RPM_BUILD_ROOT/opt/zimbra/jetty/common/lib
cp junixsocket-native/target/*.nar $RPM_BUILD_ROOT/opt/zimbra/jetty/common/lib

%files
/opt/zimbra/lib/jars/*.jar
/opt/zimbra/lib/jars/*.nar
/opt/zimbra/jetty/common/lib/*.jar
/opt/zimbra/jetty/common/lib/*.nar
