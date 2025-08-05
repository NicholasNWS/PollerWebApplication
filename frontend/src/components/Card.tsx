import React from 'react'
import { Card as ShadCard, CardContent } from '@/components/ui/card'

interface CardProps {
  title: string
  children: React.ReactNode
}

export const Card: React.FC<CardProps> = ({ title, children }) => (
  <ShadCard className="p-4 shadow-lg rounded-2xl">
    <h2 className="text-xl font-semibold mb-2">{title}</h2>
    <CardContent>{children}</CardContent>
  </ShadCard>
)