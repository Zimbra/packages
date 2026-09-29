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

## Adding GNU Aspell language support using a Copilot agent

This repository's `AGENTS.md` provides the workflow for adding GNU Aspell dictionary packages. Open the `packages` repository in a coding agent (Copilot CLI or Copilot desktop app) that reads `AGENTS.md` and ask, for example:

```text
Add Latvian Aspell language support. Use PREAPPS-1234 as the Jira ticket.
```

No separate skill, script, or translation service is required. The agent checks the [official GNU Aspell dictionary catalog](https://ftp.gnu.org/gnu/aspell/dict/) first. A package is added only when the requested dictionary is available there as an official archive; otherwise, the agent reports that it is unavailable and creates no package.

For an available dictionary, the change adds a `thirdparty/aspell-<code>` Debian/RPM packaging wrapper and updates the repository's version definitions, build order, and `zimbra-spell-components` dependencies and changelogs. The upstream archive and extracted dictionary files are downloaded during package builds and are not committed to this repository.

The `AGENTS.md` workflow covers the Jira and Git preflight, verifying the exact upstream archive and package identifiers, packaging conventions, required registration points, and validation. The agent shows its changes and validation results and asks before committing or pushing.

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
