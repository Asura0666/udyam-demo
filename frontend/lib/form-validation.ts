import { z } from "zod"
import type { IField, IFormStep } from "@/types/form"

export const createZodSchema = (fields: readonly IField[]) => {
  const schemaObject: Record<string, z.ZodTypeAny> = {}

  fields.forEach((field) => {
    let fieldSchema: z.ZodTypeAny

    switch (field.type) {
      case "text":
        fieldSchema = z.string()

        if (field.validation.required) {
          fieldSchema = fieldSchema.min(1, `${field.label} is required`)
        } else {
          fieldSchema = fieldSchema.optional()
        }

        if (field.validation.maxlength) {
          fieldSchema = fieldSchema.max(
            field.validation.maxlength,
            `${field.label} must be at most ${field.validation.maxlength} characters`,
          )
        }

        if (field.validation.pattern) {
          const regex = new RegExp(field.validation.pattern)
          fieldSchema = fieldSchema.regex(regex, `${field.label} format is invalid`)
        }
        break

      case "select":
        fieldSchema = z.string()
        if (field.validation.required) {
          fieldSchema = fieldSchema
            .min(1, `${field.label} is required`)
            .refine((val) => val !== "0" && val !== "", `${field.label} is required`)
        } else {
          fieldSchema = fieldSchema.optional()
        }
        break

      case "checkbox":
        fieldSchema = z.boolean().optional()
        if (field.validation.required && field.validation.checked) {
          fieldSchema = z.boolean().refine((val) => val === true, `${field.label} is required`)
        }
        break

      case "radio":
        fieldSchema = z.union([z.string(), z.null(), z.undefined()]).transform((val) => val || "")
        if (field.validation.required) {
          fieldSchema = z.string().min(1, `${field.label} is required`)
        } else {
          fieldSchema = fieldSchema.optional()
        }
        break

      default:
        fieldSchema = z.string().optional()
    }

    schemaObject[field.name] = fieldSchema
  })

  return z.object(schemaObject)
}

export const createFormSchema = (step: IFormStep) => {
  return createZodSchema(step.fields)
}
