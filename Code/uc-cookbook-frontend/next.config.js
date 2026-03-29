/** @type {import('next').NextConfig} */
const backendInternal =
  process.env.BACKEND_INTERNAL_URL || 'http://127.0.0.1:8000'

const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**',
      },
    ],
  },
  /** Proxy API to FastAPI so the browser only calls the Next dev server (avoids failed fetch to :8000). */
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${backendInternal.replace(/\/$/, '')}/:path*`,
      },
    ]
  },
}

module.exports = nextConfig
