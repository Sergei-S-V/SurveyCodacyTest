import { z } from "zod"

export const emailPattern = {
  value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
  message: "Invalid email address",
}

export const namePattern = {
  value: /^[A-Za-z\s\u00C0-\u017F]{1,30}$/,
  message: "Invalid name",
}

export const isISODateTimeString = (date: string): boolean => {
  // Unsafe access to 'error' type value is handled by zod's safeParse function

  const isoDateTimeSchema = z.string().datetime({ local: true })
  const parseResult = isoDateTimeSchema.safeParse(date)
  return parseResult.success
}

export const passwordRules = (isRequired = true) => {
  // These is from the boilerplate.  Not sure whether we can improve on the "any"
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const rules: Record<string, any> = {
    minLength: {
      value: 8,
      message: "Password must be at least 8 characters",
    },
  }

  if (isRequired) {
    rules.required = "Password is required"
  }

  return rules
}

export const confirmPasswordRules = (
  getValues: () => any,
  isRequired = true,
) => {
  const rules: any = {
    validate: (value: string) => {
      const password = getValues().password || getValues().new_password
      return value === password ? true : "The passwords do not match"
    },
  }

  if (isRequired) {
    rules.required = "Password confirmation is required"
  }

  return rules
}
