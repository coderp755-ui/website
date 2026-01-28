import { useEffect, useState, useContext } from "react";
import api from "../utils/api";
import { SiteContext } from "../context/SiteContext";

function About() {
  const { country, branch } = useContext(SiteContext);
  const [sections, setSections] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get(`/about/`)
      .then((res) => {
        setSections(res.data.sections);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching about page:", err);
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
    <div className="min-h-screen">
      {sections.map((section, index) => (
        <section key={index} className="py-16 px-4">
          <div className="max-w-6xl mx-auto">
            {section.section_type === "hero" && (
              <div className="text-center mb-12">
                {section.items[0]?.title && (
                  <h1 className="text-5xl font-bold mb-4">{section.items[0].title}</h1>
                )}
                {section.items[0]?.subtitle && (
                  <p className="text-xl text-gray-600">{section.items[0].subtitle}</p>
                )}
              </div>
            )}

            {section.section_type === "content" && (
              <div className="prose prose-lg max-w-none">
                {section.items.map((item, idx) => (
                  <div key={idx} className="mb-8">
                    {item.title && <h2 className="text-3xl font-bold mb-4">{item.title}</h2>}
                    {item.subtitle && <h3 className="text-xl text-gray-700 mb-3">{item.subtitle}</h3>}
                    {item.description && <p className="text-gray-600 leading-relaxed">{item.description}</p>}
                  </div>
                ))}
              </div>
            )}

            {section.section_type === "team" && (
              <div>
                <h2 className="text-4xl font-bold text-center mb-12">Our Team</h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                  {section.items.map((item, idx) => (
                    <div key={idx} className="text-center">
                      {item.image && (
                        <img
                          src={item.image}
                          alt={item.title}
                          className="w-32 h-32 rounded-full mx-auto mb-4 object-cover"
                        />
                      )}
                      {item.icon && (
                        <div className="text-6xl mb-4">{item.icon}</div>
                      )}
                      {item.title && <h3 className="text-xl font-bold mb-2">{item.title}</h3>}
                      {item.subtitle && <p className="text-gray-600 mb-2">{item.subtitle}</p>}
                      {item.description && <p className="text-gray-500 text-sm">{item.description}</p>}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {section.section_type === "values" && (
              <div>
                <h2 className="text-4xl font-bold text-center mb-12">Our Values</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  {section.items.map((item, idx) => (
                    <div key={idx} className="bg-gray-50 p-6 rounded-lg">
                      {item.icon && <div className="text-4xl mb-3">{item.icon}</div>}
                      {item.title && <h3 className="text-2xl font-bold mb-3">{item.title}</h3>}
                      {item.description && <p className="text-gray-600">{item.description}</p>}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </section>
      ))}
    </div>
  );
}

export default About
