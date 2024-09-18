/**
 * @jest-environment jsdom
 */

import {fireEvent, render, screen} from "@testing-library/react";
import userEvent from '@testing-library/user-event'
import {Inquiries} from "../../src/routes/_layout/inquiries";
import '@testing-library/jest-dom'
import {MAX_INQUIRY_LENGTH, MIN_INQUIRY_LENGTH} from "../../src/components/Inquiries/AddInquiry";

jest.mock("../../src/components/Inquiries/InquiriesTable", () => ({
    __esModule: true,
    default: () => (<div/>)
}));


jest.mock("@tanstack/react-query", () => ({
    ...jest.requireActual("@tanstack/react-query"),
    useQueryClient: () => {
    },
    useMutation: () => ({
        mutate: () => {
        }
    })
}));


describe("Add Inquiry", () => {
    beforeEach(async ()=>{
        render(<Inquiries/>)
        await userEvent.click(screen.getByText("Add Inquiry"))
    })
    it("should display add modal when user presses Add Inquiry button", async () => {
        const textArea = await screen.getByTestId("add-inquiry-text")
        fireEvent.change(textArea, {target: {value: "Why do birds suddenly appear every time you are near?"}})
        await userEvent.click(screen.getByTestId("submit-add-inquiry"))
    })
    it("should display required error when no string is entered", async() => {
        await userEvent.click(screen.getByTestId("submit-add-inquiry"))
        await screen.getByText("Inquiry text is required.")
    })
    it("should display error message when user enters inquiry less than 10 characters", async () => {
        const textArea = await screen.getByTestId("add-inquiry-text")
        const shortString = "W".repeat(MIN_INQUIRY_LENGTH - 1)
        fireEvent.change(textArea, {target: {value: shortString}})
        await userEvent.click(screen.getByTestId("submit-add-inquiry"))
        await screen.getByText("Inquiry must be at least 10 characters.")
    })
        it("should display error message when user enters inquiry more than 255 characters", async () => {
            const textArea = await screen.getByTestId("add-inquiry-text");
            const longString = "W".repeat(MAX_INQUIRY_LENGTH + 1)
            fireEvent.change(textArea, {target: {value: longString}})
            await userEvent.click(screen.getByTestId("submit-add-inquiry"))
            await screen.getByText("Inquiry can not be greater than 255 characters.")
        })
    })
/*
test.describe('AddInquiry Component', () => {
    test('should submit a new inquiry', async ({ page }) => {
        await page.goto('/inquiries');
        await page.click('button[id="add-inquiry-show-modal"]')
        await page.fill('textarea[name="text"]', 'Why do birds suddenly appear every time you are near?');
        await page.click('button[type="submit"]');
        await expect(page.locator('text=Inquiry created successfully.')).toBeVisible();
    });

    test('should show required error', async ({ page }) => {
        await page.goto('/inquiries');
        await page.click('button[id="add-inquiry-show-modal"]')
        await page.click('button[type="submit"]');
        await expect(page.locator('text=Inquiry text is required.')).toBeVisible();
    });

    test('should show min length error', async ({ page }) => {
        await page.goto('/inquiries');
        await page.click('button[id="add-inquiry-show-modal"]')
        await page.fill('textarea[name="text"]', 'Why do?');
        await page.click('button[type="submit"]');
        await expect(page.locator('text=Inquiry must be at least 10 characters.')).toBeVisible();
    });

    test('should show max length error', async ({ page }) => {
        await page.goto('/inquiries');
        await page.click('button[id="add-inquiry-show-modal"]')
        await page.fill('textarea[name="text"]', 'Why?'.repeat(100));
        await page.click('button[type="submit"]');
        await expect(page.locator('text=Inquiry can not be greater than 255 characters.')).toBeVisible();
    });
    test('should show capitalization error', async ({ page }) => {
        await page.goto('/inquiries');
        await page.click('button[id="add-inquiry-show-modal"]')
        await page.fill('textarea[name="text"]', 'why do birds suddenly appear every time you are near?');
        await page.click('button[type="submit"]');
        await expect(page.locator('text=Inquiry must start with a capital letter.')).toBeVisible();
    });
    test('should not allow duplicate inquiries', async ({ page }) => {
        await page.goto('/inquiries');
        await page.click('button[id="add-inquiry-show-modal"]')
        await page.fill('textarea[name="text"]', 'Why do birds suddenly appear every time you are near?');
        await page.click('button[type="submit"]');
        await page.click('button[id="add-inquiry-show-modal"]')
        await page.fill('textarea[name="text"]', 'Why do birds suddenly appear every time you are near?');
        await page.click('button[type="submit"]');
        await expect(page.locator('text=This inquiry already exists.')).toBeVisible();
    });
});
*/