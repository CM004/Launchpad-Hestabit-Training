"use client";
import Input from "@/components/ui/Input";  
import React, { useState } from "react";

const sampleUsers = [
  { name: "John Smith", email: "john.smith@example.com", role: "Admin", created: "15/11/2024 09:30", updated: "20/11/2024 14:15" },
  { name: "Sarah Johnson", email: "sarah.j@example.com", role: "User", created: "16/11/2024 10:45", updated: "21/11/2024 16:20" },
  { name: "Michael Chen", email: "michael.chen@example.com", role: "User", created: "17/11/2024 11:00", updated: "22/11/2024 13:30" },
  { name: "Emily Davis", email: "emily.davis@example.com", role: "Moderator", created: "18/11/2024 08:15", updated: "23/11/2024 10:45" },
  { name: "David Wilson", email: "david.w@example.com", role: "User", created: "19/11/2024 14:20", updated: "23/11/2024 15:00" },
  { name: "Lisa Anderson", email: "lisa.anderson@example.com", role: "User", created: "20/11/2024 09:00", updated: "24/11/2024 11:30" },
  { name: "James Martinez", email: "james.m@example.com", role: "Admin", created: "21/11/2024 10:30", updated: "24/11/2024 12:45" },
  { name: "Jessica Taylor", email: "jessica.t@example.com", role: "User", created: "22/11/2024 13:45", updated: "24/11/2024 14:00" },
  { name: "Robert Brown", email: "robert.brown@example.com", role: "User", created: "23/11/2024 07:30", updated: "24/11/2024 09:15" },
  { name: "Amanda White", email: "amanda.white@example.com", role: "Moderator", created: "24/11/2024 08:00", updated: "24/11/2024 08:00" },
  { name: "John Smith", email: "john.smith@example.com", role: "Admin", created: "15/11/2024 09:30", updated: "20/11/2024 14:15" },
  { name: "Sarah Johnson", email: "sarah.j@example.com", role: "User", created: "16/11/2024 10:45", updated: "21/11/2024 16:20" },
  { name: "Michael Chen", email: "michael.chen@example.com", role: "User", created: "17/11/2024 11:00", updated: "22/11/2024 13:30" },
  { name: "Emily Davis", email: "emily.davis@example.com", role: "Moderator", created: "18/11/2024 08:15", updated: "23/11/2024 10:45" },
  { name: "David Wilson", email: "david.w@example.com", role: "User", created: "19/11/2024 14:20", updated: "23/11/2024 15:00" },

];

export default function UsersList() {
  const [search, setSearch] = useState("");
  const filtered = sampleUsers.filter(
    user =>
      user.name.toLowerCase().includes(search.toLowerCase()) || user.email.toLowerCase().includes(search.toLowerCase())
  );
  
  return (
    <div className="w-full bg-white border shadow-sm text-black">
      <div className="flex justify-between items-center p-4 bg-gray-200">
        <h2 className="text-xl font-semibold">Users</h2>
        <div>
            <Input 
              placeholder="Search..." 
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm text-left">
          <thead className="border-b bg-gray-50">
            <tr>
              <th className="py-3 px-4">Name</th>
              <th className="py-3 px-4">Email</th>
              <th className="py-3 px-4">Role</th>
              <th className="py-3 px-4">Created at</th>
              <th className="py-3 px-4">Updated at</th>
            </tr>
          </thead>

          <tbody>
            {filtered.map((user, index) => (
              <tr key={index} className="border-b hover:bg-gray-50">
                <td className="py-3 px-4">{user.name}</td>
                <td className="py-3 px-4">{user.email}</td>
                <td className="py-3 px-4">{user.role}</td>
                <td className="py-3 px-4">{user.created}</td>
                <td className="py-3 px-4">{user.updated}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="flex justify-between items-center text-sm text-gray-600 p-4">
        <p>Showing {filtered.length} of {sampleUsers.length} results</p>
        <div className="flex gap-2">
          <button className="border rounded-md px-2 py-1">1</button>
          <button className="border rounded-md px-2 py-1">2</button>
        </div>
      </div>
    </div>
  );
}