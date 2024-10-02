import type { CancelablePromise } from "../core/CancelablePromise";
import { OpenAPI } from "../core/OpenAPI";
import { request as __request } from "../core/request";

export interface TDataCreateSchedule {
  startDate: string
  endDate?: string
  daysBetween: number
  skipWeekends: boolean
  skipHolidays: boolean
  timesOfDay: string[]
}

export type TDataReadSchedule = {
  id: string;
};

export function createSchedule(
  schedule: TDataCreateSchedule,
): CancelablePromise<TDataCreateSchedule> {
  return __request(OpenAPI, {
    method: "POST",
    url: "/api/v1/schedule",
    body: { schedule },
    mediaType: "application/json",
    errors: {
      422: "Validation Error",
    },
  });
}

export function readSchedule(
  data: TDataReadSchedule,
): CancelablePromise<TDataCreateSchedule> {
  const { id } = data;
  return __request(OpenAPI, {
    method: "GET",
    url: "/api/v1/schedulew",
    path: {
      id,
    },
    errors: {
      422: "Validation Error",
    },
  });
}
