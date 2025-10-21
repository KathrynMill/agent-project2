package com.echocommand.cloud.controller;

import com.echocommand.cloud.dto.UserProfileDto;
import com.echocommand.cloud.service.UserService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

/**
 * 用户管理控制器
 */
@RestController
@RequestMapping("/api/users")
@Tag(name = "用户管理", description = "用户信息、设置管理相关接口")
public class UserController {
    
    @Autowired
    private UserService userService;
    
    @GetMapping("/profile")
    @Operation(summary = "获取用户信息", description = "获取当前用户的详细信息")
    public ResponseEntity<UserProfileDto> getProfile(Authentication authentication) {
        String username = authentication.getName();
        UserProfileDto profile = userService.getUserProfile(username);
        return ResponseEntity.ok(profile);
    }
    
    @PutMapping("/profile")
    @Operation(summary = "更新用户信息", description = "更新当前用户的基本信息")
    public ResponseEntity<UserProfileDto> updateProfile(
            @Valid @RequestBody UserProfileDto profileDto,
            Authentication authentication) {
        String username = authentication.getName();
        UserProfileDto updatedProfile = userService.updateUserProfile(username, profileDto);
        return ResponseEntity.ok(updatedProfile);
    }
    
    @GetMapping("/settings")
    @Operation(summary = "获取用户设置", description = "获取当前用户的所有设置")
    public ResponseEntity<?> getUserSettings(Authentication authentication) {
        String username = authentication.getName();
        return ResponseEntity.ok(userService.getUserSettings(username));
    }
    
    @PutMapping("/settings")
    @Operation(summary = "更新用户设置", description = "批量更新用户设置")
    public ResponseEntity<?> updateUserSettings(
            @RequestBody java.util.Map<String, Object> settings,
            Authentication authentication) {
        String username = authentication.getName();
        userService.updateUserSettings(username, settings);
        return ResponseEntity.ok().build();
    }
    
    @DeleteMapping("/account")
    @Operation(summary = "删除账户", description = "删除当前用户账户")
    public ResponseEntity<Void> deleteAccount(Authentication authentication) {
        String username = authentication.getName();
        userService.deleteUser(username);
        return ResponseEntity.ok().build();
    }
}



