import dayjs from "dayjs"
import timezone from "dayjs/plugin/timezone"
import utc from "dayjs/plugin/utc"

// Dayjs Configurations
/* eslint-disable */
dayjs.extend(utc)
dayjs.extend(timezone)
/* eslint-enable */

// Format ISO date to the user's timezone.
// ex. Sep 17, 2024 14:13 PM
export function formatDate(date: string): string {
  const invalidDateMessage = "Invalid Date"
  if (typeof date !== "string") return invalidDateMessage
  // Unsafe access to 'error' typed value is handled by dayjs' isValid function
  /* eslint-disable */
  const parsedDate = dayjs.utc(date)
  const userTimezone = dayjs.tz.guess()
  return parsedDate.isValid()
    ? parsedDate.tz(userTimezone).format("MMM DD, YYYY hh:mm A")
    : invalidDateMessage
  /* eslint-enable */
}
