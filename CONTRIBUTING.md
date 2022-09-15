# Contributing to Process 360 Python SDK
To contribute to *Process 360* Python SDK project, please review this document.
## Main branches
Project branch naming is based
en [gitflow workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow).
Project is made of those branches :
- `master` → production branch
- `dev` → new features branch
- `release/<version>` → to test and fix bugs before merging new features or bug fixes in `master`
- `<type>/xxx` → cf. Developing branches
## Developing branches
- It is forbidden to commit without review on `master`, `dev` and `release/*`.
- Release branches are named `release/<version>` where `version` is the future application version.
- Feature branches are named `feat/<feat id>_<my-description>` (eg: `feat/PROC-302_my-awesome-feature` ) where :
    - `feat id` is the issue id in Jira
    - `my-description` is a short description in lowercase with dashes
- Bug fixing branches are named `fix/<bug id>_<my-description>` (eg: `fix/PROC-312_scarry-bug` ) where :
    - `bug id` is the issue id in Jira
    - `my-description` is a short description in lowercase with dashes
- It is possible to create other branches types with default types defined
  in [commitlint](https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional) (
  exemple: `perf/21_my-description`).
## Hot fix
1. create a release branch from `master`
2. create a fix branch from release branch
3. merge fix to release
4. cherry-pick fix commit on `dev`
5. create version commit on release
6. merge to `master` → tag creation from `master` (eg: `1.5.1` )
## Commit message
- Every commit messages must be compliant with [Conventional Commit](https://www.conventionalcommits.org/fr)
- Project specific rules are defined in `.commitlintrc.json` in root folder
- You can install a plugin for [IntelliJ](https://plugins.jetbrains.com/plugin/14046-commitlint-conventional-commit) to
  help to write commit messages
- BREAKING CHANGE is only used from public API
- During merge request creation:
    - MR title must be conventional commits compatible
    - for tasks or features footer must contain reference to Jira : `Implements: PROC-<id>` (
      exemple : `Implements: PROC-75` ) where `id` is an issue id in Jira
    - for bugs, footer must contain reference to Jira : `Closes: PROC-<id>` (exemple: `Closes: PROC-34` ) where `id` is
      an issue id in Jira
## Merge request
- all merge request (MR) must be reviewed by a pear
- before MR creation, the developer must change issue status *Review* in Jira
- at MR creation, the developer must assign a reviewer
- after review:
    - if all is OK, reviewer merge the branch
    - if there are comments, reviewer assign MR to developer
- when merge is passed, developer must test the fix/feature on dev environment and change issue status to `Done`
## New release
1. create `release/x.x.x` from `master`
2. merger `dev` to release branch (`merge origin/dev --no-ff`)
3. update application version (`x.x.x-rc.1`)
### Integration platform update
Update integration platform based
on [version file](https://gitlab.com/logpickr/logpickr-infrastructure/-/blob/master/Plateformes.md).
## Version commit
- update version in XXXX files
- changelog generation:
    - `git fetch --all --tags`
    - if needed, install `conventional-changelog-cli` with : `npm install -g conventional-changelog-cli`
      or `sudo npm install -g conventional-changelog-cli`
    - run `conventional-changelog -p angular -i CHANGELOG.md -s`
    - check that `CHANGELOG.md` is updated
    - add application number in changelog before the date
