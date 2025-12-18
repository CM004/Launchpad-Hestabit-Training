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
            <li>1. <a href="https://localhost" className="text-blue-600 hover:underline">HTTPS with SSL certificates</a></li>
            <li>2. <a href="/api" className="text-blue-600 hover:underline">NGINX reverse proxy</a></li>
            <li>3. <a href="/api" className="text-blue-600 hover:underline">MongoDB database</a></li>
            <li>4. <a href="/health" className="text-blue-600 hover:underline">Production ready backend</a></li>
            <li>5. Next.js frontend ✅</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
