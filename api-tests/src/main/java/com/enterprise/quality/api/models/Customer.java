package com.enterprise.quality.api.models;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;

@JsonIgnoreProperties(ignoreUnknown = true)
@JsonInclude(JsonInclude.Include.NON_NULL)
public class Customer {
    private String customer_id;
    private String first_name;
    private String last_name;
    private String full_name;
    private String email;
    private String tier;
    private String region;
    private String account_created_date;
    private String status;

    public Customer() {}

    public Customer(String customer_id, String first_name, String last_name, String email, String tier, String region, String status) {
        this.customer_id = customer_id;
        this.first_name = first_name;
        this.last_name = last_name;
        this.email = email;
        this.tier = tier;
        this.region = region;
        this.status = status;
    }

    public String getCustomer_id() { return customer_id; }
    public void setCustomer_id(String customer_id) { this.customer_id = customer_id; }
    public String getFirst_name() { return first_name; }
    public void setFirst_name(String first_name) { this.first_name = first_name; }
    public String getLast_name() { return last_name; }
    public void setLast_name(String last_name) { this.last_name = last_name; }
    public String getFull_name() { return full_name; }
    public void setFull_name(String full_name) { this.full_name = full_name; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public String getTier() { return tier; }
    public void setTier(String tier) { this.tier = tier; }
    public String getRegion() { return region; }
    public void setRegion(String region) { this.region = region; }
    public String getAccount_created_date() { return account_created_date; }
    public void setAccount_created_date(String account_created_date) { this.account_created_date = account_created_date; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
}
