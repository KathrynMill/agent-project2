package com.echocommand.cloud;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.kafka.annotation.EnableKafka;

/**
 * Echo Command 云端服务主应用
 */
@SpringBootApplication
@EnableKafka
public class EchoCommandCloudApplication {

    public static void main(String[] args) {
        SpringApplication.run(EchoCommandCloudApplication.class, args);
    }
}

