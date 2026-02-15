class ItsMagicBeta < Formula
  desc "its-magic - AI dev team workflow (beta)"
  homepage "https://github.com/USER/its-magic"
  # UPDATE: url and sha256 after each beta release
  url "https://github.com/fl0wm0ti0n/gsd_cursor/archive/refs/tags/v0.1.2-5.tar.gz"
  sha256 "d83d466ea9ad8d43740edefcc037e649ef88e7ef52d2954ca042a32d7d2cb938"
  version "0.1.2-5"
  license "MIT"

  depends_on "node"

  conflicts_with "its-magic", because: "beta and stable share the same binary"

  def install
    libexec.install Dir["*"]
    bin.install_symlink libexec/"bin/its-magic.js" => "its-magic"
  end

  test do
    system "#{bin}/its-magic", "--help"
  end
end











