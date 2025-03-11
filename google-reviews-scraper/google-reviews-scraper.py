import asyncio
import json
from dataclasses import dataclass
from typing import List, Optional
from playwright.async_api import async_playwright, Page, ElementHandle
from tqdm import tqdm

# Constants for CSS selectors and timeouts
REVIEW_SELECTOR = ".jftiEf"
REVIEWER_NAME_SELECTOR = ".d4r55"
REVIEWER_LINK_SELECTOR = "button[data-href]"
REVIEWER_IMAGE_SELECTOR = ".NBa7we"
RATING_SELECTOR = ".hCCjke.google-symbols.NhBTye.elGi1d"
DATE_SELECTOR = ".rsqaWe"
TEXT_SELECTOR = ".wiI7pd"
MORE_BUTTON_SELECTOR = "button.w8nwRe.kyuRq"
PHOTO_SELECTOR = ".Tya61d"
LIKES_SELECTOR = ".pkWtMe"
SCROLL_CONTAINER_SELECTOR = ".m6QErb.DxyBCb.kA9KIf.dS8AEf"

TIMEOUT = 3000  # Milliseconds

@dataclass
class ReviewData:
    """Data structure for storing review information"""
    reviewer_name: str
    reviewer_link: str
    reviewer_image: str
    rating: int
    date: str
    text: str
    photos: List[str]
    likes_count: str

class ReviewsScraper:
    async def init_browser(self) -> tuple:
        """Initialize browser and page"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled']
        )
        self.page = await self.browser.new_page(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
        )
        
        # Hide automation flags
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => false });
        """)
        
        return self.playwright, self.browser, self.page

    async def _extract_text(self, element: Optional[ElementHandle]) -> str:
        """Helper method to extract text from an element."""
        return await element.inner_text() if element else ""

    async def _extract_attribute(self, element: Optional[ElementHandle], attribute: str) -> str:
        """Helper method to extract an attribute from an element."""
        return await element.get_attribute(attribute) if element else ""

    async def extract_review_data(self, review_element: ElementHandle) -> Optional[ReviewData]:
        """Extract data from a single review."""
        try:
            # Extract reviewer details
            reviewer_name = await self._extract_text(await review_element.query_selector(REVIEWER_NAME_SELECTOR))
            reviewer_link = await self._extract_attribute(await review_element.query_selector(REVIEWER_LINK_SELECTOR), "data-href")
            reviewer_image = await self._extract_attribute(await review_element.query_selector(REVIEWER_IMAGE_SELECTOR), "src")

            # Extract rating
            stars = await review_element.query_selector_all(RATING_SELECTOR)
            rating = len(stars)

            # Extract date and text
            date = await self._extract_text(await review_element.query_selector(DATE_SELECTOR))
            text = await self._extract_text(await review_element.query_selector(TEXT_SELECTOR))

            # Expand text if "More" button exists
            more_button = await review_element.query_selector(MORE_BUTTON_SELECTOR)
            if more_button:
                try:
                    await more_button.click()
                    await review_element.wait_for_selector(TEXT_SELECTOR, timeout=TIMEOUT)
                    expanded_text = await self._extract_text(await review_element.query_selector(TEXT_SELECTOR))
                    if len(expanded_text) > len(text):
                        text = expanded_text
                except Exception:
                    pass

            # Extract photos
            photos = []
            photo_elements = await review_element.query_selector_all(PHOTO_SELECTOR)
            for photo in photo_elements:
                style = await self._extract_attribute(photo, "style")
                if style and "url(" in style:
                    url = style.split('url("')[1].split('")')[0]
                    photos.append(url)

            # Extract likes count
            likes_count = await self._extract_text(await review_element.query_selector(LIKES_SELECTOR))

            return ReviewData(
                reviewer_name=reviewer_name,
                reviewer_link=reviewer_link,
                reviewer_image=reviewer_image,
                rating=rating,
                date=date,
                text=text,
                photos=photos,
                likes_count=likes_count,
            )
        except Exception as e:
            print(f"Error extracting review data: {e}")
            return None

    async def scroll_reviews(self, page: Page) -> bool:
        """Scroll the reviews panel and wait for new content."""
        try:
            reviews_container = await page.query_selector(SCROLL_CONTAINER_SELECTOR)
            if not reviews_container:
                await page.evaluate("window.scrollBy(0, 500)")
                await page.wait_for_timeout(TIMEOUT)
                return True

            prev_review_count = len(await page.query_selector_all(REVIEW_SELECTOR))
            await reviews_container.evaluate("(element) => { element.scrollTop = element.scrollHeight; }")
            await page.wait_for_timeout(TIMEOUT)
            current_review_count = len(await page.query_selector_all(REVIEW_SELECTOR))
            return current_review_count > prev_review_count
        except Exception as e:
            print(f"Error scrolling reviews: {e}")
            return False

    async def scrape_reviews(self, url: str, max_reviews=float('inf')) -> List[ReviewData]:
        """Scrape reviews from a single URL."""
        playwright, browser, page = await self.init_browser()
        reviews = []
        processed_review_ids = set()

        progress_total = max_reviews if max_reviews != float('inf') else None
        pbar = tqdm(total=progress_total, desc="Scraping reviews", dynamic_ncols=True)

        consecutive_failures = 0
        max_consecutive_failures = 10

        try:
            await page.goto(url, timeout=30000, wait_until="networkidle")
            await page.wait_for_timeout(TIMEOUT)

            while consecutive_failures < max_consecutive_failures:
                if len(reviews) >= max_reviews:
                    break

                review_elements = await page.query_selector_all(REVIEW_SELECTOR)
                for review in review_elements:
                    if len(reviews) >= max_reviews:
                        break

                    review_id = await self._extract_attribute(review, "data-review-id")
                    if review_id and review_id not in processed_review_ids:
                        review_data = await self.extract_review_data(review)
                        if review_data:
                            reviews.append(review_data)
                            processed_review_ids.add(review_id)
                            pbar.update(1)
                            pbar.set_postfix(Reviews=len(reviews))

                if not await self.scroll_reviews(page):
                    consecutive_failures += 1
                else:
                    consecutive_failures = 0

            pbar.close()
        except Exception as e:
            print(f"Error during scraping: {e}")
            pbar.close()
        finally:
            await browser.close()
            await playwright.stop()

        return reviews

    def save_reviews(self, reviews: List[ReviewData], filename: str = "reviews_output.json"):
        """Save reviews to a JSON file."""
        if not reviews:
            return

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(
                    [self._review_to_dict(review) for review in reviews],
                    f,
                    indent=4,
                    ensure_ascii=False
                )
            print(f"Saved {len(reviews)} reviews to '{filename}'.")
        except Exception as e:
            print(f"Error saving reviews: {e}")

    def _review_to_dict(self, review: ReviewData) -> dict:
        """Convert ReviewData to dictionary for JSON serialization."""
        return {
            "reviewer_name": review.reviewer_name,
            "reviewer_link": review.reviewer_link,
            "reviewer_image": review.reviewer_image,
            "rating": review.rating,
            "date": review.date,
            "text": review.text,
            "photos": review.photos,
            "likes_count": review.likes_count
        }

async def main():
    url = "https://www.google.com/maps/place/Pequod's+Pizza/@41.921934,-87.6669261,676m/data=!3m1!1e3!4m8!3m7!1s0x880fd2e43edcab43:0xfa179f0b298abc4d!8m2!3d41.921934!4d-87.6643512!9m1!1b1!16s%2Fg%2F1hc0v95qd?entry=ttu&g_ep=EgoyMDI1MDMwNC4wIKXMDSoJLDEwMjExNDUzSAFQAw%3D%3D"
    
    try:
        target_reviews = int(input("How many reviews would you like to scrape? "))
        if target_reviews <= 0:
            target_reviews = float('inf')
    except ValueError:
        target_reviews = float('inf')
    
    scraper = ReviewsScraper()
    reviews = await scraper.scrape_reviews(url, max_reviews=target_reviews)
    scraper.save_reviews(reviews)

if __name__ == "__main__":
    asyncio.run(main())