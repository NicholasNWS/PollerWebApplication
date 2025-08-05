import React, { useState, useEffect } from 'react'
import axios from 'axios'

export default function InfluxConfig() {
  const [cfg, setCfg] = useState({ url: '', token: '', org: '', bucket: '' })

  useEffect(() => {
    axios.get('/influx').then(res => setCfg(res.data))
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    await axios.post('/influx', cfg)
    alert('Saved')
  }

  return (
    <form onSubmit={handleSubmit} className="p-4 space-y-4">
      {/* Fields for url, token, org, bucket */}
      <button type="submit" className="px-4 py-2 rounded-xl shadow">Save Influx Config</button>
    </form>
  )
}