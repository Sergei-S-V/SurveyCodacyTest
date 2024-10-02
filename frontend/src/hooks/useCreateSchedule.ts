import { useMutation, useQueryClient } from "@tanstack/react-query"
import type { ApiError } from "../client"
import * as scheduleService from "../client/services/scheduleService"
import { handleError } from "../utils"
import useCustomToast from "./useCustomToast"

const useCreateSchedule = () => {
  const showToast = useCustomToast()
  const queryClient = useQueryClient()

  type TDataCreateSchedule = scheduleService.TDataCreateSchedule
  const mutation = useMutation<
    TDataCreateSchedule,
    ApiError,
    TDataCreateSchedule
  >({
    mutationFn: (schedule: TDataCreateSchedule) =>
      scheduleService.createSchedule(schedule).then((response) => response),
    onSuccess: () => {
      showToast("Success!", "Schedule created successfully.", "success")
    },
    onError: (err) => {
      handleError(err, showToast)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["schedule"] })
    },
  })

  const createNewSchedule = (data: TDataCreateSchedule) => {
    mutation.mutate(data)
  }

  return { createNewSchedule }
}

export default useCreateSchedule
