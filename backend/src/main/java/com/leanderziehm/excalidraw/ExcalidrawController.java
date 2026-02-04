package com.leanderziehm.excalidraw;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.GetMapping;

@RestController
public class ExcalidrawController {
    
    @GetMapping("/")
    public String getMethodName() {
        return "hello :) v0.0.1";
    }
    
}
