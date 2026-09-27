import { WebDriver, By, until, WebElement } from 'selenium-webdriver';

export abstract class BasePage {
  protected driver: WebDriver;

  constructor(driver: WebDriver) {
    this.driver = driver;
  }

  async waitForElement(locator: By, timeoutMs: number = 8000): Promise<WebElement> {
    return await this.driver.wait(until.elementLocated(locator), timeoutMs);
  }

  async waitForElementVisible(locator: By, timeoutMs: number = 8000): Promise<WebElement> {
    const el = await this.waitForElement(locator, timeoutMs);
    await this.driver.wait(until.elementIsVisible(el), timeoutMs);
    return el;
  }

  async click(locator: By): Promise<void> {
    const el = await this.waitForElementVisible(locator);
    await el.click();
  }

  async type(locator: By, text: string): Promise<void> {
    const el = await this.waitForElementVisible(locator);
    await el.clear();
    await el.sendKeys(text);
  }

  async getText(locator: By): Promise<string> {
    const el = await this.waitForElementVisible(locator);
    return await el.getText();
  }
}
