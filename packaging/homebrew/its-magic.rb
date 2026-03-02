class ItsMagic < Formula
  desc "its-magic - AI dev team workflow"
  homepage "https://github.com/USER/its-magic"
  # UPDATE: url and sha256 after each release
  url "https://github.com/fl0wm0ti0n/its-magic/archive/refs/tags/v0.1.2-18.tar.gz"
  sha256 "5bfcf13a5489076eb41fe607da778b33cb0d8ce9c4acb9771733ed5f7d2ff26d"
  version "0.1.2-18"
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

