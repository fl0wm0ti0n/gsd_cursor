# typed: strict
# frozen_string_literal: true

# Homebrew formula for the its-magic CLI installer.
class ItsMagic < Formula
  desc "AI development workflow toolkit for multi-agent teams"
  homepage "https://github.com/USER/its-magic"
  # UPDATE: url and sha256 after each release
  url "https://github.com/fl0wm0ti0n/its-magic/archive/refs/tags/v0.1.2-26.tar.gz"
  version "0.1.2-26"
  sha256 "8c437726db4d9d3864ce8cf92c05f53b8fb80b1d900f9ffba520cb99f5d5c114"
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
