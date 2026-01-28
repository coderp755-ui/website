import { Link } from 'react-router-dom'
import { useState } from 'react'

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <nav className="bg-white shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link to="/" className="text-2xl font-bold text-blue-600">
              Grace
            </Link>
          </div>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-8">
            <Link 
              to="/" 
              className="text-gray-700 hover:text-blue-600 transition duration-200 font-medium"
            >
              Home
            </Link>
            <Link 
              to="/about" 
              className="text-gray-700 hover:text-blue-600 transition duration-200 font-medium"
            >
              About
            </Link>
            <Link 
              to="/services" 
              className="text-gray-700 hover:text-blue-600 transition duration-200 font-medium"
            >
              Services
            </Link>
            <Link 
              to="/contact" 
              className="text-gray-700 hover:text-blue-600 transition duration-200 font-medium"
            >
              Contact
            </Link>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-gray-700 hover:text-blue-600 focus:outline-none"
            >
              <svg
                className="h-6 w-6"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                {isOpen ? (
                  <path d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <div className="md:hidden bg-white border-t">
          <div className="px-2 pt-2 pb-3 space-y-1">
            <Link
              to="/"
              className="block px-3 py-2 rounded-md text-gray-700 hover:text-blue-600 hover:bg-gray-50 transition duration-200"
              onClick={() => setIsOpen(false)}
            >
              Home
            </Link>
            <Link
              to="/about"
              className="block px-3 py-2 rounded-md text-gray-700 hover:text-blue-600 hover:bg-gray-50 transition duration-200"
              onClick={() => setIsOpen(false)}
            >
              About
            </Link>
            <Link
              to="/services"
              className="block px-3 py-2 rounded-md text-gray-700 hover:text-blue-600 hover:bg-gray-50 transition duration-200"
              onClick={() => setIsOpen(false)}
            >
              Services
            </Link>
            <Link
              to="/contact"
              className="block px-3 py-2 rounded-md text-gray-700 hover:text-blue-600 hover:bg-gray-50 transition duration-200"
              onClick={() => setIsOpen(false)}
            >
              Contact
            </Link>
          </div>
        </div>
      )}
    </nav>
  )
}
