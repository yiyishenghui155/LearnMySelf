package com.softsafe.sast.platform.config.security;

import com.softsafe.sast.platform.config.RestAccessDeniedHandler;
import com.softsafe.sast.platform.config.RestAuthenticationEntryPoint;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.annotation.Order;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
@RequiredArgsConstructor
public class SecurityConfig {
    private final RestAuthenticationEntryPoint restAuthEntryPoint;
    private final RestAccessDeniedHandler restAccessDeniedHandler;
    private final OAuth2LoginSuccessHandler oauth2LoginSuccessHandler;

    @Bean
    @Order(2)
    public SecurityFilterChain applicationSecurity(HttpSecurity http) throws Exception {

        http.exceptionHandling(ex -> ex
                        .authenticationEntryPoint(restAuthEntryPoint)
                        .accessDeniedHandler(restAccessDeniedHandler)
                )
                .authorizeHttpRequests(authorize -> authorize
                        .requestMatchers(
                                "/", "/login", "/login.html",
                                "/error",
                                "/github/webhook",
                                "/api/sast/**",
                                "/favicon.ico", "/icons/**"
                        ).permitAll()
                        .anyRequest().authenticated()
                )
                .oauth2Login(oauth2 -> oauth2
                        .successHandler(oauth2LoginSuccessHandler)
                        .failureUrl("/login?error")
                )
                .csrf(csrf -> csrf
                        .ignoringRequestMatchers("/github/webhook", "/api/sast/**")
                );

        return http.build();
    }
}
