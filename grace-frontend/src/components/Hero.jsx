import { Link } from 'react-router-dom'

export default function Hero({ data }) {
  // Show loading state or fallback content if no data
  if (!data) {
    return (
      <section className="relative w-full min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-indigo-900 flex items-center justify-center text-white px-4">
        <div className="text-center animate-pulse">
          <div className="w-12 h-12 sm:w-16 sm:h-16 border-4 border-white border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold mb-4">Welcome</h1>
          <p className="text-base sm:text-lg md:text-xl opacity-80">Loading content...</p>
        </div>
      </section>
    );
  }

  const item = data.items?.[0];
  
  // Show fallback if no items
  if (!item) {
    return (
      <section className="relative w-full min-h-screen  flex items-center justify-center text-white px-4">
        <div className="text-center">
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold mb-4">Welcome</h1>
          <p className="text-base sm:text-lg md:text-xl opacity-80">No hero content available</p>
        </div>
      </section>
    );
  }
  
  // Use placeholder image if no image provided
  const backgroundImage = item?.image || 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=1920';

  // Check if link is internal (starts with /) or external
  const isInternalLink = item?.button_link?.startsWith('/');

  return (
    <section className="relative w-full min-h-screen h-screen flex items-center justify-center text-white overflow-hidden">
      {/* Background Image */}
      {backgroundImage && (
        <img 
          src={backgroundImage} 
          alt="Hero Background"
          className="absolute inset-0 w-full h-full object-cover object-center z-0"
          onError={(e) => {
            e.target.style.display = 'none';
          }}
        />
      )}
      
      {/* Background overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-black/60 via-black/40 to-black/60 z-10"></div>
      
      {/* Animated background overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-900/20 via-transparent to-purple-900/20 animate-pulse z-20"></div>
      
      {/* Floating particles effect - hidden on mobile for performance */}
      <div className="hidden sm:block absolute inset-0 overflow-hidden pointer-events-none z-30">
        <div className="absolute top-1/4 left-1/4 w-2 h-2 bg-white/20 rounded-full animate-bounce"></div>
        <div className="absolute top-1/3 right-1/3 w-1 h-1 bg-white/30 rounded-full animate-bounce delay-300"></div>
        <div className="absolute bottom-1/4 left-1/3 w-1.5 h-1.5 bg-white/25 rounded-full animate-bounce delay-500"></div>
        <div className="absolute top-1/2 right-1/4 w-1 h-1 bg-white/20 rounded-full animate-bounce delay-700"></div>
      </div>

      {/* Main content */}
      <div className="relative z-40 text-center w-full max-w-7xl mx-auto px-4 sm:px-6 md:px-8 lg:px-12 py-8 sm:py-12">
        {/* Content container */}
        <div className="space-y-4 sm:space-y-6 md:space-y-8">
          {item?.title && (
            <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl font-extrabold bg-white bg-clip-text text-transparent leading-tight animate-fade-in px-2">
              {item.title}
            </h1>
          )}
          
          {item?.subtitle && (
            <p className="text-lg sm:text-xl md:text-2xl lg:text-3xl font-light text-blue-100 opacity-90 animate-fade-in-delay-1 px-2">
              {item.subtitle}
            </p>
          )}
          
          {item?.description && (
            <p className="text-sm sm:text-base md:text-lg lg:text-xl text-gray-200 opacity-80 max-w-xs sm:max-w-md md:max-w-2xl lg:max-w-3xl mx-auto leading-relaxed animate-fade-in-delay-2 px-2">
              {item.description}
            </p>
          )}
          
          {/* {item?.button_text && (
            <div className="mt-6 sm:mt-8 md:mt-10 animate-fade-in-delay-3 px-2">
              {isInternalLink ? (
                <Link
                  to={item.button_link}
                  className="group inline-flex items-center justify-center gap-2 sm:gap-3 bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 hover:from-blue-700 hover:via-purple-700 hover:to-indigo-700 text-white font-semibold py-3 px-6 sm:py-4 sm:px-8 md:py-5 md:px-10 rounded-full text-base sm:text-lg md:text-xl transition-all duration-300 transform hover:scale-105 hover:shadow-2xl border border-white/20 backdrop-blur-sm w-auto"
                >
                  <span>{item.button_text}</span>
                  <svg className="w-4 h-4 sm:w-5 sm:h-5 group-hover:translate-x-1 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </Link>
              ) : (
                <a
                  href={item.button_link || "#"}
                  className="group inline-flex items-center justify-center gap-2 sm:gap-3 bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 hover:from-blue-700 hover:via-purple-700 hover:to-indigo-700 text-white font-semibold py-3 px-6 sm:py-4 sm:px-8 md:py-5 md:px-10 rounded-full text-base sm:text-lg md:text-xl transition-all duration-300 transform hover:scale-105 hover:shadow-2xl border border-white/20 backdrop-blur-sm w-auto"
                >
                  <span>{item.button_text}</span>
                  <svg className="w-4 h-4 sm:w-5 sm:h-5 group-hover:translate-x-1 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </a>
              )}
            </div>
          )} */}
        </div>
      </div>

      {/* Scroll indicator - hidden on small mobile */}
      <div className="hidden sm:block absolute bottom-6 sm:bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce z-50">
        <div className="w-5 h-8 sm:w-6 sm:h-10 border-2 border-white/50 rounded-full flex justify-center">
          <div className="w-1 h-2 sm:h-3 bg-white/70 rounded-full mt-2 animate-pulse"></div>
        </div>
      </div>
    </section>
  );
}