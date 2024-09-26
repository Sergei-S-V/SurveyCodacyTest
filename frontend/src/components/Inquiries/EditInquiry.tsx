import {
  Button,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalFooter,
  ModalHeader,
  ModalOverlay,
  Textarea,
} from "@chakra-ui/react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type SubmitHandler, useForm } from "react-hook-form"

import type { ApiError } from "../../client"
import type { InquiryCreate } from "../../client/models"
import * as InquiriesService from "../../client/services"
import useCustomToast from "../../hooks/useCustomToast"
import { handleError } from "../../utils"

const MIN_LENGTH = 10
const MAX_LENGTH = 256

function isValidUnicode(str: string): boolean {
  let retval: boolean
  try {
    retval = str === decodeURIComponent(encodeURIComponent(str))
  } catch {
    retval = false
  }
  return retval
}

interface InquiryModalProps {
  isOpen: boolean
  onClose: () => void
  inquiry?: InquiryCreate
}

const InquiryModal = ({ isOpen, onClose, inquiry }: InquiryModalProps) => {
  const queryClient = useQueryClient()
  const showToast = useCustomToast()

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<InquiryCreate>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      text: inquiry?.text ?? "",
    },
  })

  const mutation = useMutation({
    mutationFn: inquiry?.id
      ? (data: InquiryCreate) =>
          InquiriesService.updateInquiry({
            inquiryId: inquiry.id ?? "",
            requestBody: data,
          })
      : (data: InquiryCreate) =>
          InquiriesService.createInquiry({ requestBody: data }),
    onSuccess: () => {
      showToast(
        "Success!",
        inquiry?.id
          ? "Inquiry updated successfully."
          : "Inquiry created successfully.",
        "success",
      )
      reset()
      onClose()
    },
    onError: (err: ApiError) => {
      handleError(err, showToast)
    },
    onSettled: async () => {
      await queryClient.invalidateQueries({ queryKey: ["inquiries"] })
    },
  })

  const onSubmit: SubmitHandler<InquiryCreate> = (data) => {
    mutation.mutate(data)
  }

  return (
    <>
      <Modal
        isOpen={isOpen}
        onClose={onClose}
        size={{ base: "sm", md: "md" }}
        isCentered
      >
        <ModalOverlay />
        <ModalContent as="form" onSubmit={handleSubmit(onSubmit)}>
          <ModalHeader
            id={
              inquiry?.id ? "edit-inquiry-show-modal" : "add-inquiry-show-modal"
            }
          >
            {inquiry?.id ? "Edit Inquiry" : "Add Inquiry"}
          </ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            <FormControl isInvalid={!!errors.text}>
              <FormLabel htmlFor="text">Inquiry Text</FormLabel>
              <Textarea
                id="text"
                data-testid={
                  inquiry?.id ? "edit-inquiry-text" : "add-inquiry-text"
                }
                {...register("text", {
                  required: "Inquiry text is required.",
                  minLength: {
                    value: MIN_LENGTH,
                    message: `Inquiry must be at least ${MIN_LENGTH} characters.`,
                  },
                  maxLength: {
                    value: MAX_LENGTH,
                    message: `Inquiry can not be greater than ${MAX_LENGTH} characters.`,
                  },
                  validate: (value: string) =>
                    isValidUnicode(value) ||
                    "Inquiry must be a valid unicode string.",
                })}
                placeholder={
                  inquiry?.id
                    ? "Edit the text of your inquiry."
                    : "Enter the text of your inquiry."
                }
              />
              {errors.text && (
                <FormErrorMessage>{errors.text.message}</FormErrorMessage>
              )}
            </FormControl>
          </ModalBody>

          <ModalFooter gap={3}>
            <Button
              isLoading={isSubmitting}
              variant="primary"
              type="submit"
              data-testid={
                inquiry?.id ? "submit-edit-inquiry" : "submit-add-inquiry"
              }
            >
              Save
            </Button>
            <Button onClick={onClose}>Cancel</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  )
}

export default InquiryModal
