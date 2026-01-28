export default function Section({ data }) {
  if (!data || !data.items) return null

  return (
    <section className="py-16 px-4 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        {/* Features Section */}
        {data.section_type === 'features' && (
          <div>
            <h2 className="text-4xl font-bold text-center mb-12">Our Features</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {data.items.map((item, idx) => (
                <div key={idx} className="bg-white p-6 rounded-lg shadow-md hover:shadow-xl transition duration-300">
                  {item.icon && <div className="text-5xl mb-4">{item.icon}</div>}
                  {item.title && <h3 className="text-2xl font-bold mb-3">{item.title}</h3>}
                  {item.description && <p className="text-gray-600">{item.description}</p>}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* About Section */}
        {data.section_type === 'about' && (
          <div className="bg-white p-12 rounded-lg shadow-md">
            {data.items[0]?.title && (
              <h2 className="text-4xl font-bold mb-4 text-center">{data.items[0].title}</h2>
            )}
            {data.items[0]?.subtitle && (
              <h3 className="text-xl text-gray-600 mb-6 text-center">{data.items[0].subtitle}</h3>
            )}
            {data.items[0]?.description && (
              <p className="text-gray-700 leading-relaxed text-lg">{data.items[0].description}</p>
            )}
            {data.items[0]?.button_text && (
              <div className="text-center mt-8">
                <a
                  href={data.items[0].button_link || '#'}
                  className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg transition duration-200"
                >
                  {data.items[0].button_text}
                </a>
              </div>
            )}
          </div>
        )}

        {/* Services Section */}
        {data.section_type === 'services' && (
          <div>
            <h2 className="text-4xl font-bold text-center mb-12">Our Services</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {data.items.map((item, idx) => (
                <div key={idx} className="bg-white p-6 rounded-lg shadow-md hover:shadow-xl transition duration-300">
                  {item.image && (
                    <img src={item.image} alt={item.title} className="w-full h-48 object-cover rounded-lg mb-4" />
                  )}
                  {item.icon && <div className="text-5xl mb-4">{item.icon}</div>}
                  {item.title && <h3 className="text-2xl font-bold mb-3">{item.title}</h3>}
                  {item.description && <p className="text-gray-600 mb-4">{item.description}</p>}
                  {item.button_text && (
                    <a
                      href={item.button_link || '#'}
                      className="text-blue-600 hover:text-blue-700 font-semibold"
                    >
                      {item.button_text} →
                    </a>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </section>
  )
}
