//import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/ui/Navbar";
import Sidebar from "@/components/ui/Sidebar";

// const geistSans = Geist({
//   variable: "--font-geist-sans",
//   subsets: ["latin"],
// });

// const geistMono = Geist_Mono({
//   variable: "--font-geist-mono",
//   subsets: ["latin"],
// });

export const metadata = {
  title: "Week 3 Day1 App",
  description: "This is my first app with Next.js app with tailwindcss",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <div className="flex">
          <Sidebar/>
          <div className="flex-1">
            <Navbar/>
            <main className="">{children}</main>
          </div>
        </div>
        <script
        dangerouslySetInnerHTML={{
          __html: `document.getElementById("menu-btn")
          .addEventListener("click", function () {
          document.getElementById("sidebar")
          .classList.toggle("hidden");
          });`,
          }}
          />
      </body>
    </html>
  );
}
