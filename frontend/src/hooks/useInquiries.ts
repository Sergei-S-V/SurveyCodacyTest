import { useQuery } from "@tanstack/react-query"
import * as InquiriesService from "../client/services/inquiriesService.ts"

function getInquiriesQueryOptions() {
  return {
    queryKey: ["inquiries"],
    queryFn: () => InquiriesService.readInquiries(),
  }
}

export function useInquiries() {
  return useQuery({
    ...getInquiriesQueryOptions(),
  })
}
