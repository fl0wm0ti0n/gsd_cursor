class ItsMagicBeta < Formula
  desc "its-magic - AI dev team workflow (beta)"
  homepage "https://github.com/USER/its-magic"
  # UPDATE: url and sha256 after each beta release
  url "https://github.com/fl0wm0ti0n/its-magic/archive/refs/tags/v0.1.2-17.tar.gz"
  sha256 "40240ffc266680c7f63dce9593318d3f31a4f9097500050c964ba731d9d5d34c"
  version "0.1.2-17"
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





















