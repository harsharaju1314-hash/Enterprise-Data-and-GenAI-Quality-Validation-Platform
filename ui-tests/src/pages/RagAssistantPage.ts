import { By, WebDriver } from 'selenium-webdriver';
import { BasePage } from './BasePage';

export class RagAssistantPage extends BasePage {
  private chatInput = By.id('chat-input');
  private sendButton = By.id('btn-send');
  private chatMessages = By.css('#chat-messages .message-ai');

  constructor(driver: WebDriver) {
    super(driver);
  }

  async navigateTo(baseUrl: string = 'http://localhost:4000/rag_assistant.html'): Promise<void> {
    await this.driver.get(baseUrl);
  }

  async askQuestion(question: string): Promise<void> {
    await this.type(this.chatInput, question);
    await this.click(this.sendButton);
  }

  async getLatestAiResponse(): Promise<string> {
    const messages = await this.driver.findElements(this.chatMessages);
    if (messages.length === 0) return '';
    const lastMsg = messages[messages.length - 1];
    return await lastMsg.getText();
  }
}
