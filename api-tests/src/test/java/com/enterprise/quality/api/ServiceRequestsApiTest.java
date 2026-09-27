package com.enterprise.quality.api;

import com.enterprise.quality.api.config.TestConfig;
import com.enterprise.quality.api.models.ServiceRequest;
import com.enterprise.quality.api.utils.SpecBuilder;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

public class ServiceRequestsApiTest {

    @Test
    @DisplayName("TC-API-07: GET /api/service-requests - Filter by category Billing")
    public void testFilterServiceRequestsByCategory() {
        given()
                .spec(SpecBuilder.getRequestSpec())
                .queryParam("category", "Billing")
        .when()
                .get("/api/service-requests")
        .then()
                .spec(SpecBuilder.getSuccessResponseSpec(200))
                .body("data", everyItem(hasEntry("category", "Billing")));
    }

    @Test
    @DisplayName("TC-API-08: POST /api/service-requests - Create valid service request")
    public void testCreateServiceRequestSuccess() {
        String uniqueSrId = "SR-" + (3000 + (int)(Math.random() * 6000));
        ServiceRequest req = new ServiceRequest(
                uniqueSrId,
                "CUST-1001",
                "Technical",
                "High",
                "Application timeout on high concurrency run"
        );

        given()
                .spec(SpecBuilder.getAuthenticatedRequestSpec(TestConfig.ADMIN_TOKEN))
                .body(req)
        .when()
                .post("/api/service-requests")
        .then()
                .statusCode(201)
                .body("request_id", equalTo(uniqueSrId))
                .body("status", equalTo("Open"));
    }

    @Test
    @DisplayName("TC-API-09: POST /api/service-requests - Validation error on invalid Priority")
    public void testCreateServiceRequestInvalidPriority() {
        ServiceRequest req = new ServiceRequest(
                "SR-9991",
                "CUST-1001",
                "Technical",
                "CRITICAL_IMMEDIATE", // Invalid priority
                "Invalid priority test"
        );

        given()
                .spec(SpecBuilder.getAuthenticatedRequestSpec(TestConfig.ADMIN_TOKEN))
                .body(req)
        .when()
                .post("/api/service-requests")
        .then()
                .statusCode(400)
                .body("error", equalTo("Bad Request"))
                .body("message", containsString("Invalid priority"));
    }

    @Test
    @DisplayName("TC-API-10: PUT /api/service-requests/:id/resolve - Resolve request with valid CSAT")
    public void testResolveServiceRequestSuccess() {
        Map<String, Object> body = new HashMap<>();
        body.put("satisfaction_score", 5);

        given()
                .spec(SpecBuilder.getAuthenticatedRequestSpec(TestConfig.ADMIN_TOKEN))
                .body(body)
                .pathParam("id", "SR-2003")
        .when()
                .put("/api/service-requests/{id}/resolve")
        .then()
                .statusCode(200)
                .body("message", containsString("marked as Closed"));
    }

    @Test
    @DisplayName("TC-API-11: PUT /api/service-requests/:id/resolve - Boundary failure when CSAT > 5")
    public void testResolveServiceRequestInvalidBoundaryScore() {
        Map<String, Object> body = new HashMap<>();
        body.put("satisfaction_score", 9); // Boundary violation

        given()
                .spec(SpecBuilder.getAuthenticatedRequestSpec(TestConfig.ADMIN_TOKEN))
                .body(body)
                .pathParam("id", "SR-2005")
        .when()
                .put("/api/service-requests/{id}/resolve")
        .then()
                .statusCode(400)
                .body("error", equalTo("Bad Request"))
                .body("message", containsString("Satisfaction score must be between 1 and 5"));
    }
}
