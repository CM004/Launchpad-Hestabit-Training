"use client";
import { useState } from "react";

import Button from "@/components/ui/Button";
import Login from "@/components/ui/Login";
import Link from "next/link";

export default function Navbar(){

  const [isLoginOpen, setIsLoginOpen] = useState(false);
  
    return(
      <div>
        <nav className="flex items-center justify-between p-4 bg-gray-700">
  <button id="menu-btn"
   className="text-2xl  text-white hover:text-gray-500 cursor-pointer">☰</button>
  <h1 className="fixed left-150 text-4xl text-white font-extrabold">Gr8 Solutions.</h1>
  {/* <div>
      <Button size="sm" type="primary">Sign in</Button>
    </div> */}
  <input 
    type="search" 
    placeholder="Search..." 
    className="fixed left-300 border p-2 rounded w-32 md:w-50  text-white "
  />
  <Link href="/login">
  <Button size="sm" type="primary" className="rounded ml-4 hover:cursor-pointer flex items-center gap-2" onClick={() => setIsLoginOpen(true)}>
    <img 
      src="/profile.png"
      alt="profile image"
      className="w-6 h-6 rounded-full"
    />
  Login
  </Button>
  </Link>
 
</nav>
    <Login isOpen={isLoginOpen} onClose={() => setIsLoginOpen(false)} />
     </div>
  );
}