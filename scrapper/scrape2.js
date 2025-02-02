
const puppeteer = require("puppeteer");
const fs = require("fs");

(async () => {
    const url = "https://www.digitalocean.com/customers";
    console.log("🚀 Launching browser...");
    let browser = await puppeteer.launch({ headless: true });

    try {
        const page = await browser.newPage();
        console.log(`🔗 Navigating to main page: ${url}`);
        await page.goto(url, { waitUntil: "networkidle2", timeout: 60000 });

        console.log("🔍 Extracting customer story links...");
        const links = await page.evaluate(() => {
            return Array.from(
                document.querySelectorAll(
                    "#__next > div.Layout__StyledLayout-sc-3a10f19e-0.etQQpa > div.CustomerCardsStyles__StyledCustomerCardsWrapper-sc-72ac5ef3-0.boCwOR > div > div.CustomerCardsStyles__StyledCustomerCardsContainer-sc-72ac5ef3-2.fkfRA a"
                )
            )
                .map((el) => el.href)
                .filter((href) => !href.includes("load-more")); // Exclude "Load More" button
        });

        console.log(`✅ Found ${links.length} customer story links.`);

        let results = [];

        for (let link of links) {
            console.log(`🔍 Visiting: ${link}`);

            let maxRetries = 3;
            let retryCount = 0;
            let success = false;
            let customerPage;

            while (retryCount < maxRetries && !success) {
                try {
                    customerPage = await browser.newPage();
                    await customerPage.goto(link, { waitUntil: "networkidle2", timeout: 60000 });

                    console.log("📌 Extracting testimonial details...");
                    const testimonialData = await customerPage.evaluate((link) => {
                        let figcaption = document.querySelector(
                            ".HeroQuoteStyles__StyledQuoteSectionContent-sc-e3812a2-5.YqNBJ figcaption"
                        );

                        if (!figcaption) {
                            console.warn(`⚠️ No testimonial found for ${link}`);
                            return null;
                        }

                        let text = figcaption.innerText.trim();
                        let parts = text.split(",").map((t) => t.trim());

                        if (parts.length < 3) {
                            console.warn(`⚠️ Invalid testimonial format at ${link}: ${text}`);
                            return null;
                        }

                        return {
                            company: parts[2], // Company name
                            testimonial: {
                                name: parts[0], // Person's name
                                title: parts[1], // Job title
                                company: parts[2], // Company name again
                                URL: link, // The URL being scraped
                            },
                        };
                    }, link);

                    if (testimonialData) {
                        results.push(testimonialData);
                        console.log("✅ Testimonial extracted successfully.");
                    } else {
                        console.warn(`⚠️ Skipping ${link} due to missing/invalid data.`);
                    }

                    success = true; // Mark as successful if no errors occurred
                } catch (error) {
                    retryCount++;
                    console.error(`❌ Error scraping ${link} (Attempt ${retryCount}/${maxRetries}): ${error.message}`);
                    if (retryCount === maxRetries) {
                        console.error(`🚫 Skipping ${link} after ${maxRetries} failed attempts.`);
                    }
                } finally {
                    if (customerPage) await customerPage.close();
                }
            }
        }

        console.log("📁 Writing results to customers.json...");
        fs.writeFileSync("digital_ocean-case_studies.json", JSON.stringify(results, null, 2));

        console.log("🎉 Scraping completed! Data saved to customers.json.");
    } catch (error) {
        console.error("❌ Fatal error:", error.message);
    } finally {
        await browser.close();
        console.log("🚪 Browser closed.");
    }
})();
