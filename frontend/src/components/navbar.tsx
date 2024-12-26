"use client";
import { useState } from "react";
import Link from "next/link";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBars, faTimes } from "@fortawesome/free-solid-svg-icons";

const Navbar: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <nav className="bg-blue-500 p-4">
      <div className="container mx-auto flex items-center justify-between">
        {/* Logo */}
        <div className="text-white text-xl font-bold">IDS.</div>

        {/* Navigation Links for Desktop */}
        <div className="hidden md:flex space-x-6">
          <Link href="/" className="text-white hover:text-gray-300">
            Home
          </Link>
          <Link href="/dashboard" className="text-white hover:text-gray-300">
            Dashboard
          </Link>
          <Link href="/history" className="text-white hover:text-gray-300">
            History
          </Link>
          <Link href="/about" className="text-white hover:text-gray-300">
            About
          </Link>
        </div>

        {/* Sign In Button for Desktop */}
        <div className="hidden md:block text-white">
          <Link
            href="/signin"
            className="border-2 border-white py-2 px-4 rounded-lg hover:bg-white hover:text-blue-500"
          >
            Sign In
          </Link>
        </div>

        {/* Hamburger Menu for Mobile */}
        <div className="md:hidden">
          <button onClick={toggleMenu} className="text-white">
            <FontAwesomeIcon icon={isMenuOpen ? faTimes : faBars} className="h-6 w-6" />
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="md:hidden bg-blue-500 p-4">
          <Link href="/" className="block text-white py-2">
            Home
          </Link>
          <Link href="/dashboard" className="block text-white py-2">
            Dashboard
          </Link>
          <Link href="/history" className="block text-white py-2">
            History
          </Link>
          <Link href="/about" className="block text-white py-2">
            About
          </Link>
          <Link
            href="/signin"
            className="block text-white py-2 border-2 border-white px-4 rounded-lg hover:bg-white hover:text-blue-500"
          >
            Sign In
          </Link>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
