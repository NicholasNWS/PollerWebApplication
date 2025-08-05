// frontend/src/pages/PlcList.tsx
import React from "react";
import { useQuery } from "@tanstack/react-query";
import api from "../api/axios";

interface Plc {
  id: number;
  name: string;
  ip_address: string;
  port: number;
  protocol: "modbus" | "cip";
  active: boolean;
  tags?: { id: number; name: string }[];
}

export default function PlcList() {
  const {
    data: plcs,
    error,
    isLoading,
    isError,
  } = useQuery<Plc[]>(
    ["plcs"],
    async () => {
      const res = await api.get<Plc[]>("/plcs/");
      return res.data;
    },
    {
      refetchOnWindowFocus: false,
      retry: 1,
    }
  );

  if (isLoading) return <div>Loading PLCs…</div>;
  if (isError)
    return (
      <div className="p-4 text-red-600">
        Error loading PLCs:{" "}
        {(error as Error).message || "Unknown error"}
      </div>
    );

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">PLC List</h1>
      {plcs && plcs.length > 0 ? (
        <table className="min-w-full border border-gray-300">
          <thead className="bg-gray-100">
            <tr>
              {["ID","Name","IP Address","Port","Protocol","Active"].map((h) => (
                <th
                  key={h}
                  className="border px-4 py-2 text-left text-sm font-medium text-gray-700"
                >
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {plcs.map((plc) => (
              <tr key={plc.id} className="hover:bg-gray-50">
                <td className="border px-4 py-2">{plc.id}</td>
                <td className="border px-4 py-2">{plc.name}</td>
                <td className="border px-4 py-2">{plc.ip_address}</td>
                <td className="border px-4 py-2">{plc.port}</td>
                <td className="border px-4 py-2 capitalize">
                  {plc.protocol}
                </td>
                <td className="border px-4 py-2">
                  {plc.active ? "Yes" : "No"}
                </td>
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
