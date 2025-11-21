import Button from "@/components/ui/Button";
export default function Navbar(){
    return(
        <nav className="flex items-center justify-between p-4 bg-gray-700">
  <button id="menu-btn"
   className="text-2xl  text-white hover:text-gray-500 cursor-pointer">☰</button>
  <h1 className="fixed left-150 text-4xl text-white font-extrabold">My App</h1>
  {/* <div>
      <Button size="sm" type="primary">Sign in</Button>
    </div> */}
  <input 
    type="search" 
    placeholder="Search..." 
    className="fixed left-300 border p-2 rounded w-32 md:w-50  text-white "
  />
  <Button>
  <img 
    src="profile.png" 
    alt="profile" 
    className="w-8 h-8 rounded-full hover: cursor-pointer"
  />
  </Button>
</nav>

    );
}