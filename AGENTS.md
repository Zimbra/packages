# Agent guidance for Zimbra packages

## Adding GNU Aspell language support

When a new language is added to a Zimbra user interface, check whether the official GNU Aspell
dictionary catalog provides a dictionary for that language:

```text
https://ftp.gnu.org/gnu/aspell/dict/
```

Only add an Aspell package when that official catalog contains a downloadable `.tar.bz2`
dictionary archive for the requested language. If no official archive exists, report that
Aspell support is unavailable and do not create a `thirdparty/aspell-*` directory. Do not use
an unofficial mirror, a related language, or a different regional variant as a substitute.

The Aspell directories in this repository are packaging wrappers around upstream dictionaries.
They do not contain translated Zimbra messages, and agents must not create or edit dictionary
word lists.

### Required Git workflow

For a six-repository language rollout started in `zm-x-web`, its up-front
`preflight-new-language.js` checks this checkout and selects the ticket branch
**before any** repository starts translation. Do not run a second branch-creation preflight here
after the UI repositories have been changed; verify the checkout is still on that clean
ticket branch before adding a package. The same ticket and separate commit/push approvals
apply. For a standalone Aspell package change, follow this workflow:

1. Ask the user for the Jira ticket number. Do not create a working branch until the user
   provides it. Use the ticket number as the branch name unless the user requests another
   repository-approved branch name.
2. Check the working tree with `git status`. If any staged or unstaged tracked changes are
   present, report them and stop. Do not stash, reset, clean, commit, or discard the existing
   work on the user's behalf.
3. Report unrelated untracked files and stop when they could conflict with the planned work.
   Never delete or overwrite them.
4. Fetch the latest `origin/develop`, the base branch of this repository.
5. If the ticket branch is new, create it directly from the fetched `origin/develop`. Do not
   switch or reset the local `develop` branch to make it current.
6. If the ticket branch already exists locally or remotely, reuse it only when it contains
   the latest `origin/develop`. Stop and ask if it is behind or diverged; never overwrite,
   merge, rebase, or force-update it automatically.
7. Make and validate the Aspell changes on the ticket branch only.
8. Show the user the changed files, validation results, and proposed commit before publishing.
9. Commit only after the user confirms that the changes are ready to commit.
10. Ask for separate explicit confirmation before pushing the branch to the remote. Never push
    automatically and never force-push.

Read-only analysis, including checking the official GNU catalog, may be performed before branch
creation. Any repository file modification must wait until the preflight and ticket branch are
complete.

### Confirm identifiers before editing

Do not assume these identifiers are the same:

- Zimbra UI locale
- GNU Aspell dictionary directory
- upstream archive prefix
- extracted archive directory
- Zimbra package suffix

Examples:

- Catalan uses package suffix `ca` and archive prefix `aspell6-ca`.
- Danish uses archive prefix `aspell5-da`.
- French, Dutch, and Swedish use archive prefixes such as `aspell-fr`, without `aspell6`.
- Brazilian Portuguese uses upstream code `pt_BR` but Zimbra package suffix `pt-br`.

Inspect the official directory and archive before choosing identifiers. If more than one
dictionary or regional variant could match the requested locale, ask the user which one to use.

### Inspect the upstream archive

Before creating files:

1. Verify the exact official archive URL exists.
2. Record the archive's version and top-level extracted directory.
3. Inspect its `Copyright`, `COPYING`, `README`, `info`, and build metadata when present.
4. Determine its actual license and copyright holders.
5. Check whether it uses the normal `PREZIP` configuration or needs a different build helper.

Treat downloaded archives as untrusted input. Inspect their listing before extraction, do not
execute archive scripts during analysis, and do not extract entries outside a dedicated
temporary directory.

Never copy license, copyright, archive naming, or build details from another language without
verifying them against the selected upstream archive. Existing packages use several different
licenses and build patterns.

### Package structure

Follow a comparable **current** package. Start from the most recently added Aspell package,
not an older one such as Swedish, because older packages carry legacy values (old copyright
years, old release strings, and settings that no longer agree with each other).

**A copy is not verified.** Every line you leave unchanged in a copied package was never
checked for the new language. After copying, diff the new package against its model and review
each line that stayed identical, not only the ones you edited. In particular:

- `debian/compat` is `N`, so `debian/control` must require `debhelper (>= N)` or newer. Never
  keep a lower `debhelper` minimum than the `compat` level. Existing packages currently have
  `compat` 10 with `debhelper (>= 9)`; do not copy that mismatch into a new package.
- The `debian/*` copyright year is the year the package is added, not the model's year.
- The dictionary's `Copyright` holders and license come from the new archive, never from the
  model (this is already required below; check it again after copying).
- `debian/watch`, the Makefile URL, and the RPM `%setup -n` directory match the new archive's
  official filename and top-level directory.
- Debian `Depends` and RPM `Requires` use the same package name and version constraints.

A normal package has this structure:

```text
thirdparty/aspell-<package-code>/
├── Makefile
└── zimbra-aspell-<package-code>/
    ├── debian/
    │   ├── changelog
    │   ├── compat
    │   ├── control
    │   ├── copyright
    │   ├── rules
    │   ├── source/
    │   │   └── format
    │   ├── watch
    │   └── zimbra-aspell-<package-code>.install
    └── rpm/
        └── SPECS/
            └── aspell-<package-code>.spec
```

Use current repository conventions rather than copying historical values literally.

#### `Makefile`

Define:

- `pvers` using the normalized version from `versions.def`
- `dictver` using the exact upstream archive version
- the Zimbra package name
- the exact upstream archive prefix and filename
- the official GNU download URL

The URL and filename must match the official archive exactly. Preserve upstream capitalization
and underscores, such as `pt_BR`.

#### Debian package metadata

- `debian/control` defines `zimbra-aspell-<package-code>` and depends on `zimbra-aspell`.
- `debian/copyright` records the selected dictionary's real authors and license.
- `debian/rules` configures and installs the dictionary using Zimbra's Aspell paths.
- `debian/watch` matches the exact official directory, archive prefix, and version syntax.
- `debian/zimbra-aspell-<package-code>.install` normally installs
  `opt/zimbra/common/lib/aspell-0.60`; confirm this against current packages.
- `debian/compat` and `debian/source/format` must follow current repository convention.

#### RPM package metadata

The RPM spec must define the matching `zimbra-aspell-<package-code>` package, correct license,
dependency on `zimbra-aspell`, and current Zimbra paths.

The `%setup -n` directory must match the archive's actual top-level directory after repository
version substitution. Do not assume every archive expands to `aspell6-<code>-<version>`.

Add a patch only when the unchanged official archive fails for an understood and documented
reason. Keep Debian and RPM behavior consistent.

### Repository registration

Creating the package directory is not sufficient. Update every registration point:

1. `versions.def`
   - Add `ASPELL-<CODE>_VERSION` with the exact upstream archive version.
   - Add `ASPELL-<CODE>_NORM` with the normalized package version used by this repository.
   - Follow comparable entries when converting upstream hyphens or underscores.
2. `build-order`
   - Add `thirdparty/aspell-<package-code>` beside the other Aspell dictionaries.
3. `zimbra/spell-components/zimbra-spell-components/debian/control`
   - Add `zimbra-aspell-<package-code>` to `Depends`.
4. `zimbra/spell-components/zimbra-spell-components/debian/changelog`
   - Add a new entry and increment the spell-components version according to current
     repository convention.
5. `zimbra/spell-components/zimbra-spell-components/rpm/SPECS/spell-components.spec`
   - Add the package to `Requires`.
   - Increment the spell-components version.
   - Add the matching changelog entry.

Search the repository for a comparable existing Aspell package before finishing. Include any
additional registration point introduced after this guidance was written.

### Validation

Do not report the language as supported based only on the presence of new files.

At minimum:

1. Verify the configured official URL downloads the intended archive.
2. Confirm the archive's top-level directory matches the RPM `%setup` value.
3. Confirm Debian and RPM package names match all spell-component dependency references.
4. Confirm version placeholders and normalized versions follow current substitution rules.
5. Confirm the package occurs exactly once in `build-order`.
6. Build both Debian and RPM packages when the required build environments are available.
7. If installation testing is available, confirm files install into the current Aspell data
   directory and Zimbra's Aspell binary discovers the dictionary.
8. Run a small spelling check using the installed dictionary code.

Report unavailable build or installation environments as not run. Never describe a skipped
check as passed.

### Reference implementation

Use [Zimbra/packages#149](https://github.com/Zimbra/packages/pull/149), which added Catalan, as
a reference for the overall change surface:

- `thirdparty/aspell-ca`
- `versions.def`
- `build-order`
- Debian spell-components dependency and changelog
- RPM spell-components dependency, version, and changelog

The pull request is a historical example, not a template whose versions, compatibility level,
license, dates, or archive names should be copied unchanged.
