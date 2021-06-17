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

## Structural changes in packages repo with respect to nginx code:
- Following to the upgraded Zimbra nginx 1.20.0, packages repo no more contains nginx specific code.
- To do same forked repo from upstream nginx is maintained as [Zimbra/nginx](https://github.com/Zimbra/nginx/tree/zimbra/develop)
- Packages repo references Zimbra/nginx repo as submodule.

## Steps to add submodule [Zimbra/nginx](https://github.com/Zimbra/nginx/tree/zimbra/develop) for nginx compilation:
- Clone packages repo as usual.
- cd packages.
- pull nginx submodule using 

    git submodule update --init --recursive --remote

Once those are checked out at the same level you can enter a sub-directory to build that package.

## Guide: Compilation for nginx
    Clone the repos
    cd packages
    git submodule update --init --recursive --remote

    cd packages/thirdparty/nginx
    make build

    ls -ltr build/UBUNTU16_64/

    src
    zimbra-nginx_1.19.0.orig.tar.gz
    zimbra-nginx_1.19.0-1zimbra8.8b1.16.04.tar.xz
    zimbra-nginx_1.19.0-1zimbra8.8b1.16.04.dsc
    zimbra-nginx
    zimbra-nginx_1.19.0-1zimbra8.8b1.16.04_amd64.deb
    zimbra-nginx-dbg_1.19.0-1zimbra8.8b1.16.04_amd64.deb
    zimbra-nginx_1.19.0-1zimbra8.8b1.16.04_amd64.changes
