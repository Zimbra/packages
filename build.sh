#!/bin/bash
# Before ackaging run: spec_required.sh to remove non-Zimbra packages from
# dependencies.
# List installed packages: rpm -qa
# Remove all RPMs: rpm -e $(rpm -qa)

title='\033]0;'
titleend='\007'
txtgreen='\033[1;32m'
txtreset='\033[00m'

PACKAGES_DIR=$(pwd)
if [ -f "$PACKAGES_DIR/last-built" ] ; then
  SKIP=1
  read LAST_BUILT < "$PACKAGES_DIR/last-built"
  echo -e "Skipping enabled, starting after $txtgreen $LAST_BUILT $txtreset"
else
  SKIP=0
fi

cat 'build-order' | while read DIR ; do
  if [ ! -d "$PACKAGES_DIR/$DIR" ]; then continue ; fi
  if [ "$SKIP" -eq 1 ] ; then
    if [[ "x$DIR" == "x$LAST_BUILT" ]]; then SKIP=0 ; fi
    continue
  fi
  echo -e "$txtgreen----- BUILDING $DIR -----$txtreset"
  echo -e "$title$DIR$titleend"
  PACKAGE=${DIR##*/}
  cd "$PACKAGES_DIR/$DIR"
  make clean
  make >/dev/null
  result=$?
  if [ $result -ne 0 ]; then
    echo "ERROR, aborting"
    exit 255
  fi
  sudo rpm -iv --nodeps --replacefiles "$PACKAGES_DIR/$DIR/build/GENTOO_64/*/rpm/RPMS/x86_64/*.rpm"
  if [ $result -ne 0 ]; then
    echo "ERROR, aborting"
    exit 255
  fi
  echo "$DIR" > "$PACKAGES_DIR/last-built"
done

