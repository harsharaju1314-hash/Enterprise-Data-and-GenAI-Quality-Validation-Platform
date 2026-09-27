package com.enterprise.quality.api.config;

public class TestConfig {
    public static final String BASE_URL = System.getProperty("api.base.url", "http://localhost:4000");
    public static final String ADMIN_TOKEN = "admin-token-12345";
    public static final String ANALYST_TOKEN = "analyst-token-67890";
    public static final String SUPPORT_TOKEN = "support-token-54321";
}
