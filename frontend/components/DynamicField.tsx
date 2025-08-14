import type React from "react"
import type { UseFormRegister, FieldErrors, UseFormWatch } from "react-hook-form"
import type { IField } from "@/types/form"

interface DynamicFieldProps {
  field: IField
  register: UseFormRegister<any>
  errors: FieldErrors
  watch: UseFormWatch<any>
  disabled?: boolean
}

export const DynamicField: React.FC<DynamicFieldProps> = ({ field, register, errors, watch, disabled = false }) => {
  const error = errors[field.name]
  const watchedValue = watch(field.name)

  const formatPAN = (value: string) => {
    return value
      .toUpperCase()
      .replace(/[^A-Z0-9]/g, "")
      .slice(0, 10)
  }

  const formatDate = (value: string) => {
    const cleaned = value.replace(/\D/g, "")
    if (cleaned.length >= 8) {
      const day = cleaned.slice(0, 2)
      const month = cleaned.slice(2, 4)
      const year = cleaned.slice(4, 8)

      // Validate day (01-31)
      const dayNum = Number.parseInt(day)
      if (dayNum < 1 || dayNum > 31) return value.slice(0, -1)

      // Validate month (01-12)
      const monthNum = Number.parseInt(month)
      if (monthNum < 1 || monthNum > 12) return value.slice(0, -1)

      // Validate year (1900-current year)
      const yearNum = Number.parseInt(year)
      const currentYear = new Date().getFullYear()
      if (yearNum < 1900 || yearNum > currentYear) return value.slice(0, -1)

      return `${day}/${month}/${year}`
    } else if (cleaned.length >= 4) {
      const day = cleaned.slice(0, 2)
      const month = cleaned.slice(2, 4)

      // Validate day and month as user types
      const dayNum = Number.parseInt(day)
      const monthNum = Number.parseInt(month)
      if (dayNum < 1 || dayNum > 31 || monthNum < 1 || monthNum > 12) {
        return value.slice(0, -1)
      }

      return `${day}/${month}/${cleaned.slice(4)}`
    } else if (cleaned.length >= 2) {
      const day = cleaned.slice(0, 2)
      const dayNum = Number.parseInt(day)
      if (dayNum < 1 || dayNum > 31) return value.slice(0, -1)

      return `${day}/${cleaned.slice(2)}`
    }
    return cleaned
  }

  const getErrorMessage = (error: any) => {
    if (!error) return ""
    const message = error.message as string
    if (message.includes("is required")) {
      return "required!"
    }
    return message
  }

  const renderField = () => {
    switch (field.type) {
      case "text":
        return (
          <input
            {...register(field.name, {
              onChange: (e) => {
                if (field.name === "panNumber") {
                  e.target.value = formatPAN(e.target.value)
                } else if (field.name === "dobOrDoi") {
                  e.target.value = formatDate(e.target.value)
                }
              },
            })}
            type="text"
            className="form-control"
            placeholder={field.placeholder || ""}
            disabled={disabled}
            maxLength={field.name === "panNumber" ? 10 : field.name === "dobOrDoi" ? 10 : undefined}
            style={{
              padding: "8px 12px",
              border: "1px solid #ddd",
              borderRadius: "4px",
              width: "100%",
              fontSize: "14px",
              backgroundColor: disabled ? "#f5f5f5" : "white",
              color: disabled ? "#666" : "#333",
            }}
          />
        )

      case "select":
        return (
          <select
            {...register(field.name)}
            className="form-control"
            disabled={disabled}
            style={{
              padding: "8px 12px",
              border: "1px solid #ddd",
              borderRadius: "4px",
              width: "100%",
              fontSize: "14px",
              backgroundColor: disabled ? "#f5f5f5" : "white",
              color: disabled ? "#666" : "#333",
            }}
          >
            {field.options?.map((option) => (
              <option key={option.value} value={option.value}>
                {option.text}
              </option>
            ))}
          </select>
        )

      case "checkbox":
        return (
          <div style={{ display: "flex", alignItems: "flex-start", gap: "8px" }}>
            <input
              {...register(field.name)}
              type="checkbox"
              disabled={disabled}
              style={{
                marginTop: "4px",
                transform: "scale(1.2)",
              }}
            />
            <label style={{ fontSize: "14px", lineHeight: "1.4", color: disabled ? "#666" : "#333" }}>
              {field.label}
            </label>
          </div>
        )

      case "radio":
        return (
          <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
            {field.options?.map((option) => (
              <div key={option.value} style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <input
                  {...register(field.name)}
                  type="radio"
                  value={option.value}
                  disabled={disabled}
                  style={{ transform: "scale(1.2)" }}
                />
                <label style={{ fontSize: "14px", color: disabled ? "#666" : "#333" }}>{option.text}</label>
              </div>
            ))}
          </div>
        )

      default:
        return null
    }
  }

  if (field.type === "checkbox") {
    return (
      <div style={{ marginBottom: "16px" }}>
        {renderField()}
        {error && <div style={{ color: "#dc3545", fontSize: "12px", marginTop: "4px" }}>{getErrorMessage(error)}</div>}
      </div>
    )
  }

  return (
    <div style={{ marginBottom: "16px" }}>
      <label
        style={{
          display: "block",
          marginBottom: "6px",
          fontWeight: "600",
          fontSize: "14px",
          color: "#333",
        }}
      >
        {field.validation?.required && <span style={{ color: "#dc3545" }}>* </span>}
        {field.label}
      </label>
      {renderField()}
      {error && <div style={{ color: "#dc3545", fontSize: "12px", marginTop: "4px" }}>{getErrorMessage(error)}</div>}
    </div>
  )
}

export type { IField } from "@/types/form"
