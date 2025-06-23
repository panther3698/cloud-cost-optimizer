import React from 'react';

interface MetricCardProps {
  icon: React.ReactNode;
  label: string;
  value: string | number;
  color?: string;
}

const MetricCard: React.FC<MetricCardProps> = ({ icon, label, value, color = 'brand' }) => (
  <div className={`bg-gradient-to-br from-${color}-100 to-white dark:from-${color}-dark dark:to-gray-900 rounded-2xl shadow-card p-6 flex items-center transition-transform hover:scale-105`}>
    <div className={`bg-${color}-200 dark:bg-${color}-dark p-4 rounded-full mr-4 shadow-inner`}>
      {icon}
    </div>
    <div>
      <div className="text-gray-500 dark:text-gray-300 text-xs font-semibold">{label}</div>
      <div className="text-3xl font-extrabold text-gray-900 dark:text-white">{value}</div>
    </div>
  </div>
);

export default MetricCard; 