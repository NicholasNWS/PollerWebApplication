// frontend/src/pages/PlcList.tsx
import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getPlcs, deletePlc } from "../api/plc";
import PlcForm, { PlcFormData } from "../components/PlcForm";

interface Tag {
  id: number;
  name: string;
  address: number;
  function_code: number;
  unit_id: number;
  plc_id: number;
}

interface Plc {
  id: number;
  name: string;
  ip_address: string;
  port: number;
  protocol: "modbus" | "cip";
  active: boolean;
  tags: Tag[];
}

export default function PlcList() {
  const [formOpen, setFormOpen] = useState(false);
  const [editing, setEditing] = useState<PlcFormData | null>(null);
  const queryClient = useQueryClient();

  // Fetch PLCs
  const {
    data: plcs,
    error,
    isLoading,
    isError,
  } = useQuery<Plc[]>(["plcs"], () => getPlcs().then((res) => res.data), {
    refetchOnWindowFocus: false,
  });

  // Delete PLC mutation
  const deleteMutation = useMutation((id: number) => deletePlc(id), {
    onSuccess: () => queryClient.invalidateQueries(["plcs"]),
    onError: (err: any) => {
      alert(err.response?.data?.detail || "Failed to delete PLC");
    },
  });

  if (isLoading) return <div>Loading PLCs…</div>;
  if (isError)
    return (
      <div className="p-4 text-red-600">
        Error loading PLCs: {(error as Error).message || "Unknown error"}
      </div>
    );

  return (
    <div className="p-4 space-y-6">
      {/* Header with Add button */}
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">PLC List</h1>
        <button
          className="px-4 py-1 bg-green-600 text-white rounded"
          onClick={() => {
            setEditing(null);
            setFormOpen(true);
          }}
        >
          + Add PLC
        </button>
      </div>

      {/* List of PLC cards */}
      {plcs && plcs.length > 0 ? (
        plcs.map((plc) => (
          <div
            key={plc.id}
            className="border rounded-lg p-4 bg-white shadow-sm"
          >
            <div className="flex justify-between items-center mb-2">
              <div>
                <h2 className="text-xl font-semibold">{plc.name}</h2>
                <p className="text-sm text-gray-600">
                  {plc.ip_address}:{plc.port} —{" "}
                  <span className="capitalize">{plc.protocol}</span> —{" "}
                  {plc.active ? "Active" : "Inactive"}
                </p>
              </div>
              <div className="space-x-2">
                {/* Edit button */}
                <button
                  className="text-blue-600 hover:underline"
                  onClick={() => {
                    setEditing({
                      id: plc.id,
                      name: plc.name,
                      ip_address: plc.ip_address,
                      port: plc.port,
                      protocol: plc.protocol,
                      active: plc.active,
                    });
                    setFormOpen(true);
                  }}
                >
                  Edit
                </button>
                {/* Delete button */}
                <button
                  className="text-red-600 hover:underline"
                  onClick={() => deleteMutation.mutate(plc.id)}
                >
                  Delete
                </button>
              </div>
            </div>

            {/* Tags */}
            <div className="mt-4">
              <h3 className="font-medium mb-2">Tags:</h3>
              {plc.tags.length > 0 ? (
                <ul className="list-disc pl-5 space-y-1">
                  {plc.tags.map((tag) => (
                    <li key={tag.id}>
                      <span className="font-medium">{tag.name}</span> — Addr{" "}
                      {tag.address}, FC {tag.function_code}, Unit{" "}
                      {tag.unit_id}
                      {/* TODO: Edit/Delete tag icons here */}
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-sm text-gray-500">No tags defined.</p>
              )}
              {/* TODO: Add “Add Tag” button here */}
            </div>
          </div>
        ))
      ) : (
        <p>No PLCs found.</p>
      )}

      {/* PLC Form Modal */}
      {formOpen && (
        <PlcForm
          initialData={editing || undefined}
          onClose={() => setFormOpen(false)}
        />
      )}
    </div>
  );
}
