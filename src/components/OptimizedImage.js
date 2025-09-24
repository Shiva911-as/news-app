import React, { useState, useRef, useEffect } from 'react';

const OptimizedImage = ({ 
  src, 
  alt, 
  className = '', 
  width, 
  height, 
  placeholder = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIwIiBoZWlnaHQ9IjgwIiB2aWV3Qm94PSIwIDAgMTIwIDgwIiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxyZWN0IHdpZHRoPSIxMjAiIGhlaWdodD0iODAiIGZpbGw9IiNmM2Y0ZjYiLz48L3N2Zz4=',
  quality = 80,
  priority = false,
  onLoad,
  onError,
  ...props 
}) => {
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageError, setImageError] = useState(false);
  const [isInView, setIsInView] = useState(priority);
  const imgRef = useRef(null);

  // Intersection Observer for lazy loading
  useEffect(() => {
    if (priority || !imgRef.current) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsInView(true);
          observer.disconnect();
        }
      },
      {
        rootMargin: '50px',
        threshold: 0.1
      }
    );

    observer.observe(imgRef.current);

    return () => observer.disconnect();
  }, [priority]);

  // Generate optimized image URL (placeholder for actual optimization service)
  const getOptimizedSrc = (originalSrc) => {
    if (!originalSrc) return placeholder;
    
    // For Unsplash images, we can optimize them
    if (originalSrc.includes('unsplash.com')) {
      try {
        const url = new URL(originalSrc);
        url.searchParams.set('w', width || 400);
        url.searchParams.set('h', height || 250);
        url.searchParams.set('fit', 'crop');
        url.searchParams.set('q', quality || 80);
        url.searchParams.set('auto', 'format');
        return url.toString();
      } catch (e) {
        return originalSrc;
      }
    }
    
    // For Picsum images, optimize them
    if (originalSrc.includes('picsum.photos')) {
      try {
        const url = new URL(originalSrc);
        url.searchParams.set('w', width || 400);
        url.searchParams.set('h', height || 250);
        return url.toString();
      } catch (e) {
        return originalSrc;
      }
    }
    
    // In a real implementation, you would use a service like:
    // - Cloudinary
    // - ImageKit
    // - Next.js Image Optimization API
    // - Custom image optimization service
    
    // For now, we'll return the original src
    // In production, you would construct URLs like:
    // return `https://your-cdn.com/image?url=${encodeURIComponent(originalSrc)}&w=${width}&h=${height}&q=${quality}&f=webp`;
    
    return originalSrc;
  };

  const handleLoad = () => {
    setImageLoaded(true);
    if (onLoad) onLoad();
  };

  const handleError = () => {
    setImageError(true);
    if (onError) onError();
  };

  const shouldLoadImage = isInView || priority;
  const optimizedSrc = shouldLoadImage ? getOptimizedSrc(src) : placeholder;

  return (
    <div 
      ref={imgRef}
      className={`relative overflow-hidden ${className}`}
      style={{ width, height }}
    >
      {/* Skeleton/Placeholder */}
      {!imageLoaded && !imageError && (
        <div 
          className="absolute inset-0 bg-gray-200 dark:bg-gray-700 animate-pulse rounded-lg"
          style={{ 
            backgroundImage: `url(${placeholder})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center'
          }}
        />
      )}

      {/* Actual Image */}
      {shouldLoadImage && (
        <img
          src={optimizedSrc}
          alt={alt}
          className={`w-full h-full object-cover transition-all duration-300 ${
            imageLoaded ? 'opacity-100' : 'opacity-0'
          } ${imageError ? 'hidden' : ''}`}
          onLoad={handleLoad}
          onError={handleError}
          loading={priority ? 'eager' : 'lazy'}
          decoding="async"
          {...props}
        />
      )}

      {/* Error State */}
      {imageError && (
        <div className="absolute inset-0 flex items-center justify-center bg-gray-100 dark:bg-gray-700 rounded-lg">
          <div className="text-center text-gray-500 dark:text-gray-400">
            <svg 
              className="w-8 h-8 mx-auto mb-2" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" 
              />
            </svg>
            <p className="text-xs">Image unavailable</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default OptimizedImage;
