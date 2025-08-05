import React from "react";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";

interface Plc {
  id: number;
  name: string;
  ip_address: string;
  protocol: string;
  active: boolean;
}

export default function PlcList() {
  const { data, error, isLoading } = useQuery<Plc[]>(
    ["plcs"],
    async () => {
      const res = await axios.get("http://127.0.0.1:8000/plcs/");
      return res.data;
    },
    {
      refetchOnWindowFocus: false,
    }
  );

  if (isLoading) return <div>Loading PLCs...</div>;
  if (error) return <div>Error loading PLCs</div>;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">PLC List</h1>
      {data && data.length ? (
        <table className="min-w-full border border-gray-300">
          <thead>
            <tr>
              <th className="border px-4 py-2">ID</th>
              <th className="border px-4 py-2">Name</th>
              <th className="border px-4 py-2">IP Address</th>
              <th className="border px-4 py-2">Protocol</th>
              <th className="border px-4 py-2">Active</th>
            </tr>
          </thead>
          <tbody>
            {data.map((plc) => (
              <tr key={plc.id}>
                <td className="border px-4 py-2">{plc.id}</td>
                <td className="border px-4 py-2">{plc.name}</td>
                <td className="border px-4 py-2">{plc.ip_address}</td>
                <td className="border px-4 py-2">{plc.protocol}</td>
                <td className="border px-4 py-2">{plc.active ? "Yes" : "No"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No PLCs found.</p>
      )}
    </div>
  );
}
