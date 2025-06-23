import React from 'react';

const LoadingSkeleton: React.FC = () => (
  <div className="animate-pulse flex space-x-4">
    <div className="rounded-full bg-gray-200 dark:bg-gray-700 h-12 w-12"></div>
    <div className="flex-1 space-y-4 py-1">
      <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4"></div>
      <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded"></div>
    </div>
  </div>
);

export default LoadingSkeleton; 