package com.softsafe.sast.platform.config.security;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.softsafe.sast.platform.config.OAuthUserExtractor;
import com.softsafe.sast.platform.dto.AuthUserReqDTO;
import com.softsafe.sast.platform.entity.UserInfo;
import com.softsafe.sast.platform.service.TokenService;
import com.softsafe.sast.platform.service.UserService;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.security.oauth2.client.*;
import org.springframework.security.oauth2.client.authentication.OAuth2AuthenticationToken;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.util.Map;

@Component
@RequiredArgsConstructor
public class OAuth2LoginSuccessHandler implements org.springframework.security.web.authentication.AuthenticationSuccessHandler {

    private final TokenService tokenService;
    private final OAuth2AuthorizedClientService authorizedClientService;
    private final ObjectMapper objectMapper;
    private final UserService userService;
    private final OAuthUserExtractor oAuthUserExtractor;

    private final long ACCESS_TOKEN_SECONDS = 60 * 30; // 30min
    private final long REFRESH_TOKEN_SECONDS = 60 * 60 * 24 * 7; // 7d

    @Override
    public void onAuthenticationSuccess(HttpServletRequest request, HttpServletResponse response, Authentication authentication) throws IOException, ServletException {
        OAuth2AuthenticationToken oauthToken = (OAuth2AuthenticationToken) authentication;

        // application user id
        AuthUserReqDTO authUserReqDTO = oAuthUserExtractor.extract(oauthToken.getPrincipal(), oauthToken);
        UserInfo userInfo = userService.getUserInfoByOauthUserIdAndSourceType(
                authUserReqDTO.getId(),
                authUserReqDTO.getProvider()
        );
        if (userInfo == null){
            userInfo = UserInfo.builder()
                    .oauthType(authUserReqDTO.getProvider())
                    .oauthUserId(authUserReqDTO.getId())
                    .oauthUserName(authUserReqDTO.getUsername())
                    .build();
            userService.save(userInfo);
        }

        // optionally save third-party access token for backend usage (not returned to frontend)
        OAuth2AuthorizedClient client = authorizedClientService.loadAuthorizedClient(oauthToken.getAuthorizedClientRegistrationId(), oauthToken.getName());
        if (client != null && client.getAccessToken() != null) {
            String externalToken = client.getAccessToken().getTokenValue();
            // TODO save to secure storage if needed
        }
        try {
            String accessJwt = tokenService.createAccessToken(userInfo.getId().toString(), ACCESS_TOKEN_SECONDS);
            String refreshJwt = tokenService.createRefreshToken(userInfo.getId().toString(), REFRESH_TOKEN_SECONDS);
            Cookie refreshTokenCookie = new Cookie("refreshToken", refreshJwt);
            refreshTokenCookie.setHttpOnly(true);
            refreshTokenCookie.setSecure(true);
            refreshTokenCookie.setPath("/");
            //TODO 配置文件
            refreshTokenCookie.setDomain("lekker-hypertragically-jadwiga.ngrok-free.dev");
            refreshTokenCookie.setMaxAge((int) REFRESH_TOKEN_SECONDS);
            response.addCookie(refreshTokenCookie);

            response.setContentType("application/json;charset=UTF-8");
            objectMapper.writeValue(response.getWriter(), Map.of(
                    "accessToken", accessJwt,
                    "expiresIn", ACCESS_TOKEN_SECONDS,
                    "userId", userInfo.getId().toString()
            ));
        } catch (Exception e) {
            throw new ServletException(e);
        }
    }
}
