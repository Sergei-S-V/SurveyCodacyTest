import { Controller, type SubmitHandler, useForm } from "react-hook-form"
import FormRow from "../Common/FormRow.tsx"

import {
  Button,
  Card,
  CardBody,
  CardHeader,
  Checkbox,
  Flex,
  FormControl,
  FormLabel,
  Heading,
  Input,
  NumberDecrementStepper,
  NumberIncrementStepper,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
} from "@chakra-ui/react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import dayjs from "dayjs"
import type { ApiError } from "../../client"
import {
  type TDataCreateSchedule,
  createSchedule,
} from "../../client/services/scheduleService.ts"
import useCustomToast from "../../hooks/useCustomToast.ts"
import { handleError } from "../../utils.ts"

interface TimerFormData {
  startDate: string
  endDate?: string
  daysBetween: number
  skipWeekends: boolean
  skipHolidays: boolean
  timeOfDay: string
}
const TimerPanel = () => {
  // eslint-disable-next-line
  const today: string = dayjs().format("YYYY-MM-DD")
  // eslint-disable-next-line
  const tomorrow: string = dayjs().add(1, "day").format("YYYY-MM-DD")
  // eslint-disable-next-line
  const aMonthFromToday: string = dayjs().add(1, "month").format("YYYY-MM-DD")

  // eslint-disable-next-line
  const { handleSubmit, register, control, watch, setValue } = useForm({
    defaultValues: {
      startDate: tomorrow,
      endDate: aMonthFromToday,
      daysBetween: 1,
      timeOfDay: "08:00",
      skipHolidays: false,
      skipWeekends: false,
    },
  })

  // eslint-disable-next-line
  const endDate = watch("endDate")
  // eslint-disable-next-line
  const startDate = watch("startDate")

  const showToast = useCustomToast()
  const queryClient = useQueryClient()
  const mutation = useMutation({
    mutationFn: (data: TDataCreateSchedule) => createSchedule(data),
    onSuccess: () => {
      showToast("Success!", "Schedule created successfully.", "success")
    },
    onError: (err: ApiError) => {
      handleError(err, showToast)
    },
    onSettled: async () => {
      await queryClient.invalidateQueries({ queryKey: ["schedule"] })
    },
  })

  const onSubmit: SubmitHandler<TimerFormData> = (data: TimerFormData) => {
    const {
      startDate,
      endDate,
      daysBetween,
      timeOfDay,
      skipHolidays,
      skipWeekends,
    } = data
    const submissionData: TDataCreateSchedule = {
      startDate,
      endDate,
      daysBetween,
      skipHolidays,
      skipWeekends,
      timesOfDay: [timeOfDay],
    }
    mutation.mutate(submissionData)
  }

  return (
    <Card variant="outline" w="80%">
      <CardHeader bg="gray.100">
        <Heading size="lg">Question Schedule</Heading>
      </CardHeader>
      <CardBody>
        <form onSubmit={/* eslint-disable */ handleSubmit(onSubmit)}>
          <Flex direction="column">
            <FormRow>
              <FormControl>
                <FormLabel>Date Start</FormLabel>
                <Controller
                  name="startDate"
                  control={control}
                  rules={{ required: true }}
                  render={({ field }) => (
                    <Input
                      {...field}
                      type="date"
                      min={today}
                      onChange={(e) => {
                        const newStartDate = e.target.value
                        if (dayjs(newStartDate).isAfter(dayjs(endDate))) {
                          setValue(
                            "endDate",
                            dayjs(newStartDate)
                              .add(1, "month")
                              .format("YYYY-MM-DD"),
                          )
                        }
                        field.onChange(newStartDate)
                      }}
                    />
                  )}
                />
              </FormControl>
              <FormControl>
                <FormLabel>Date End</FormLabel>
                <Controller
                  name="endDate"
                  control={control}
                  rules={{
                    required: true,
                    validate: (value) => dayjs(value).isAfter(dayjs(startDate)),
                  }}
                  render={({ field }) => (
                    <Input
                      {...field}
                      type="date"
                      min={startDate}
                      onChange={(e) => {
                        field.onChange(e.target.value)
                      }}
                    />
                  )}
                />
              </FormControl>
            </FormRow>
            <FormRow>
              <FormControl>
                <FormLabel>Days Between Inquiries</FormLabel>
                <Controller
                  name="daysBetween"
                  control={control}
                  rules={{ min: 1, max: 365 }}
                  render={({ field }) => (
                    <NumberInput
                      min={1}
                      {...field}
                      onChange={(_, value) => field.onChange(value)}
                    >
                      <NumberInputField />
                      <NumberInputStepper>
                        <NumberIncrementStepper />
                        <NumberDecrementStepper />
                      </NumberInputStepper>
                    </NumberInput>
                  )}
                />
              </FormControl>
              <FormControl>
                <FormLabel>Time of Day for Inquiries</FormLabel>
                <Input
                  type="time"
                  {...register("timeOfDay", { value: "08:00" })}
                />
              </FormControl>
            </FormRow>
            <FormRow>
              <div>
                <Checkbox {...register("skipWeekends")}>
                  Skip Weekends{" "}
                </Checkbox>
              </div>
              <div>
                <Checkbox {...register("skipHolidays")}>Skip Holidays</Checkbox>
              </div>
            </FormRow>
            <FormRow>
              <Button type="submit">Save Timing</Button>
            </FormRow>
          </Flex>
        </form>
      </CardBody>
    </Card>
  )
}

export default TimerPanel
