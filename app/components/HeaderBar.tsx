import React, { useState } from 'react';

const HeaderBar: React.FC = () => {
  const [dark, setDark] = useState(false);

  React.useEffect(() => {
    if (dark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [dark]);

  return (
    <header className="sticky top-0 z-40 w-full bg-white/80 dark:bg-gray-900/80 backdrop-blur shadow flex items-center justify-between px-8 py-4 mb-8 transition-colors">
      <div className="flex items-center space-x-3">
        <img src="/globe.svg" alt="Logo" className="h-8 w-8" />
        <span className="text-2xl font-extrabold text-brand-dark dark:text-brand-light tracking-tight">Cloud Cost Optimizer</span>
      </div>
      <button
        className="bg-gray-100 dark:bg-gray-800 rounded-full px-3 py-1 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-700 transition"
        onClick={() => setDark(d => !d)}
      >
        {dark ? '🌞 Light' : '🌙 Dark'}
      </button>
    </header>
  );
};

export default HeaderBar; 