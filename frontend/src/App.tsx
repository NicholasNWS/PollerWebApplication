import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

import PlcList from './pages/PlcList'
import PlcForm from './pages/PlcForm'
import InfluxConfig from './pages/InfluxConfig'
import Dashboard from './pages/Dashboard'

// Create a query client
const queryClient = new QueryClient()

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navigate to="/plcs" replace />} />
          <Route path="/plcs" element={<PlcList />} />
          <Route path="/plcs/new" element={<PlcForm />} />
          <Route path="/plcs/:id" element={<PlcForm />} />
          <Route path="/influx" element={<InfluxConfig />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}
