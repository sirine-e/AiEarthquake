package fr.uha.ensisa;

import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.core.io.ByteArrayResource;

@RestController
public class MainController {
    private final String IA_SERVICE_URL = "http://ia:5000";
    private final RestTemplate restTemplate = new RestTemplate();

    @PostMapping("/config")
    public ResponseEntity<String> config(@RequestParam String model) {
        try {
            String url = IA_SERVICE_URL + "/config?model={model}";
            return restTemplate.postForEntity(url, null, String.class, model);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body("{\"error\":\"Configuration failed: " + e.getMessage() + "\"}");
        }
    }

    @PostMapping(value = "/classify", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<String> classify(@RequestParam("data") MultipartFile file) {
        try {
            String url = IA_SERVICE_URL + "/classify";
            
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.MULTIPART_FORM_DATA);
            
            MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
            ByteArrayResource fileAsResource = new ByteArrayResource(file.getBytes()) {
                @Override
                public String getFilename() {
                    return file.getOriginalFilename();
                }
            };
            body.add("data", fileAsResource);
            HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);
            
            return restTemplate.postForEntity(url, requestEntity, String.class);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body("{\"error\":\"Classification failed: " + e.getMessage() + "\"}");
        }
    }

    @PostMapping("/validate")
    public ResponseEntity<String> validate(@RequestParam(defaultValue = "0") int id) {
        try {
            String url = IA_SERVICE_URL + "/validate?id=" + id;
            return restTemplate.postForEntity(url, null, String.class);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body("{\"error\":\"Validation failed: " + e.getMessage() + "\"}");
        }
    }
}