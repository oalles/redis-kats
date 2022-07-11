package es.omarall.redis.kats;

import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.redis.lettucemod.api.StatefulRedisModulesConnection;
import com.redis.lettucemod.api.sync.RedisGearsCommands;
import com.redis.lettucemod.gears.Registration;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import javax.annotation.PostConstruct;
import java.util.Arrays;
import java.util.List;

@SpringBootApplication
@RestController
@Slf4j
public class KatsJavaClientApplication {

    public static void main(String[] args) {
        SpringApplication.run(KatsJavaClientApplication.class, args);
    }

    public KatsJavaClientApplication(final ObjectMapper om, final StatefulRedisModulesConnection<String, String> connection) {
        this.connection = connection;
        om.configure(JsonParser.Feature.ALLOW_SINGLE_QUOTES, true);
        this.om = om;
    }

    public static final String RG_GET_PREDICTIONS_TRIGGER = "GetValuesPerDayPredictions";

    private final StatefulRedisModulesConnection<String, String> connection;

    private final ObjectMapper om;

    @PostConstruct
    public void checkRGRegistrations() {

        RedisGearsCommands<String, String> gears = connection.sync();
        List<Registration> registrations = gears.dumpregistrations();

        if (registrations.isEmpty() ||
                registrations.stream().noneMatch(registration -> registration.getData().getArgs().get("trigger").equals(RG_GET_PREDICTIONS_TRIGGER))) {
            throw new IllegalStateException(String.format("RedisGears function %s NOT REGISTERED", RG_GET_PREDICTIONS_TRIGGER));
        }
    }

    @GetMapping(path = "/{daysCount}")
    public List<ValuePerDay> getPredictionsForNextDays(@PathVariable Integer daysCount) {

        try {
            RedisGearsCommands<String, String> gears = connection.sync();
            List<Object> results = gears.trigger(RG_GET_PREDICTIONS_TRIGGER, Integer.toString(daysCount));
            if (results.isEmpty()) {
                return Arrays.asList();
            }
            List<ValuePerDay> predictedValuesPerDay = om.readValue((String) results.get(0), new TypeReference<List<ValuePerDay>>() {
            });
            return predictedValuesPerDay;
        } catch (Throwable t) {
            log.error("", t);
            return Arrays.asList();
        }
    }
}

@Data
@AllArgsConstructor
@NoArgsConstructor
class ValuePerDay {
    private Long t;
    private Double v;
}
