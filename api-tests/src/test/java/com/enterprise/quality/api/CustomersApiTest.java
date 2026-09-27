package com.enterprise.quality.api;

import com.enterprise.quality.api.config.TestConfig;
import com.enterprise.quality.api.models.Customer;
import com.enterprise.quality.api.utils.SpecBuilder;
import io.restassured.response.Response;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

public class CustomersApiTest {

    @Test
    @DisplayName("TC-API-01: GET /api/customers - Retrieve all customers and verify schema")
    public void testGetAllCustomers() {
        given()
                .spec(SpecBuilder.getRequestSpec())
        .when()
                .get("/api/customers")
        .then()
                .spec(SpecBuilder.getSuccessResponseSpec(200))
                .body("count", greaterThanOrEqualTo(12))
                .body("data", notNullValue())
                .body("data[0].customer_id", notNullValue())
                .body("data[0].tier", is(oneOf("Platinum", "Gold", "Silver", "Bronze")));
    }

    @Test
    @DisplayName("TC-API-02: GET /api/customers/:id - Retrieve existing customer by ID")
    public void testGetCustomerByIdSuccess() {
        given()
                .spec(SpecBuilder.getRequestSpec())
                .pathParam("id", "CUST-1001")
        .when()
                .get("/api/customers/{id}")
        .then()
                .spec(SpecBuilder.getSuccessResponseSpec(200))
                .body("customer_id", equalTo("CUST-1001"))
                .body("first_name", equalTo("Alice"))
                .body("tier", equalTo("Platinum"));
    }

    @Test
    @DisplayName("TC-API-03: GET /api/customers/:id - Non-existent customer returns 404")
    public void testGetCustomerByIdNotFound() {
        given()
                .spec(SpecBuilder.getRequestSpec())
                .pathParam("id", "CUST-9999")
        .when()
                .get("/api/customers/{id}")
        .then()
                .statusCode(404)
                .body("error", equalTo("Not Found"));
    }

    @Test
    @DisplayName("TC-API-04: POST /api/customers - Create new customer with valid payload")
    public void testCreateCustomerSuccess() {
        String uniqueId = "CUST-" + (2000 + (int)(Math.random() * 8000));
        Customer newCustomer = new Customer(
                uniqueId,
                "Robert",
                "Taylor",
                "robert." + uniqueId.toLowerCase() + "@example.com",
                "Gold",
                "West",
                "Active"
        );

        given()
                .spec(SpecBuilder.getAuthenticatedRequestSpec(TestConfig.ADMIN_TOKEN))
                .body(newCustomer)
        .when()
                .post("/api/customers")
        .then()
                .statusCode(201)
                .body("customer_id", equalTo(uniqueId))
                .body("message", equalTo("Customer created successfully"));
    }

    @Test
    @DisplayName("TC-API-05: POST /api/customers - Validation fails on invalid Tier (400 Bad Request)")
    public void testCreateCustomerInvalidTier() {
        Customer invalidCustomer = new Customer(
                "CUST-8888",
                "Test",
                "User",
                "test.invalid@example.com",
                "DiamondVIP", // Invalid tier
                "East",
                "Active"
        );

        given()
                .spec(SpecBuilder.getAuthenticatedRequestSpec(TestConfig.ADMIN_TOKEN))
                .body(invalidCustomer)
        .when()
                .post("/api/customers")
        .then()
                .statusCode(400)
                .body("error", equalTo("Bad Request"))
                .body("message", containsString("Invalid tier"));
    }

    @Test
    @DisplayName("TC-API-06: POST /api/customers - Missing mandatory fields returns 400 Bad Request")
    public void testCreateCustomerMissingMandatoryFields() {
        Customer incompleteCustomer = new Customer();
        incompleteCustomer.setCustomer_id("CUST-7777");

        given()
                .spec(SpecBuilder.getAuthenticatedRequestSpec(TestConfig.ADMIN_TOKEN))
                .body(incompleteCustomer)
        .when()
                .post("/api/customers")
        .then()
                .statusCode(400)
                .body("error", equalTo("Bad Request"));
    }
}
