import React from 'react'
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'
import { Card } from '../components/Card'

interface Plc {
  id: number
  name: string
  ip_address: string
  protocol: string
  active: boolean
}

export default function PlcList() {
  const { data: plcs } = useQuery<Plc[]>('plcs', () =>
    axios.get('/plcs/').then(res => res.data)
  )

  return (
    <div className="grid gap-4 p-4">
      {plcs?.map(plc => (
        <Card key={plc.id} title={plc.name}>
          <p>IP: {plc.ip_address}</p>
          <p>Protocol: {plc.protocol}</p>
        </Card>
      ))}
    </div>
  )
}