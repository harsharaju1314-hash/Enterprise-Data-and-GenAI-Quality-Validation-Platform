import { Builder, WebDriver } from 'selenium-webdriver';
import chrome from 'selenium-webdriver/chrome';
import { expect } from 'chai';
import { LoginPage } from '../pages/LoginPage';
import { DashboardPage } from '../pages/DashboardPage';
import { RagAssistantPage } from '../pages/RagAssistantPage';

describe('Enterprise Analytics & AI Portal - Selenium UI Regression Suite', function () {
  this.timeout(35000);
  let driver: WebDriver;
  let loginPage: LoginPage;
  let dashboardPage: DashboardPage;
  let ragPage: RagAssistantPage;

  before(async function () {
    const options = new chrome.Options();
    options.addArguments('--headless');
    options.addArguments('--disable-gpu');
    options.addArguments('--no-sandbox');
    options.addArguments('--window-size=1920,1080');

    driver = await new Builder()
      .forBrowser('chrome')
      .setChromeOptions(options)
      .build();

    loginPage = new LoginPage(driver);
    dashboardPage = new DashboardPage(driver);
    ragPage = new RagAssistantPage(driver);
  });

  after(async function () {
    if (driver) {
      await driver.quit();
    }
  });

  it('TC-UI-01: Invalid login displays appropriate error notification', async function () {
    await loginPage.navigateTo();
    await loginPage.login('invalid_user', 'WrongPass123');
    const isAlertShown = await loginPage.isAlertVisible();
    expect(isAlertShown).to.be.true;
    const alertMsg = await loginPage.getAlertText();
    expect(alertMsg.toLowerCase()).to.satisfy((s: string) => s.includes('invalid credentials') || s.includes('invalid username'));
  });

  it('TC-UI-02: Valid login authenticates and navigates to Executive Dashboard', async function () {
    await loginPage.navigateTo();
    await loginPage.login('admin', 'Admin@123');
    await driver.sleep(1000);
    const currentUrl = await driver.getCurrentUrl();
    expect(currentUrl).to.include('dashboard.html');
  });

  it('TC-UI-03: Dashboard loads verified KPIs from relational layer', async function () {
    const grossVolume = await dashboardPage.getGrossVolume();
    const totalTxns = await dashboardPage.getTotalTxns();
    const avgCsat = await dashboardPage.getAvgCsat();

    expect(grossVolume).to.include('$');
    expect(Number(totalTxns)).to.be.at.least(16);
    expect(avgCsat).to.include('/ 5.0');
  });

  it('TC-UI-04: Filter application dynamically filters customer records by Tier', async function () {
    await dashboardPage.selectTier('Platinum');
    await dashboardPage.clickApplyFilters();
    await driver.sleep(600);

    const rows = await dashboardPage.getTableRows();
    expect(rows.length).to.be.greaterThan(0);
    for (const row of rows) {
      const text = await row.getText();
      expect(text).to.include('Platinum');
    }
  });

  it('TC-UI-05: Global search filters table by specific customer ID', async function () {
    await dashboardPage.clickResetFilters();
    await dashboardPage.enterSearchText('CUST-1001');
    await dashboardPage.clickApplyFilters();
    await driver.sleep(600);

    const rows = await dashboardPage.getTableRows();
    expect(rows.length).to.equal(1);
    const rowText = await rows[0].getText();
    expect(rowText).to.include('Alice Smith');
  });

  it('TC-UI-06: Customer drill-down triggers visual drill-down badge state', async function () {
    await dashboardPage.clickResetFilters();
    await driver.sleep(500);
    const rows = await dashboardPage.getTableRows();
    expect(rows.length).to.be.greaterThan(0);

    // Click drill down on first row
    const drillBtn = await rows[0].findElement({ css: 'button' });
    await drillBtn.click();
    await driver.sleep(500);

    const isBadgeVisible = await dashboardPage.isDrilldownBadgeVisible();
    expect(isBadgeVisible).to.be.true;
  });

  it('TC-UI-07: Empty filter combinations render clean empty-state UI', async function () {
    await dashboardPage.clickResetFilters();
    await dashboardPage.selectTier('Platinum');
    await dashboardPage.selectRegion('North'); // Non-existent combination
    await dashboardPage.clickApplyFilters();
    await driver.sleep(500);

    const isEmpty = await dashboardPage.isEmptyStateVisible();
    expect(isEmpty).to.be.true;
  });

  it('TC-UI-08: Access control renders authenticated Admin role badge', async function () {
    const roleText = await dashboardPage.getRoleName();
    expect(roleText).to.equal('Admin');
  });

  it('TC-UI-09: Dashboard refresh button triggers re-rendering of live metrics', async function () {
    await dashboardPage.clickResetFilters();
    await dashboardPage.clickRefresh();
    await driver.sleep(600);

    const rows = await dashboardPage.getTableRows();
    expect(rows.length).to.be.at.least(12);
  });

  it('TC-UI-10: User logout clears session and navigates back to login view', async function () {
    await dashboardPage.clickLogout();
    await driver.sleep(600);
    const currentUrl = await driver.getCurrentUrl();
    expect(currentUrl).to.include('index.html');
  });
});
