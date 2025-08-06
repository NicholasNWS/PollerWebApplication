// frontend/src/components/PlcForm.tsx
import React, { useState, useEffect } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { addPlc, updatePlc } from "../api/plc";

export interface PlcFormData {
  id?: number;
  name: string;
  ip_address: string;
  port: number;
  protocol: "modbus" | "cip";
  active: boolean;
}

interface PlcFormProps {
  /** If editing, pass in the existing plc data; otherwise omit for Add mode */
  initialData?: PlcFormData;
  /** Called when the modal/form should close */
  onClose: () => void;
}

export default function PlcForm({ initialData, onClose }: PlcFormProps) {
  const isEdit = Boolean(initialData?.id);
  const [form, setForm] = useState<PlcFormData>({
    name: initialData?.name || "",
    ip_address: initialData?.ip_address || "",
    port: initialData?.port || 502,
    protocol: initialData?.protocol || "modbus",
    active: initialData?.active ?? true,
    id: initialData?.id,
  });

  const queryClient = useQueryClient();

  const mutation = useMutation(
    (data: PlcFormData) =>
      isEdit
        ? updatePlc(data.id!, {
            name: data.name,
            ip_address: data.ip_address,
            port: data.port,
            protocol: data.protocol,
            active: data.active,
          })
        : addPlc({
            name: data.name,
            ip_address: data.ip_address,
            port: data.port,
            protocol: data.protocol,
          }),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(["plcs"]);
        onClose();
      },
      onError: (err: any) => {
        alert(
          err.response?.data?.detail ||
            "An error occurred. Please check your input."
        );
      },
    }
  );

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value, type, checked } = e.target;
    setForm((f) => ({
      ...f,
      [name]:
        type === "checkbox"
          ? checked
          : name === "port"
          ? Number(value)
          : value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    mutation.mutate(form);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-6 rounded-lg shadow-lg w-96 space-y-4"
      >
        <h2 className="text-xl font-semibold">
          {isEdit ? "Edit PLC" : "Add PLC"}
        </h2>

        <div>
          <label className="block text-sm font-medium">Name</label>
          <input
            name="name"
            value={form.name}
            onChange={handleChange}
            required
            className="w-full border px-2 py-1 rounded"
          />
        </div>

        <div>
          <label className="block text-sm font-medium">IP Address</label>
          <input
            name="ip_address"
            value={form.ip_address}
            onChange={handleChange}
            required
            className="w-full border px-2 py-1 rounded"
          />
        </div>

        <div className="flex space-x-2">
          <div className="flex-1">
            <label className="block text-sm font-medium">Port</label>
            <input
              name="port"
              type="number"
              value={form.port}
              onChange={handleChange}
              required
              className="w-full border px-2 py-1 rounded"
            />
          </div>
          <div className="flex-1">
            <label className="block text-sm font-medium">Protocol</label>
            <select
              name="protocol"
              value={form.protocol}
              onChange={handleChange}
              className="w-full border px-2 py-1 rounded"
            >
              <option value="modbus">Modbus</option>
              <option value="cip">CIP</option>
            </select>
          </div>
        </div>

        {isEdit && (
          <div className="flex items-center space-x-2">
            <input
              id="active"
              name="active"
              type="checkbox"
              checked={form.active}
              onChange={handleChange}
              className="h-4 w-4"
            />
            <label htmlFor="active" className="text-sm">
              Active
            </label>
          </div>
        )}

        <div className="flex justify-end space-x-2">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-1 border rounded"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={mutation.isLoading}
            className="px-4 py-1 bg-blue-600 text-white rounded"
          >
            {isEdit ? "Save" : "Add"}
          </button>
        </div>
      </form>
    </div>
  );
}
