# packages
ZCS Third Party Dependency Build System

This is the official repository for building out the third party dependencies for Zimbra Collaboration Suite 8.7 and later.

Issues should be reported via [Zimbra's bugzilla](https://bugzilla.zimbra.com)

To build the packages in this repository please checkout the following repositories:

  - packages            git@github.com:Zimbra/packages.git
  - zimbra-build        git@github.com:Zimbra/zimbra-build.git
  - zimbra-package-stub git@github.com:Zimbra/zimbra-package-stub.git

Install the build pre-requisites:

    sudo apt install m4 libpcre3-dev

Once those are checked out at the same level you can enter a sub-directory to build that package.

Example:

    cd packages/thirdparty/nginx
    make build

    ls build/UBUNTU16_64/

    src
    zimbra-nginx
    zimbra-nginx-dbg_1.7.1-1zimbra8.7b11.16.04_amd64.deb
    zimbra-nginx_1.7.1-1zimbra8.7b11.16.04.dsc
    zimbra-nginx_1.7.1-1zimbra8.7b11.16.04.tar.xz
    zimbra-nginx_1.7.1-1zimbra8.7b11.16.04_amd64.changes
    zimbra-nginx_1.7.1-1zimbra8.7b11.16.04_amd64.deb
    zimbra-nginx_1.7.1.orig.tar.gz
