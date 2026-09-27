package com.enterprise.quality.api;

import com.enterprise.quality.api.models.Customer;
import com.enterprise.quality.api.utils.AuthHelper;
import com.enterprise.quality.api.utils.SpecBuilder;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

public class AuthorizationAndSecurityApiTest {

    @Test
    @DisplayName("TC-API-13: POST /api/auth/login - Successful login returns valid bearer token")
    public void testSuccessfulLogin() {
        Map<String, String> credentials = new HashMap<>();
        credentials.put("username", "admin");
        credentials.put("password", "Admin@123");

        given()
                .spec(SpecBuilder.getRequestSpec())
                .body(credentials)
        .when()
                .post("/api/auth/login")
        .then()
                .statusCode(200)
                .body("token", notNullValue())
                .body("role", equalTo("Admin"));
    }

    @Test
    @DisplayName("TC-API-14: POST /api/auth/login - Invalid credentials returns 401 Unauthorized")
    public void testInvalidLoginCredentials() {
        Map<String, String> credentials = new HashMap<>();
        credentials.put("username", "admin");
        credentials.put("password", "WrongPassword999");

        given()
                .spec(SpecBuilder.getRequestSpec())
                .body(credentials)
        .when()
                .post("/api/auth/login")
        .then()
                .statusCode(401)
                .body("error", equalTo("Unauthorized"));
    }

    @Test
    @DisplayName("TC-API-15: POST /api/customers - Missing Authorization header returns 401")
    public void testAccessProtectedEndpointWithoutToken() {
        Customer c = new Customer("CUST-9992", "Test", "User", "test@example.com", "Gold", "East", "Active");

        given()
                .spec(SpecBuilder.getRequestSpec())
                .body(c)
        .when()
                .post("/api/customers")
        .then()
                .statusCode(401)
                .body("error", equalTo("Unauthorized"));
    }

    @Test
    @DisplayName("TC-API-16: POST /api/customers - Invalid bearer token returns 403 Forbidden")
    public void testAccessProtectedEndpointWithInvalidToken() {
        Customer c = new Customer("CUST-9993", "Test", "User", "test@example.com", "Gold", "East", "Active");

        given()
                .spec(SpecBuilder.getAuthenticatedRequestSpec("invalid-bogus-token-xyz"))
                .body(c)
        .when()
                .post("/api/customers")
        .then()
                .statusCode(403)
                .body("error", equalTo("Forbidden"));
    }
}
