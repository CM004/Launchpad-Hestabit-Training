"use client";

import { useState } from "react";
import Modal from "@/components/ui/Modal";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input"

import {User, Lock} from "lucide-react";
export function LoginOpen() {
  const [open, setOpen] = useState(true);

  function handleClose() {
    setOpen(false);
    // navigate back if possible, otherwise go to home
    if (typeof window !== "undefined" && window.history.length > 1) {
      window.history.back();
    } else {
      window.location.href = "/";
    }
  }

  return <Login isOpen={open} CloseModal={handleClose} />;
}

export default function Login({ isOpen, CloseModal }) {
  return (
    <Modal isOpen={isOpen} CloseModal={CloseModal} title="Login">
      <div className="space-y-2 text-black">
        <div>
          <label className="text-sm">Username</label>
            <div className="flex items-center py-1 gap-2" >
            <User size={18} />
            <Input placeholder="Enter Username" />
            </div>
        </div>

        <div>
          <label className="text-sm">Password</label>
            <div className="flex items-center py-1 gap-2" >
            <Lock size={18} />
            <Input placeholder="Enter Password" />
            </div>
        </div>

          <Button type="primary" size="sm" className="text-white">Login</Button>
        
      </div>
    </Modal>
  );
}
