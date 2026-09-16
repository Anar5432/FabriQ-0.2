package com.company.erp.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class WebDashboardController {

    @GetMapping("/")
    public String home() {
        return "forward:/index.html";
    }
}
