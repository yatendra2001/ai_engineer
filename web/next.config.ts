import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  turbopack: {
    root: "..",
  },
  serverExternalPackages: ["@e2b/code-interpreter"],
};

export default nextConfig;
