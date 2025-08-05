import React, { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import axios from 'axios'

export default function PlcForm() {
  const { id } = useParams()
  const navigate = useNavigate()
  const isEdit = Boolean(id)
  const [form, setForm] = useState({ name: '', ip_address: '', protocol: 'modbus', tags: [], active: true })

  useEffect(() => {
    if (isEdit) axios.get(`/plcs/${id}`).then(res => setForm(res.data))
  }, [id])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (isEdit) await axios.patch(`/plcs/${id}`, form)
    else await axios.post('/plcs/', form)
    navigate('/plcs')
  }

  return (
    <form onSubmit={handleSubmit} className="p-4 space-y-4">
      {/* Fields for name, ip_address, protocol, tags, active */}
      <button type="submit" className="px-4 py-2 rounded-xl shadow">{isEdit ? 'Update' : 'Create'}</button>
    </form>
  )
}