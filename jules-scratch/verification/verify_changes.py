from playwright.sync_api import sync_playwright, expect
import os

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Get the absolute path to the HTML file
        file_path = os.path.abspath('index.html')

        # Go to the local HTML file
        page.goto(f'file://{file_path}')

        # 1. Start the quiz
        page.get_by_role("button", name="Começar o Questionário").click()

        # Wait for the quiz screen to be visible
        expect(page.locator("#quiz-screen")).to_be_visible()

        # 2. Verify the "I haven't watched" checkbox and its functionality for the first anime
        first_anime_question = page.locator("#question-container-0")
        not_watched_checkbox = first_anime_question.get_by_label("Não Assisti")
        rating_slider = first_anime_question.get_by_role("slider")

        # Assert checkbox is present and slider is enabled by default
        expect(not_watched_checkbox).to_be_visible()
        expect(rating_slider).to_be_enabled()

        # 3. Click the checkbox and assert the slider is now disabled
        not_watched_checkbox.check()
        expect(rating_slider).to_be_disabled()

        # 4. Take a screenshot of the quiz screen with the disabled slider
        page.screenshot(path="jules-scratch/verification/verification.png")

        browser.close()

if __name__ == "__main__":
    run_verification()