// frontend/src/api/axios.ts
import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,  // e.g. "http://localhost:8000"
  timeout: 5000,
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
