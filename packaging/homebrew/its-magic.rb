# typed: strict
# frozen_string_literal: true

# Homebrew formula for the its-magic CLI installer.
class ItsMagic < Formula
  desc "AI development workflow toolkit for multi-agent teams"
  homepage "https://github.com/USER/its-magic"
  # UPDATE: url, version, and sha256 after each release (`curl -sL <url> | shasum -a 256`)
  url "https://github.com/fl0wm0ti0n/its-magic/archive/refs/tags/v0.1.2-35.tar.gz"
  version "0.1.2-35"
  # UPDATE sha256 when the tag tarball is published: curl -sL <url> | shasum -a 256
  sha256 "0000000000000000000000000000000000000000000000000000000000000000"
  license "MIT"

  def install
    libexec.install Dir["*"]
    # Create a shell wrapper that calls installer.sh directly (no Node.js needed)
    (bin/"its-magic").write <<~SH
      #!/bin/bash
      exec sh "#{libexec}/installer.sh" "$@"
    SH
    chmod 0755, bin/"its-magic"
  end

  def caveats
    <<~EOS

        ██╗████████╗███████╗      ███╗   ███╗ █████╗  ██████╗ ██╗ ██████╗
        ██║╚══██╔══╝██╔════╝      ████╗ ████║██╔══██╗██╔════╝ ██║██╔════╝
        ██║   ██║   ███████╗█████╗██╔████╔██║███████║██║  ███╗██║██║
        ██║   ██║   ╚════██║╚════╝██║╚██╔╝██║██╔══██║██║   ██║██║██║
        ██║   ██║   ███████║      ██║ ╚═╝ ██║██║  ██║╚██████╔╝██║╚██████╗
        ╚═╝   ╚═╝   ╚══════╝      ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝ ╚═════╝

                           AI dev team
                      Installation complete!

      Run: its-magic --help
    EOS
  end

  test do
    system "#{bin}/its-magic", "--target", testpath, "--mode", "missing"
  end
end
