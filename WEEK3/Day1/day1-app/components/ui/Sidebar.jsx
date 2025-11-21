import Link from "next/link";
import { FaTachometerAlt, FaProjectDiagram, FaCog, FaUser, FaMoneyBill } from "react-icons/fa";
export default function Sidebar() {
  return (
    <aside id="sidebar" className="h-screen w-48 bg-gray-800 text-white p-4">

      <div className="mb-6">
        <h2 className="text-4xl underline decoration-indigo-400 font-bold">Menu</h2>
      </div>


     <ul className="space-y-4 text-sm">
        <p className="text-sm text-gray-500 uppercase mb-6 tracking-wide">Core</p>
        <li>
        <Link href="/Dashboard" className="flex items-center gap-2 hover:text-gray-300 cursor-pointer text-2xl mb-6 font-semibold"> <FaTachometerAlt/> Dashboard</Link></li>
        
        <p className="text-sm text-gray-500 uppercase mb-6 tracking-wide">Core</p>
        <li className="flex items-center gap-2 hover:text-gray-300 cursor-pointer text-2xl mb-6 font-semibold"><FaProjectDiagram/> Projects</li>
        
        <p className="text-sm text-gray-500 uppercase mb-6 tracking-wide">Core</p>
        <li className="flex items-center gap-2 hover:text-gray-300 cursor-pointer text-2xl mb-6 font-semibold"><FaCog/> Settings</li>
        <li className="flex items-center gap-2 hover:text-gray-300 cursor-pointer text-2xl mb-6 font-semibold"><FaMoneyBill/> Plans</li>
        
        <p className="text-sm text-gray-500 uppercase mb-6 tracking-wide">Core</p>
        <li className="flex items-center gap-2 hover:text-gray-300 cursor-pointer text-2xl mb-6 font-semibold"><FaUser/> Profile</li>
     </ul>
    </aside>
  );
}
