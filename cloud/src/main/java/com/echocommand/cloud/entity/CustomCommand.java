package com.echocommand.cloud.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;

/**
 * 自定义命令实体
 */
@Entity
@Table(name = "custom_commands")
public class CustomCommand {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;
    
    @NotBlank
    @Size(max = 100)
    private String name;
    
    @Size(max = 500)
    private String description;
    
    @NotBlank
    @Column(columnDefinition = "TEXT")
    private String triggerPhrase;
    
    @NotBlank
    @Column(columnDefinition = "TEXT")
    private String commandScript;
    
    @Enumerated(EnumType.STRING)
    private CommandType commandType = CommandType.SYSTEM_CONTROL;
    
    @Enumerated(EnumType.STRING)
    private CommandStatus status = CommandStatus.ACTIVE;
    
    private Boolean isPublic = false;
    
    private Integer usageCount = 0;
    
    @CreationTimestamp
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    private LocalDateTime updatedAt;
    
    // 构造函数
    public CustomCommand() {}
    
    public CustomCommand(User user, String name, String triggerPhrase, String commandScript) {
        this.user = user;
        this.name = name;
        this.triggerPhrase = triggerPhrase;
        this.commandScript = commandScript;
    }
    
    // Getters and Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public User getUser() {
        return user;
    }
    
    public void setUser(User user) {
        this.user = user;
    }
    
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        this.name = name;
    }
    
    public String getDescription() {
        return description;
    }
    
    public void setDescription(String description) {
        this.description = description;
    }
    
    public String getTriggerPhrase() {
        return triggerPhrase;
    }
    
    public void setTriggerPhrase(String triggerPhrase) {
        this.triggerPhrase = triggerPhrase;
    }
    
    public String getCommandScript() {
        return commandScript;
    }
    
    public void setCommandScript(String commandScript) {
        this.commandScript = commandScript;
    }
    
    public CommandType getCommandType() {
        return commandType;
    }
    
    public void setCommandType(CommandType commandType) {
        this.commandType = commandType;
    }
    
    public CommandStatus getStatus() {
        return status;
    }
    
    public void setStatus(CommandStatus status) {
        this.status = status;
    }
    
    public Boolean getIsPublic() {
        return isPublic;
    }
    
    public void setIsPublic(Boolean isPublic) {
        this.isPublic = isPublic;
    }
    
    public Integer getUsageCount() {
        return usageCount;
    }
    
    public void setUsageCount(Integer usageCount) {
        this.usageCount = usageCount;
    }
    
    public LocalDateTime getCreatedAt() {
        return createdAt;
    }
    
    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
    
    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }
    
    public void setUpdatedAt(LocalDateTime updatedAt) {
        this.updatedAt = updatedAt;
    }
    
    public enum CommandType {
        SYSTEM_CONTROL, FILE_OPERATION, TEXT_PROCESSING, 
        APPLICATION, MEDIA, QUERY, CUSTOM
    }
    
    public enum CommandStatus {
        ACTIVE, INACTIVE, DEPRECATED
    }
}



