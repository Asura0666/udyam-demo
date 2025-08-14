"use client";

import { useState } from "react";
import { ChevronDown, Menu, X } from "lucide-react";
import Image from "next/image";

export default function Header() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  return (
    <header className="bg-[#4538c6]/95 backdrop-blur-sm text-white sticky top-0 z-50 shadow-md">
      <div className="container max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between py-1">
          {/* Logo and Ministry Info */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center justify-center">
              <Image
                src="/images/ministry-logo.webp"
                alt="Ministry of MSME Logo"
                width={300}
                height={300}
                className="object-contain"
              />
            </div>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden p-2"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          >
            {isMobileMenuOpen ? (
              <X className="w-6 h-6" />
            ) : (
              <Menu className="w-6 h-6" />
            )}
          </button>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <a
              href="#"
              className="hover:text-purple-200 transition-colors border-b-2 border-white pb-1"
            >
              Home
            </a>
            <a href="#" className="hover:text-purple-200 transition-colors text-gray-200">
              NIC Code
            </a>
            <div className="relative group">
              <button className="flex items-center space-x-1 hover:text-purple-200 transition-colors text-gray-200">
                <span>Useful Documents</span>
                <ChevronDown className="w-4 h-4" />
              </button>
            </div>
            <div className="relative group">
              <button className="flex items-center space-x-1 hover:text-purple-200 transition-colors text-gray-200">
                <span>Print / Verify</span>
                <ChevronDown className="w-4 h-4" />
              </button>
            </div>
            <div className="relative group">
              <button className="flex items-center space-x-1 hover:text-purple-200 transition-colors text-gray-200">
                <span>Update Details</span>
                <ChevronDown className="w-4 h-4" />
              </button>
            </div>
            <div className="relative group">
              <button className="flex items-center space-x-1 hover:text-purple-200 transition-colors text-gray-200">
                <span>Login</span>
                <ChevronDown className="w-4 h-4" />
              </button>
            </div>
          </nav>
        </div>

        {/* Mobile Navigation */}
        {isMobileMenuOpen && (
          <div className="md:hidden border-t border-purple-400 py-4">
            <nav className="flex flex-col space-y-4">
              <a
                href="#"
                className="hover:text-purple-200 transition-colors border-b border-white pb-1"
              >
                Home
              </a>
              <a href="#" className="hover:text-purple-200 transition-colors text-gray-200">
                NIC Code
              </a>
              <button className="flex items-center justify-between hover:text-purple-200 transition-colors text-gray-200">
                <span>Useful Documents</span>
                <ChevronDown className="w-4 h-4" />
              </button>
              <button className="flex items-center justify-between hover:text-purple-200 transition-colors text-gray-200">
                <span>Print / Verify</span>
                <ChevronDown className="w-4 h-4" />
              </button>
              <button className="flex items-center justify-between hover:text-purple-200 transition-colors text-gray-200">
                <span>Update Details</span>
                <ChevronDown className="w-4 h-4" />
              </button>
              <button className="flex items-center justify-between hover:text-purple-200 transition-colors text-gray-200">
                <span>Login</span>
                <ChevronDown className="w-4 h-4" />
              </button>
            </nav>
          </div>
        )}
      </div>
    </header>
  );
}
