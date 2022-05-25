# How to publish a release

TL;DR: Releases are published automatically whenever a new tag of the format X.Y.Z is pushed to the GitHub repository.

## Create a tag and release draft

All you have to do is create and push a new tag.

In the command below, replace `<MAJOR.MINOR.PATCH>` with the actual version number you want to publish.

```nohighlight
export VERSION=<MAJOR.MINOR.PATCH>
git checkout master
git pull
git tag -a ${VERSION} -m "Release version ${VERSION}"
git push origin ${VERSION}
```

This will push your the new tag to the GitHub repository where it will show up as a tag without release.

Follow CircleCI's progress in [https://circleci.com/gh/socios-linux/socios](https://circleci.com/gh/socios-linux/socios). Do not do anything until CI is finished.

CircleCI should have created a new Release draft. Edit this draft.

## Edit the release draft and publish

Open the [release draft](https://github.com/socios-linux/socios/releases/) on Github.

Edit the description to inform about what has changed since the last release. Save and publish the release.

The release draft will attach itself to the tag you've pushed in the first step.

## Release docs

The socios-installer reference docs have not yet been published  [to-do]

To update this, read the [Deploying](https://github.com/socios-linux/socios/docs) section in the socios-linux/docs.

## Prerequisites

CircleCI must be set up with certain environment variables:

- `CODE_SIGNING_CERT_BUNDLE_BASE64` - Base64 encoded PKCS#12 key/cert bundle used for signing binaries
- `CODE_SIGNING_CERT_BUNDLE_PASSWORD` - Password for the above bundle
- `RELEASE_TOKEN` - A GitHub token with the permission to write to repositories
  - [socios-linux/socios](https://github.com/socios-linux/socios)
  - [socios-linux/sociosbrew-tap](https://github.com/socios-linux/sociosbrew-tap)
- `GITHUB_USER_EMAIL` - Email address of the github user owning the personal token above
- `GITHUB_USER_NAME` - Username of the above github user
