import dayjs from "dayjs"
import type React from "react"
import { Controller, useForm } from "react-hook-form"

interface FormData {
  startDate: string
}

const DateStartForm: React.FC = () => {
  const { control, handleSubmit } = useForm<FormData>({
    defaultValues: {
      startDate: dayjs().format("YYYY-MM-DD"),
    },
  })

  const onSubmit = (data: FormData) => {
    console.log("Submitted data:", data)
    // Handle form submission here
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label htmlFor="startDate">Start Date:</label>
        <Controller
          name="startDate"
          control={control}
          render={({ field }) => (
            <input {...field} type="date" id="startDate" />
          )}
        />
      </div>
      <button type="submit">Submit</button>
    </form>
  )
}

export default DateStartForm
