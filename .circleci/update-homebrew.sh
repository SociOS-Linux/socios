#!/bin/bash

# This script creates a homebrew formula for the Mac OS binary release
# and pushes it to the right repository "sociosbrew-tap"

set -o errexit
set -o nounset
set -o pipefail

# Our version number
VERSION=$1

REPO_URL="https://${RELEASE_TOKEN}@github.com/socios-linux/sociosbrew-tap.git"

# SHA256 hash of the tar.gz file
SHA256=$(openssl dgst -sha256 bin-dist/socios-$VERSION-darwin-amd64.tar.gz|awk '{print $2}')

git clone --depth 1 $REPO_URL
cd sociosbrew-tap/Formula

# Dump formula ruby code
cat > socios.rb << EOF
require "formula"
# This file is generated automatically by
# https://github.com/socios-linux/socios/blob/master/.circleci/update-homebrew.sh
class Socios < Formula
  desc "installs socios homebrew installer"
  homepage "https://github.com/socios-linux/socios"
  url "https://github.com/socios-linux/socios/releases/download/$VERSION/socios-$VERSION-darwin-amd64.tar.gz"
  version "$VERSION"
  # openssl dgst -sha256 <file>
  sha256 "$SHA256"
  def install
    bin.install "socios"
  end
end
EOF

git config credential.helper 'cache --timeout=120'
git config user.email "${GITHUB_USER_EMAIL}"
git config user.name "${GITHUB_USER_NAME}"
git add socios.rb
git commit -m "Update socios to ${VERSION}"

# Push quietly with -q to prevent showing the token in log
git push -q $REPO_URL master
