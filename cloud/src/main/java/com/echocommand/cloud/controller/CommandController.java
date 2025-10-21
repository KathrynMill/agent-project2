package com.echocommand.cloud.controller;

import com.echocommand.cloud.dto.CustomCommandDto;
import com.echocommand.cloud.service.CommandService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

/**
 * 自定义命令控制器
 */
@RestController
@RequestMapping("/api/commands")
@Tag(name = "命令管理", description = "自定义命令创建、管理相关接口")
public class CommandController {
    
    @Autowired
    private CommandService commandService;
    
    @GetMapping
    @Operation(summary = "获取命令列表", description = "获取当前用户的自定义命令列表")
    public ResponseEntity<Page<CustomCommandDto>> getCommands(
            Authentication authentication,
            Pageable pageable) {
        String username = authentication.getName();
        Page<CustomCommandDto> commands = commandService.getUserCommands(username, pageable);
        return ResponseEntity.ok(commands);
    }
    
    @GetMapping("/public")
    @Operation(summary = "获取公共命令", description = "获取所有公开的自定义命令")
    public ResponseEntity<Page<CustomCommandDto>> getPublicCommands(Pageable pageable) {
        Page<CustomCommandDto> commands = commandService.getPublicCommands(pageable);
        return ResponseEntity.ok(commands);
    }
    
    @PostMapping
    @Operation(summary = "创建命令", description = "创建新的自定义命令")
    public ResponseEntity<CustomCommandDto> createCommand(
            @Valid @RequestBody CustomCommandDto commandDto,
            Authentication authentication) {
        String username = authentication.getName();
        CustomCommandDto createdCommand = commandService.createCommand(username, commandDto);
        return ResponseEntity.ok(createdCommand);
    }
    
    @GetMapping("/{id}")
    @Operation(summary = "获取命令详情", description = "获取指定命令的详细信息")
    public ResponseEntity<CustomCommandDto> getCommand(
            @PathVariable Long id,
            Authentication authentication) {
        String username = authentication.getName();
        CustomCommandDto command = commandService.getCommand(username, id);
        return ResponseEntity.ok(command);
    }
    
    @PutMapping("/{id}")
    @Operation(summary = "更新命令", description = "更新指定的自定义命令")
    public ResponseEntity<CustomCommandDto> updateCommand(
            @PathVariable Long id,
            @Valid @RequestBody CustomCommandDto commandDto,
            Authentication authentication) {
        String username = authentication.getName();
        CustomCommandDto updatedCommand = commandService.updateCommand(username, id, commandDto);
        return ResponseEntity.ok(updatedCommand);
    }
    
    @DeleteMapping("/{id}")
    @Operation(summary = "删除命令", description = "删除指定的自定义命令")
    public ResponseEntity<Void> deleteCommand(
            @PathVariable Long id,
            Authentication authentication) {
        String username = authentication.getName();
        commandService.deleteCommand(username, id);
        return ResponseEntity.ok().build();
    }
    
    @PostMapping("/{id}/use")
    @Operation(summary = "使用命令", description = "记录命令使用次数")
    public ResponseEntity<Void> useCommand(
            @PathVariable Long id,
            Authentication authentication) {
        String username = authentication.getName();
        commandService.useCommand(username, id);
        return ResponseEntity.ok().build();
    }
}



