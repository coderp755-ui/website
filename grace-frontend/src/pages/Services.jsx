import { useEffect, useState, useContext } from "react";
import api from "../utils/api";
import { SiteContext } from "../context/SiteContext";

function Services() {
  const { country, branch } = useContext(SiteContext);
  const [sections, setSections] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get(`/services/`)
      .then((res) => {
        setSections(res.data.sections);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching services page:", err);
        setLoading(false);
      });
  }, [country, branch]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-xl">Loading...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-blue-600 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <h1 className="text-5xl font-bold mb-4">Our Services</h1>
          <p className="text-xl">Comprehensive solutions tailored to your needs</p>
        </div>
      </div>

      {sections.map((section, index) => (
        <section key={index} className="py-16 px-4">
          <div className="max-w-7xl mx-auto">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {section.items?.map((item, idx) => (
                <div key={idx} className="bg-white p-6 rounded-lg shadow-md hover:shadow-xl transition duration-300">
                  {item.icon && <div className="text-5xl mb-4">{item.icon}</div>}
                  {item.title && <h3 className="text-2xl font-bold mb-3">{item.title}</h3>}
                  {item.description && <p className="text-gray-600">{item.description}</p>}
                </div>
              ))}
            </div>
          </div>
        </section>
      ))}
    </div>
  );
}

export default Services
