class ItsMagic < Formula
  desc "its-magic - AI dev team workflow"
  homepage "https://github.com/USER/its-magic"
  # UPDATE: url and sha256 after each release
  url "https://github.com/fl0wm0ti0n/gsd_cursor/archive/refs/tags/v0.1.1.tar.gz"
  sha256 "0c728dc21b0eb4a2e62bd8a4ad40298d618f3ce2b70d0eaef567c8f701e3cd2e"
  license "MIT"

  depends_on "node"

  def install
    libexec.install Dir["*"]
    bin.install_symlink libexec/"bin/its-magic.js" => "its-magic"
  end

  test do
    system "#{bin}/its-magic", "--help"
  end
end

