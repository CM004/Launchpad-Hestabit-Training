// components/dashboard/DashboardClient.jsx
"use client";

import { useState } from "react";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import Modal from "@/components/ui/Modal";
import Input from "@/components/ui/Input";

/**
 * DashboardClient
 * - Uses your existing ui components (Button, Card, Badge, Modal, Input)
 * - Does NOT use chart images — draws simple lightweight SVG placeholders
 * - Keeps interactive bits (useState, onClick) inside this client component
 */

export default function DashboardClient({ initialData = {} }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="p-6 space-y-6 min-h-screen bg-gray-900 text-gray-100">
      {/* Title row */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
          <p className="mt-2 text-gray-400">Overview of key metrics</p>
        </div>

        <div className="flex items-center gap-3">
          <Badge color="green">Live</Badge>
          <Button size="sm" type="primary" onClick={() => setOpen(true)}>
            New
          </Button>
        </div>
      </div>

      {/* Top cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card title="Primary Card" className="bg-white text-black">
          <p className="text-sm text-gray-600">Primary metric</p>
          <div className="mt-4">
            <Button size="sm" type="basic">View Details</Button>
          </div>
        </Card>

        <Card title="Warning Card" className="bg-yellow-400 text-black">
          <p className="text-sm opacity-90">Warning metric</p>
          <div className="mt-4">
            <Button size="sm" type="basic">View Details</Button>
          </div>
        </Card>

        <Card title="Success Card" className="bg-green-500 text-white">
          <p className="text-sm opacity-90">Success metric</p>
          <div className="mt-4">
            <Button size="sm" type="basic">View Details</Button>
          </div>
        </Card>

        <Card title="Danger Card" className="bg-red-500 text-white">
          <p className="text-sm opacity-90">Danger metric</p>
          <div className="mt-4">
            <Button size="sm" type="basic">View Details</Button>
          </div>
        </Card>
      </div>

      {/* Charts row: use SVG placeholders (no images) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card title="Area Chart Example" className="bg-white text-black">
          <div className="mt-3">
            {/* Simple area chart placeholder (SVG) */}
            <svg viewBox="0 0 600 180" className="w-full h-48">
              <defs>
                <linearGradient id="g1" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#60a5fa" stopOpacity="0.6" />
                  <stop offset="100%" stopColor="#60a5fa" stopOpacity="0.08" />
                </linearGradient>
              </defs>
              <rect width="100%" height="100%" fill="transparent" />
              <path
                d="M0,140 C60,60 120,100 180,80 C240,60 300,100 360,90 C420,80 480,110 540,50 L600,50 L600,180 L0,180 Z"
                fill="url(#g1)"
              />
              <polyline
                points="0,140 60,60 120,100 180,80 240,60 300,100 360,90 420,80 480,110 540,50 600,50"
                fill="none"
                stroke="#2563eb"
                strokeWidth="3"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </div>
        </Card>

        <Card title="Bar Chart Example" className="bg-white text-black">
          <div className="mt-3">
            {/* Simple bar chart placeholder (SVG) */}
            <svg viewBox="0 0 600 180" className="w-full h-48">
              <rect width="100%" height="100%" fill="transparent" />
              {/* bars */}
              <rect x="40" y="110" width="40" height="60" rx="4" fill="#2563eb" />
              <rect x="120" y="95" width="40" height="75" rx="4" fill="#2563eb" />
              <rect x="200" y="80" width="40" height="90" rx="4" fill="#2563eb" />
              <rect x="280" y="65" width="40" height="105" rx="4" fill="#2563eb" />
              <rect x="360" y="50" width="40" height="120" rx="4" fill="#2563eb" />
              <rect x="440" y="25" width="40" height="145" rx="4" fill="#2563eb" />
              {/* x-axis labels (subtle) */}
              <g fill="#9ca3af" fontSize="10">
                <text x="40" y="168">Jan</text>
                <text x="120" y="168">Feb</text>
                <text x="200" y="168">Mar</text>
                <text x="280" y="168">Apr</text>
                <text x="360" y="168">May</text>
                <text x="440" y="168">Jun</text>
              </g>
            </svg>
          </div>
        </Card>
      </div>

      {/* DataTable placeholder */}
      <Card title="DataTable Example" className="bg-white text-black">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-700">Show</span>
            <select className="ml-2 border px-2 py-1 rounded text-sm">
              <option>10</option>
              <option>25</option>
              <option>50</option>
            </select>
            <span className="text-sm text-gray-700">entries</span>
          </div>

          <div className="flex items-center gap-2">
            <label className="text-sm text-gray-700">Search:</label>
            <Input className="w-48" placeholder="Search..." />
          </div>
        </div>

        <div className="text-sm text-gray-600">Table content goes here...</div>
      </Card>

      {/* Modal for "New" action */}
      <Modal isOpen={open} onClose={() => setOpen(false)} title="Create new item">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Name</label>
            <Input placeholder="Enter name" />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Description</label>
            <textarea className="w-full px-3 py-2 border rounded-md" rows={4} />
          </div>

          <div className="flex justify-end gap-2">
            <Button type="basic" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button type="primary" onClick={() => setOpen(false)}>
              Create
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
