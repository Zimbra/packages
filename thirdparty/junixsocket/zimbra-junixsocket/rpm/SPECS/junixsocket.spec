Summary:            Zimbra's junixsocket build
Name:               zimbra-junixsocket
Version:            2.0.4
Release:            1zimbra9.0b1
BuildRequires:      maven
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
mvn -P with-native package

%install
mkdir -p $RPM_BUILD_ROOT/opt/zimbra/common/lib
cp junixsocket-native/target/nar/junixsocket-native-2.0.4-amd64-Linux-gpp-jni/lib/amd64-Linux-gpp/jni/libjunixsocket-native-2.0.4.so $RPM_BUILD_ROOT/opt/zimbra/common/lib
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

%package jars
Summary:        junixsocket JAR's
AutoReqProv:        no

%package lib
Summary:        junixsocket Libaries
AutoReqProv:        no

%description jars
The zimbra-junixsocket-jars package contains the junixsocket JAR's

%description lib
The zimbra-junixsocket-lib package contains the junixsocket libraries

%files jars
/opt/zimbra/lib/jars/*.jar
/opt/zimbra/lib/jars/*.nar
/opt/zimbra/jetty/common/lib/*.jar
/opt/zimbra/jetty/common/lib/*.nar

%files lib
%defattr(-,root,root)
/opt/zimbra/common/lib/*.so
