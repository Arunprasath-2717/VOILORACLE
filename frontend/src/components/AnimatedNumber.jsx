import React, { useState, useEffect, useRef } from 'react';

const AnimatedNumber = ({ end, suffix = '', prefix = '', duration = 1500 }) => {
  const [val, setVal] = useState(0);
  const ref = useRef();

  useEffect(() => {
    // If end is not a number or 0, just set it
    if (end == null || isNaN(end) || end === 0) {
      setVal(end || 0);
      return;
    }

    const obs = new IntersectionObserver(
      ([e]) => {
        if (e.isIntersecting) {
          let startTimestamp = null;
          const startValue = 0;
          
          const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            // Ease out quad
            const easeOutProgress = progress * (2 - progress);
            
            setVal(Math.floor(easeOutProgress * (end - startValue) + startValue));
            
            if (progress < 1) {
              window.requestAnimationFrame(step);
            } else {
              setVal(end);
            }
          };
          
          window.requestAnimationFrame(step);
          obs.unobserve(e.target);
        }
      },
      { threshold: 0.1 }
    );
    
    if (ref.current) {
      obs.observe(ref.current);
    }
    
    return () => obs.disconnect();
  }, [end, duration]);

  return <span ref={ref}>{prefix}{Number(val).toLocaleString()}{suffix}</span>;
};

export default AnimatedNumber;
