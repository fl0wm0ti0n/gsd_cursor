# typed: strict
# frozen_string_literal: true

# Homebrew formula for the its-magic CLI installer.
class ItsMagic < Formula
  desc "AI development workflow toolkit for multi-agent teams"
  homepage "https://github.com/USER/its-magic"
  # UPDATE: url and sha256 after each release
  url "https://github.com/fl0wm0ti0n/its-magic/archive/refs/tags/v0.1.2-19.tar.gz"
  version "0.1.2-19"
  sha256 "430282e8f913631665ad5e3c701f922b76ecd3cb2815a1d3340e8f0661eb2681"
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
