import { By, WebDriver, WebElement } from 'selenium-webdriver';
import { BasePage } from './BasePage';

export class DashboardPage extends BasePage {
  private userDisplay = By.id('user-display');
  private roleDisplay = By.id('role-display');
  private logoutButton = By.id('btn-logout');
  private refreshButton = By.id('btn-refresh');
  private kpiGrossVolume = By.id('kpi-gross-volume');
  private kpiTotalTxns = By.id('kpi-total-txns');
  private kpiAvgCsat = By.id('kpi-avg-csat');
  private filterTier = By.id('filter-tier');
  private filterRegion = By.id('filter-region');
  private searchInput = By.id('search-input');
  private applyFiltersBtn = By.id('btn-apply-filters');
  private resetFiltersBtn = By.id('btn-reset-filters');
  private customersTableRows = By.css('#customers-tbody tr');
  private emptyState = By.id('empty-state');
  private drilldownBadge = By.id('drilldown-badge');

  constructor(driver: WebDriver) {
    super(driver);
  }

  async getUserName(): Promise<string> {
    return await this.getText(this.userDisplay);
  }

  async getRoleName(): Promise<string> {
    return await this.getText(this.roleDisplay);
  }

  async getGrossVolume(): Promise<string> {
    return await this.getText(this.kpiGrossVolume);
  }

  async getTotalTxns(): Promise<string> {
    return await this.getText(this.kpiTotalTxns);
  }

  async getAvgCsat(): Promise<string> {
    return await this.getText(this.kpiAvgCsat);
  }

  async selectTier(tier: string): Promise<void> {
    const el = await this.waitForElementVisible(this.filterTier);
    await el.sendKeys(tier);
  }

  async selectRegion(region: string): Promise<void> {
    const el = await this.waitForElementVisible(this.filterRegion);
    await el.sendKeys(region);
  }

  async enterSearchText(query: string): Promise<void> {
    await this.type(this.searchInput, query);
  }

  async clickApplyFilters(): Promise<void> {
    await this.click(this.applyFiltersBtn);
  }

  async clickResetFilters(): Promise<void> {
    await this.click(this.resetFiltersBtn);
  }

  async clickRefresh(): Promise<void> {
    await this.click(this.refreshButton);
  }

  async clickLogout(): Promise<void> {
    await this.click(this.logoutButton);
  }

  async getTableRows(): Promise<WebElement[]> {
    return await this.driver.findElements(this.customersTableRows);
  }

  async isEmptyStateVisible(): Promise<boolean> {
    try {
      const el = await this.waitForElement(this.emptyState, 2000);
      return await el.isDisplayed();
    } catch {
      return false;
    }
  }

  async isDrilldownBadgeVisible(): Promise<boolean> {
    try {
      const el = await this.waitForElement(this.drilldownBadge, 2000);
      return await el.isDisplayed();
    } catch {
      return false;
    }
  }
}
