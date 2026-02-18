class ItsMagicBeta < Formula
  desc "its-magic - AI dev team workflow (beta)"
  homepage "https://github.com/USER/its-magic"
  # UPDATE: url and sha256 after each beta release
  url "https://github.com/fl0wm0ti0n/its-magic/archive/refs/tags/v0.1.2-15.tar.gz"
  sha256 "59a5e9f17dcbc5c0abc5b076ab5c349d01161a80e503673b3951fc3327a6d0c5"
  version "0.1.2-15"
  license "MIT"

  conflicts_with "its-magic", because: "beta and stable share the same binary"

  def install
    libexec.install Dir["*"]
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
                   Installation complete! (beta)

      Run: its-magic --help
    EOS
  end

  test do
    system "#{bin}/its-magic", "--target", testpath, "--mode", "missing"
  end
end



















