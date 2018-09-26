Summary:            Zimbra Base
Name:               zimbra-base
Version:            1.0.1
Release:            ITERATIONZAPPEND
License:            GPL-2
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
AutoReqProv:        no

%define debug_package %{nil}

%description
Zimbra Base is used as a simple method to allow removing
all the zimbra specific third party packages.

%files

%changelog
* Tue Dec 15 2015  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.1
- Create zimbra user and group
- Add dependencies for useradd/usermod/adduser

%post -p /bin/bash
grp_exists() {
  if [ -x /usr/bin/getent ]
  then
    getent group $1 >/dev/null 2>&1
    FOUND=$?
  else
    egrep -q "^$1:" /etc/group
    FOUND=$?
  fi
  return $FOUND
}

acct_exists() {
  if [ -x /usr/bin/getent ]
  then
    getent passwd $1 >/dev/null 2>&1
    return $?
  else
    egrep -q "^$1:" /etc/passwd
    return $?
  fi
}

grp_exists zimbra
if [ $? != 0 ]; then
        groupadd -r zimbra
fi

acct_exists zimbra
if [ $? != 0 ]; then
        useradd -r -g zimbra -G tty -d /opt/zimbra -s /bin/bash zimbra
else
        usermod -g zimbra -d /opt/zimbra -s /bin/bash zimbra
fi
