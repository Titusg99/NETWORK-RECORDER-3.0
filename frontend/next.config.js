/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  // Enable static exports for Electron
  output: 'export',
  // Disable image optimization since we're running in Electron
  images: {
    unoptimized: true,
  },
};

module.exports = nextConfig; 