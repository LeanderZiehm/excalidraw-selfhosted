package com.leanderziehm.excalidraw;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;


@Configuration
@Profile("dev")
public class DevSecurityConfiguration {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.authorizeHttpRequests(auth -> auth.anyRequest().permitAll());
        return http.build();
    }
}

// @Configuration
// @Profile("!dev")
// public class DevSecurityConfiguration {
//     @Bean
//     SecurityFilterChain httpSecurity(HttpSecurity http) throws Exception {
//         http.authorizeHttpRequests(auth -> auth.anyRequest().authenticated())
//           .formLogin(withDefaults())
//           .httpBasic(withDefaults());

//         return http.build();
//     }
// }