package com.enterprise.quality.api.utils;

import com.enterprise.quality.api.config.TestConfig;
import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import io.restassured.response.Response;

import java.util.HashMap;
import java.util.Map;

public class AuthHelper {

    public static String loginAndGetToken(String username, String password) {
        Map<String, String> credentials = new HashMap<>();
        credentials.put("username", username);
        credentials.put("password", password);

        Response response = RestAssured.given()
                .baseUri(TestConfig.BASE_URL)
                .contentType(ContentType.JSON)
                .body(credentials)
                .when()
                .post("/api/auth/login")
                .then()
                .extract().response();

        if (response.getStatusCode() == 200) {
            return response.jsonPath().getString("token");
        }
        return null;
    }
}
