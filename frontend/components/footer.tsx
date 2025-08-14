import { Facebook, Instagram } from "lucide-react";

export default function Footer() {
  return (
    <footer
      className="text-white relative"
      style={{
        background: `linear-gradient(45deg, rgba(2, 4, 53, 0.91) 0%, rgba(22, 4, 90, 0.9) 100%), url('/images/footer-bg.jpg') center center no-repeat`,
        backgroundSize: "cover",
      }}
    >
      <div className="container max-w-7xl mx-auto px-4 py-12">
        <div className="grid md:grid-cols-3 gap-10">
          {/* Contact Information */}
          <div>
            <h3 className="text-xl font-bold mb-4">UDYAM REGISTRATION</h3>
            <div className="space-y-2 text-sm">
              <p>Ministry of MSME</p>
              <p>Udyog bhawan - New Delhi</p>
              <p className="mt-4">
                <span className="font-medium">Email:</span> champions@gov.in
              </p>
              <div className="mt-6">
                <p className="font-medium">Contact Us</p>
                <p>For Grievances / Problems</p>
              </div>
            </div>
          </div>

          {/* Our Services */}
          <div>
            <h3 className="text-sm font-bold mb-4">Our Services</h3>
            <ul className="space-y-4 text-xs font-light">
              <li>
                <a
                  href="#"
                  className="hover:text-blue-300 transition-colors flex items-center"
                >
                  <span className="mr-2">›</span>
                  CHAMPIONS
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="hover:text-blue-300 transition-colors flex items-center"
                >
                  <span className="mr-2">›</span>
                  MSME Samadhaan
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="hover:text-blue-300 transition-colors flex items-center"
                >
                  <span className="mr-2">›</span>
                  MSME Sambandh
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="hover:text-blue-300 transition-colors flex items-center"
                >
                  <span className="mr-2">›</span>
                  MSME Dashboard
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="hover:text-blue-300 transition-colors flex items-center"
                >
                  <span className="mr-2">›</span>
                  Entrepreneurship Skill Development Programme (ESDP)
                </a>
              </li>
            </ul>
          </div>

          {/* Video Section */}
          <div>
            <h3 className="text-xl font-bold mb-4">Video</h3>
            <div className="bg-black rounded-lg overflow-hidden">
              <div className="relative aspect-video bg-gradient-to-br from-blue-600 to-teal-500 flex items-center justify-center">
                <div className="text-center">
                  <div className="text-2xl font-bold mb-2">
                    Udyam Registration
                  </div>
                  <div className="text-lg">www.udyamregistration.gov.in</div>
                </div>
                <button className="absolute bottom-4 left-4 w-8 h-8 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
                  <div className="w-0 h-0 border-l-[6px] border-l-white border-y-[4px] border-y-transparent ml-1"></div>
                </button>
              </div>
              <div className="bg-black px-4 py-2 flex items-center justify-between text-xs">
                <span>0:00 / 0:47</span>
                <div className="flex items-center space-x-2">
                  <button className="hover:text-blue-300">🔊</button>
                  <button className="hover:text-blue-300">⛶</button>
                  <button className="hover:text-blue-300">⋮</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="border-t border-gray-600 mt-8 pt-6">
          <div className="flex flex-col md:flex-row justify-between items-center text-xs text-gray-300">
            <div className="mb-4 md:mb-0">
              <p>
                © Copyright Udyam Registration. All Rights Reserved, Website
                Content Managed by Ministry of Micro Small and Medium
                Enterprises, GoI
              </p>
              <p className="mt-1">
                Website hosted & managed by National Informatics Centre,
                Ministry of Communications and IT, Government of India
              </p>
            </div>
            <div className="flex space-x-4">
              <a href="#" className="hover:text-white transition-colors">
                <span className="sr-only">Twitter</span>
                <svg
                  className="w-5 h-5"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
                </svg>
              </a>
              <a href="#" className="hover:text-white transition-colors">
                <Facebook className="w-5 h-5" />
              </a>
              <a href="#" className="hover:text-white transition-colors">
                <Instagram className="w-5 h-5" />
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
