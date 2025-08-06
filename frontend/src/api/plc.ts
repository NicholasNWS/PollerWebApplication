import axios from "axios";

// Use your Vite env var
const API_BASE = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_BASE,
  timeout: 5000,
  headers: {
    "Content-Type": "application/json",
  },
});

// PLC endpoints
export const getPlcs = () => api.get("/plcs/");
export const addPlc = (plc: {
  name: string;
  ip_address: string;
  port: number;
  protocol: "modbus" | "cip";
}) => api.post("/plcs/", plc);
export const updatePlc = (id: number, plc: Partial<{
  name: string;
  ip_address: string;
  port: number;
  protocol: "modbus" | "cip";
  active: boolean;
}>) => api.patch(`/plcs/${id}`, plc);
export const deletePlc = (id: number) => api.delete(`/plcs/${id}`);

// Tag endpoints
export const getTags = (plcId: number) => api.get(`/plcs/${plcId}/tags/`);
export const addTag = (plcId: number, tag: {
  name: string;
  address: number;
  function_code: number;
  unit_id: number;
}) => api.post(`/plcs/${plcId}/tags/`, tag);
export const updateTag = (tagId: number, tag: Partial<{
  name: string;
  address: number;
  function_code: number;
  unit_id: number;
}>) => api.patch(`/tags/${tagId}`, tag);
export const deleteTag = (tagId: number) => api.delete(`/tags/${tagId}`);

export default api;
