import React, { useState } from 'react';

const ChatBox: React.FC = () => {
  const [open, setOpen] = useState(false);

  if (!open) {
    return (
      <button
        className="fixed bottom-6 right-6 bg-brand shadow-lg text-white rounded-full p-4 z-50 hover:bg-brand-dark focus:outline-none transition-all"
        onClick={() => setOpen(true)}
        aria-label="Open chat"
      >
        💬
      </button>
    );
  }

  return (
    <div className="fixed bottom-6 right-6 w-96 max-w-full bg-white/70 dark:bg-gray-900/70 backdrop-blur-lg rounded-2xl shadow-2xl border border-white/30 z-50 flex flex-col transition-all">
      {/* ...rest of chat content... */}
    </div>
  );
};

export default ChatBox; 