import React from 'react';

interface CardProps {
  title: string;
  children: React.ReactNode;
}

export const Card: React.FC<CardProps> = ({ title, children }) => (
  <div className="p-4 shadow-lg rounded-2xl border border-gray-300 bg-white">
    <h2 className="text-xl font-semibold mb-2">{title}</h2>
    <div>{children}</div>
  </div>
);

export default Card;
