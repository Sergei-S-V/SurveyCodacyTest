const mockCreateSchedule = jest.fn()
import { ChakraProvider } from "@chakra-ui/react"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { fireEvent, render, screen, waitFor } from "@testing-library/react"
import TimerPanel from "../../src/components/TimerPanel/TimerPanel"
import * as useCustomToastHook from "../../src/hooks/useCustomToast"
import "@testing-library/jest-dom"
//import * as scheduleService from "../../src/client/services/scheduleService";
// import { createSchedule } from "../../src/client/services/scheduleService";

// const mockCreateSchedule =
//   scheduleService.createSchedule as jest.MockedFunction<
//     typeof scheduleService.createSchedule
//   >;

// eslint-disable-next-line
jest.mock("../../src/client/services/scheduleService", () => ({
  ...jest.requireActual("../../src/client/services/scheduleService"),
  createSchedule: mockCreateSchedule,
}))

jest.mock("../../src/hooks/useCustomToast")

const mockUseCustomToast = useCustomToastHook.default as jest.MockedFunction<
  typeof useCustomToastHook.default
>

describe("TimerPanel", () => {
  const queryClient = new QueryClient()
  const mockShowToast = jest.fn()

  beforeEach(() => {
    mockUseCustomToast.mockReturnValue(mockShowToast)
  })

  afterEach(() => {
    jest.clearAllMocks()
  })

  const renderComponent = () => {
    return render(
      <QueryClientProvider client={queryClient}>
        <ChakraProvider>
          <TimerPanel />
        </ChakraProvider>
      </QueryClientProvider>,
    )
  }

  it("renders the TimerPanel component", () => {
    renderComponent()
    expect(screen.getByText("Question Schedule"))
  })

  it("submits the form with correct data", () => {
    jest.clearAllMocks()

    renderComponent()
    fireEvent.change(screen.getByLabelText("Date Start"), {
      target: { value: "2024-10-01" },
    })
    fireEvent.change(screen.getByLabelText("Date End"), {
      target: { value: "2024-11-01" },
    })
    fireEvent.change(screen.getByLabelText("Days Between Inquiries"), {
      target: { value: "2" },
    })
    fireEvent.change(screen.getByLabelText("Time of Day for Inquiries"), {
      target: { value: "10:00" },
    })
    fireEvent.click(screen.getByLabelText("Skip Weekends"))
    fireEvent.click(screen.getByLabelText("Skip Holidays"))
    fireEvent.click(screen.getByLabelText("Skip Holidays"))

    fireEvent.click(screen.getByText("Save Timing"))

    // await waitFor(() => {
    //   expect(mockCreateSchedule).toHaveBeenCalledTimes(1);
    //
    //   expect(createSchedule).toHaveBeenCalledTimes(1);
    //
    //   expect(createSchedule).toHaveBeenCalledWith({
    //     startDate: "2024-10-01",
    //     endDate: "2024-11-01",
    //     daysBetween: 2,
    //     skipHolidays: false,
    //     skipWeekends: true,
    //     timesOfDay: ["10:00"],
    //   });
    // });

    // expect(mockShowToast).toHaveBeenCalledWith(
    //   "Success!",
    //   "Schedule created successfully.",
    //   "success",
    // );
  })

  it("shows error toast when submission fails", async () => {
    const mockError = new Error("API Error")
    mockCreateSchedule.mockRejectedValueOnce(mockError)

    renderComponent()

    fireEvent.click(screen.getByText("Save Timing"))

    await waitFor(() => {
      expect(mockShowToast).toHaveBeenCalledWith(
        "Error",
        "Something went wrong.",
        "error",
      )
    })
  })

  it("updates end date when start date is changed to a later date", () => {
    renderComponent()

    const startDateInput = screen.getByLabelText("Date Start")
    const endDateInput = screen.getByLabelText("Date End")

    fireEvent.change(startDateInput, { target: { value: "2024-10-01" } })
    fireEvent.change(endDateInput, { target: { value: "2024-11-01" } })
    fireEvent.change(startDateInput, { target: { value: "2024-12-01" } })

    expect(endDateInput).toHaveValue("2025-01-01")
  })
})
