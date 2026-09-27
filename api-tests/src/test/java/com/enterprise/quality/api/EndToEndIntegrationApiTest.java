package com.enterprise.quality.api;

import com.enterprise.quality.api.models.Customer;
import com.enterprise.quality.api.models.ServiceRequest;
import com.enterprise.quality.api.utils.AuthHelper;
import com.enterprise.quality.api.utils.SpecBuilder;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

public class EndToEndIntegrationApiTest {

    @Test
    @DisplayName("TC-API-17: End-to-End Workflow: Auth -> Create Customer -> File SR -> Resolve SR -> Validate Metrics")
    public void testCompleteEnterpriseBusinessFlow() {
        // Step 1: Login & obtain Token
        String token = AuthHelper.loginAndGetToken("admin", "Admin@123");
        org.junit.jupiter.api.Assertions.assertNotNull(token, "Login failed to generate token");

        // Step 2: Create new enterprise Customer
        String custId = "CUST-E2E-" + (int)(Math.random() * 9000);
        Customer cust = new Customer(custId, "Workflow", "Tester", custId.toLowerCase() + "@enterprise.test", "Platinum", "East", "Active");

        given()
                .spec(SpecBuilder.getAuthenticatedRequestSpec(token))
                .body(cust)
        .when()
                .post("/api/customers")
        .then()
                .statusCode(201)
                .body("customer_id", equalTo(custId));

        // Step 3: Create Service Request for this customer
        String srId = "SR-E2E-" + (int)(Math.random() * 9000);
        ServiceRequest sr = new ServiceRequest(srId, custId, "Billing", "High", "Automated E2E billing test request");

        given()
                .spec(SpecBuilder.getAuthenticatedRequestSpec(token))
                .body(sr)
        .when()
                .post("/api/service-requests")
        .then()
                .statusCode(201)
                .body("request_id", equalTo(srId))
                .body("status", equalTo("Open"));

        // Step 4: Resolve the Service Request
        Map<String, Object> resolvePayload = new HashMap<>();
        resolvePayload.put("satisfaction_score", 5);

        given()
                .spec(SpecBuilder.getAuthenticatedRequestSpec(token))
                .body(resolvePayload)
                .pathParam("id", srId)
        .when()
                .put("/api/service-requests/{id}/resolve")
        .then()
                .statusCode(200)
                .body("message", containsString("marked as Closed"));

        // Step 5: Verify Global Metrics endpoint
        given()
                .spec(SpecBuilder.getRequestSpec())
        .when()
                .get("/api/metrics")
        .then()
                .statusCode(200)
                .body("total_service_requests", greaterThanOrEqualTo(15));
    }
}
