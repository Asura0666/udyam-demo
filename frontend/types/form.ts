export interface IFieldOption {
  text: string
  value: string
}

export interface IFieldValidation {
  required?: boolean
  maxlength?: number
  pattern?: string
  checked?: boolean
}

export interface IField {
  name: string
  label: string
  type: "text" | "checkbox" | "select" | "radio"
  placeholder: string | null
  validation: IFieldValidation
  options?: IFieldOption[]
  conditional?: boolean
}

export interface IFormStep {
  step: number
  name: string
  fields: readonly IField[]
}

export interface IFormSchema {
  steps: IFormStep[]
}
