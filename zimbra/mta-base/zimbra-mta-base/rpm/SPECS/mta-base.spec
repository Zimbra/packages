Summary:            Zimbra MTA Base
Name:               zimbra-mta-base
Version:            1.0.1
Release:            ITERATIONZAPPEND
License:            GPL-2
Packager:           Zimbra Packaging Services <packaging-devel@zimbra.com>
Group:              Development/Languages
Requires:           zimbra-base
AutoReqProv:        no

%define debug_package %{nil}

%description
Zimbra MTA Base is used as a simple method to allow removing
all the zimbra-mta specific packages

%files

%changelog
* Tue Dec 15 2015  Zimbra Packaging Services <packaging-devel@zimbra.com> - 1.0.1
- Create postfix user and group and postdrop group

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

grp_exists postfix
if [ $? != 0 ]; then
        groupadd -r postfix
fi

grp_exists postdrop
if [ $? != 0 ]; then
        groupadd -r postdrop
fi

acct_exists postfix
if [ $? != 0 ]; then
        useradd -r -g postfix -d /opt/zimbra/postfix postfix
        if [ -L /opt/zimbra/postfix ]; then
            /bin/rm -rf /opt/zimbra/postfix
        fi
fi
usermod -a -G postfix,tty zimbra
