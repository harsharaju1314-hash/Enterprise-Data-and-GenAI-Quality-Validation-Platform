package com.enterprise.quality.api.models;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;

@JsonIgnoreProperties(ignoreUnknown = true)
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ServiceRequest {
    private String request_id;
    private String customer_id;
    private String category;
    private String priority;
    private String created_date;
    private String resolved_date;
    private String status;
    private Double resolution_time_hours;
    private Double satisfaction_score;
    private String description;

    public ServiceRequest() {}

    public ServiceRequest(String request_id, String customer_id, String category, String priority, String description) {
        this.request_id = request_id;
        this.customer_id = customer_id;
        this.category = category;
        this.priority = priority;
        this.description = description;
    }

    public String getRequest_id() { return request_id; }
    public void setRequest_id(String request_id) { this.request_id = request_id; }
    public String getCustomer_id() { return customer_id; }
    public void setCustomer_id(String customer_id) { this.customer_id = customer_id; }
    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }
    public String getPriority() { return priority; }
    public void setPriority(String priority) { this.priority = priority; }
    public String getCreated_date() { return created_date; }
    public void setCreated_date(String created_date) { this.created_date = created_date; }
    public String getResolved_date() { return resolved_date; }
    public void setResolved_date(String resolved_date) { this.resolved_date = resolved_date; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public Double getResolution_time_hours() { return resolution_time_hours; }
    public void setResolution_time_hours(Double resolution_time_hours) { this.resolution_time_hours = resolution_time_hours; }
    public Double getSatisfaction_score() { return satisfaction_score; }
    public void setSatisfaction_score(Double satisfaction_score) { this.satisfaction_score = satisfaction_score; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
}
