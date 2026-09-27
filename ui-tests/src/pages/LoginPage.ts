import { By, WebDriver } from 'selenium-webdriver';
import { BasePage } from './BasePage';

export class LoginPage extends BasePage {
  private usernameInput = By.id('username');
  private passwordInput = By.id('password');
  private loginButton = By.id('btn-login');
  private alertBox = By.id('login-alert');

  constructor(driver: WebDriver) {
    super(driver);
  }

  async navigateTo(baseUrl: string = 'http://localhost:4000/index.html'): Promise<void> {
    await this.driver.get(baseUrl);
  }

  async login(username: string, password: string): Promise<void> {
    await this.type(this.usernameInput, username);
    await this.type(this.passwordInput, password);
    await this.click(this.loginButton);
  }

  async getAlertText(): Promise<string> {
    return await this.getText(this.alertBox);
  }

  async isAlertVisible(): Promise<boolean> {
    try {
      const el = await this.waitForElementVisible(this.alertBox, 3000);
      return await el.isDisplayed();
    } catch {
      return false;
    }
  }
}
