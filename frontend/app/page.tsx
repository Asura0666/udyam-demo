import Footer from "@/components/footer";
import Header from "@/components/header";
import RegistrationForm from "@/components/registration-form";

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      {/* Main Title */}
      <h1 className="text-2xl text-gray-800 mb-4 border px-44 py-4 bg-gray-100">
        UDYAM REGISTRATION FORM - For New Enterprise who are not Registered yet
        as MSME
      </h1>
      <main className="container mx-auto px-4 py-8">
        <RegistrationForm />
        <div className="mt-8 mb-8">
          <div className="overflow-hidden whitespace-nowrap">
            <div className="animate-marquee hover:animate-marquee-paused inline-block">
              <a
                href="#"
                className="text-blue-600 hover:text-blue-800 font-medium text-lg"
              >
                Activities (NIC codes) not covered under MSMED Act, 2006 for
                Udyam Registration
              </a>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}
