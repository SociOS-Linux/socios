# Documentation: https://docs.brew.sh/Formula-Cookbook
#                https://rubydoc.brew.sh/Formula
# PLEASE REMOVE ALL GENERATED COMMENTS BEFORE SUBMITTING YOUR PULL REQUEST!
class Socios < Formula
  desc "development formula -Socios"
  homepage "https://github.com/SociOS-Linux/socios"
  url "https://github.com/SociOS-Linux/socios/archive/refs/tags/v1.3.6.tar.gz"
  sha256 "bd1a0143992839b88bd0205d919288ddb08f23c18ffe094dca5abe29b5d19d3f"
  license "GPL-3.0"

  # depends_on "cmake" => :build

  def install
	bin.install "socios"
	prefix.install Dir["lib"]
  end
end
