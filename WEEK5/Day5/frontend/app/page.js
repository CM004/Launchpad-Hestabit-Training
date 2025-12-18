export default function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-6xl font-bold text-white mb-4">
          Day 5 - Production Deployment
        </h1>
        <p className="text-2xl text-yellow-300 mb-8">
          Full-Stack App with Docker + NGINX + HTTPS
        </p>
        <div className="bg-white rounded-lg p-6 shadow-2xl">
          <h2 className="text-3xl font-semibold text-gray-800 mb-4">
            Deployment Benchmarks
          </h2>
          <ul className="text-left text-gray-700 space-y-2">
            <li>1. HTTPS with SSL certificates</li>
            <li>2. NGINX reverse proxy</li>
            <li>3. MongoDB database</li>
            <li>4. Production ready backend</li>
            <li>5. Next.js frontend</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
