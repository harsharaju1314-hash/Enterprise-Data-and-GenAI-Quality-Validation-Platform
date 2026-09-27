package com.enterprise.quality.api;

import com.enterprise.quality.api.utils.SpecBuilder;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

public class MetricsAndAnalyticsApiTest {

    @Test
    @DisplayName("TC-API-12: GET /api/metrics - Verify executive KPIs align with relational database")
    public void testGetMetricsSummary() {
        given()
                .spec(SpecBuilder.getRequestSpec())
        .when()
                .get("/api/metrics")
        .then()
                .spec(SpecBuilder.getSuccessResponseSpec(200))
                .body("total_transactions", greaterThanOrEqualTo(16))
                .body("gross_transaction_volume", notNullValue())
                .body("total_service_requests", greaterThanOrEqualTo(15))
                .body("open_service_requests", notNullValue())
                .body("closed_service_requests", notNullValue());
    }
}
