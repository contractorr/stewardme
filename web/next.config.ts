import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  devIndicators: false,
  async redirects() {
    return [
      { source: "/learning", destination: "/goals", permanent: true },
      { source: "/projects", destination: "/goals", permanent: true },
    ];
  },
};

export default nextConfig;
