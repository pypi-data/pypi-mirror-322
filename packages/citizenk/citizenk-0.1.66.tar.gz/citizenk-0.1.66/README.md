# CitizenK
**CitizenK** is a simple but powerful Python Library for developing reactive async Kafka microservices, built on top of [Confluent Kafka Python](https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html), [FastAPI](https://fastapi.tiangolo.com/) and [Pydantic](https://docs.pydantic.dev/).

**CitizenK Replicator** is an additional tool that we developed using the same technology to simplify data transfer between production and staging environments. It's not a substitution for Confluent's replicator which is a much more robust tool for replicating data between multiple production environments

------------------------------------------------------------------------
------------------------------------------------------------------------

## How we got here...
We exclusively use Python for service development. Our work involves crafting web services, creating ETL code, and engaging in data science, all within the Python ecosystem. A few years back, as we embarked on the Lanternn project, our quest led us to seek a Python library that could facilitate the construction of distributed, scalable processing pipelines built on top of Kafka. These pipelines needed to accommodate both stateless and stateful microservices seamlessly. After extensive exploration, we found that the most suitable solution at the time was Faust.

Faust is a stream processing library that borrows concepts from Kafka Streams and brings them into the Python realm. Beyond this, Faust boasts an impressive array of features, including a robust web server, comprehensive schema validation and management, all built upon an agents/actors architecture. With such a compelling set of attributes, it was impossible for us to resist its allure.

We went on to develop numerous services utilizing Faust, and by and large, we were quite content with the results. However, as time progressed, we came to realize that Kafka Streams was not the ideal fit for our needs. Its complexity made it challenging to manage, and we found simpler alternatives for state management, such as Redis, to be more suitable. Additionally, concerns began to emerge about the long-term viability of Faust, particularly in the absence of its creator Ask Solem. Moreover, the underlying Kafka libraries it relied upon, aiokafka and python-kafka, lacked the robust community support necessary to address the stability issues we encountered.

Concurrently, we observed that frameworks like FastAPI and Confluent Kafka, which we were already using, enjoyed strong backing from vibrant and sizable communities. This realization led us to explore the possibility of combining these frameworks to establish a new foundation for our pipelines, one that would offer greater stability and long-term viability, and would be easy to migrate to from Faust.

The choice of the name "CitizenK" embodies our belief that Python should occupy a prominent position within the Kafka ecosystem. It also draws inspiration from Kafka's renowned novel, "The Trial," which chronicles the plight of Josef K., a man ensnared and prosecuted by an enigmatic, distant authority. The nature of his alleged transgression remains shrouded in mystery, a narrative that resonates with our journey in the world of Kafka.


## Existing tools
- Faust
- Fastkafka

------------------------------------------------------------------------

## Tutorial

You can see an example of how to use CitizenK in the demo app

### Creating a CitizenK app

First, we create a CitizenK app similar to how we create a FastAPI app, but with additional arguments:

- kafka_config: provides configuration for connecting and configuring the Kafka client
- app_name: Mainly used as the consumer group name
- app_type: SINK (consumer only), SOURCE(producer only) or TRANSFORM(producer-consumer)
- auto_generate_apis: Will auto generate FastAPI to consume and produce to workers and topics
- agents_in_thread: Will run the consumer agents in a thread and not in an async loop
- consumer_group_init_offset: Where to start consuming when the consumer group is created
- consumer_group_auto_commit: commit after consume / commit after processing completed successfully in all agents
- exit_on_agent_exception: exit the service if there is exception in an agent

``` python
app = CitizenK(
    kafka_config=config.source_kafka,
    app_name="citizenk",
    app_type=AppType.TRANSFORM,
    debug=True,
    title="CitizenK Demo App",
    auto_generate_apis=True,
    agents_in_thread=config.AGENTS_IN_THREAD,
    api_router_prefix=prefix,
    api_port=config.API_PORT,
    schema_registry_url=config.KAFKA_SCHEMA_REGISTRY,
    version=config.VERSION,
    consumer_group_init_offset = "latest",
    consumer_group_auto_commit = True,
    consumer_extra_config=config.KAFKA_CONSUMER_EXTRA_CONFIG,
    producer_extra_config=config.KAFKA_PRODUCER_EXTRA_CONFIG,
    exit_on_agent_exception=True,
    openapi_url=prefix + "/openapi.json",
    docs_url=prefix + "/docs",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)
```

### Creating CitizenK topics
Next, we create topics for the app and define the model for the topics using Pydantic

Topics can be either INPUT, OUTPUT or BIDIR

``` python
class Video(JSONSchema):
    camera_id: int
    path: str
    timestamp: datetime


class ProcessedVideo(JSONSchema):
    camera_id: int
    path: str
    timestamp: datetime
    valid: bool


t1 = app.topic(name="B", value_type=Video, topic_dir=TopicDir.BIDIR)
t2 = app.topic(name="C", value_type=ProcessedVideo, topic_dir=TopicDir.BIDIR)
t3 = app.topic(name="D", value_type=ProcessedVideo, topic_dir=TopicDir.OUTPUT)
```

Schemas can also be AVRO

``` python
class AvroProcessedVideo(AvroBase):
    camera_id: int
    path: str
    timestamp: datetime
    valid: bool

t4 = app.topic(
    name="E",
    value_type=AvroProcessedVideo,
    topic_dir=TopicDir.BIDIR,
    schema_type=SchemaType.AVRO,
)
```

In case the schema is unknown or not managed, Pydantic offers an option to allow extra non managed fields:

``` python
class AnythingModel(BaseModel):
  class Config:
    extra = Extra.allow
```

### Creating CitizenK agents
And lastly, we create gents that process the Kafka messages.

Agents can listen to multiple topics and accept either values or the entire Kafka event (key, value, offset, partition, timestamp...). Agents can also accept a self argument to get a reference to the Agent object.

In non auto commit apps, offsets are committed only after all agents processed the event successfully.

- topics: one or more topics to process
- batch_size: specify desired batch_size. Default = 1
- batch_timeout: How long to wait for batch to arrive: Default = 10 seconds

``` python
@app.agent(topics=t1, batch_size=100)
async def process_videos_t1(events: list[KafkaEvent]):
    # Process incoming video
    for event in events:
        camera_id = event.value.camera_id
        video_counts[camera_id] += 1
        v = ProcessedVideo(
            camera_id=camera_id,
            path=event.value.path,
            timestamp=event.value.timestamp,
            valid=bool(camera_id % 2),
        )
        t2.send(value=v, key=str(v.camera_id))


@app.agent(topics=t2, batch_size=100)
async def process_videos_t2(values: list[BaseModel]):
    # Process incoming video
    for value in values:
        if value.valid:
            t3.send(value=value, key=str(value.camera_id))

```

### Auto endpoints
To help debug and evaluate the service, CitizenK automatically creates web endpoints that help you send messages to topics and agents.

- info: get service info
- topics: send events to topics
- agents: send events directly to agents, bypassing topics
- stats: get Kafka stats for producer and consumer

![CitizenK Demo API](docs/citizenk_demo_api.jpg)


### Creating additional CitizenK endpoints
Just like any other FastAPI app, you can create get, post and put endpoints that either interact with Kafka or perform some other tasks, non Kafka related

``` python
@router.post("/events", response_class=JSONResponse)
async def produce_video_events(
    values: list[Video],
    topic: str = Query(),
):
    """Sends events to the given topic"""
    if topic not in app.topics:
        raise HTTPException(status_code=400, detail="Topic not supported by app")
    t = app.topics[topic]
    for v in values:
        t.send(value=v, key=str(v.camera_id))
    return {"status": "ok"}


@router.get("/topics", response_class=JSONResponse)
async def get_source_topics():
    """Returns the list of topics from the source kafka"""
    admin = KafkaAdapter(config.source_kafka)
    topics = sorted(list(admin.get_all_broker_topics().keys()))
    return {"topics": topics}
```

### Multiple workers behind a load balancer
CitizenK includes two special decorators for scenarios where the service has multiple workers behind a load balancer and the web request needs to reach a specific worker that holds a partition.

- topic_router: forwards the request based on the topic and key (JSON / HTML)
- broadcast_router: aggregates the responses from all workers into a single JSON

Both routers support GET, POST, PUT and DELETE commands

``` python
@router.get("/topic_test", response_class=JSONResponse)
@app.topic_router(topic=t1, match_info="camera_id")
async def test_topic_router(request: Request, camera_id: int):
    """Returns the list of groups from the target kafka"""
    return {"key": camera_id, "count": video_counts[camera_id]}


@router.get("/broadcast_test", response_class=JSONResponse)
@app.broadcast_router()
async def test_broadcast_router(request: Request):
    """Returns the list of groups from the target kafka"""
    return video_counts
```

### Websocket
CitizenK support for Websocket agents

``` python
@app.agent(topics=t2, batch_size=100, websocket_route=prefix + "/ws")
async def websocket_agent(values: list[BaseModel]) -> str:
    values = [json.loads(v.model_dump_json()) for v in values if not v.valid]
    return json.dumps(values, indent=4)
```

This agent exposes a WebSocket endpoint for one or more clients to connect to. It then processes incoming Kafka messages from topic t2 and sends the returned string value to all the existing live WebSocket "/ws" connections. The main use case for this is to bridge between Kafka and Websocket. One possible use case for this feature is to send filtered Kafka events to a web app or mobile app.


The other direction frontend --> Kafka is probably easier to implement with a normal REST post endpoint and is not supported yet.

### Event handlers tasks and repeat / cron tasks
To start tasks in certain condition, just like FastAPI on_event("startup") / on_event("shutdown"), CitizenK includes similar mechanism:

on_citizenk_event("startup")
on_citizenk_event("shutdown")
on_citizenk_event("agent_thread_startup")

agent_thread_startup can be used to run tasks in the agents thread, while normal startup runs them in the web thread.

``` python
@app.on_citizenk_event("agent_thread_startup")
async def startup_debug():
    logger.debug("Demo App starting")
```

CitizenK also includes repeatable tasks:

``` python
def repeat_every(
    *,
    seconds: float,
    wait_first: bool = False,
    logger: logging.Logger | None = None,
    raise_exceptions: bool = False,
    max_repetitions: int | None = None,
) -> Callable:

def repeat_at(
    *,
    cron: str,
    logger: logging.Logger = None,
    raise_exceptions: bool = False,
    max_repetitions: int = None,
) -> Callable:
```

that normally works with event handlers like this:
``` python
@app.on_citizenk_event("agent_thread_startup")
@repeat_every(seconds=5)
async def agent_thread_debug():
    logger.debug("In agent thread... thread=%s",threading.get_ident())
```

## Things to be aware of...
CitizenK is a single-threaded async app. i.e. If a coroutine spends too much time in processing without awaiting IO, it will block other coroutines from running. Specifically, when using a load balancer with health checks, it's important to pay attention to the time between health checks and see that it's higher than the longest-running agent. Fixed using:agents_in_thread


To help tune the service. CitizenK includes the concept of batch size:i.e. how many events to consume and process every batch across all agents.

Additionally like any other Kafka service. it's important to tune several kafka [consumer](https://docs.confluent.io/platform/current/installation/configuration/consumer-configs.html#fetch-max-bytes) and [producer](https://docs.confluent.io/platform/current/installation/configuration/producer-configs.html) configs. Specifically ensure rebalancing is not triggered unintentionally: Alternatively this list includes [all Kafka configs](https://github.com/confluentinc/librdkafka/blob/master/CONFIGURATION.md)

Consumer:
- fetch.max.bytes (50 Mbytes): The maximum amount of data the server should return for a fetch request. Reduce if processing each record takes significant time.
- max.poll.records(500): The maximum number of records returned in a single call to poll().
- max.poll.interval.ms (5 min): The maximum delay between invocations of poll() when using consumer group management

Group rebalancing in stateful services:
- Prefer static membership + Increase session.timeout.ms to 2-5 minutes (how long it takes a new service to come up)
- partition.assignment.strategy': 'range'

Producer:
- linger.ms(0): Important to set to 0/5/10/50/200 on moderate/high load
- batch.size(16K): Increase if sending large buffers to Kafka

Both:
- compression.type(none): gzip, snappy, or lz4

More explanation in here: [Solving My Weird Kafka Rebalancing Problems & Explaining What Is Happening and Why?](https://medium.com/bakdata/solving-my-weird-kafka-rebalancing-problems-c05e99535435)


## CitizenK vs Faust

| Topic | CitizenK | Faust |
| ------ |------- | ----- |
| Creating an app | app = Citizenk() | app = faust.App() |
| Creating a topic | topic = app.topic() | topic = app.topic() |
| Creating an agent | @app.agent() | @app.agent() |
| Creating a table | not supported | app.Table() |
| Creating a timer | @repeat_every | @app.timer() |
| Creating a task | background_tasks.add_task() | @app.task() |
| Creating a page | @app.get() | @app.page() |
| Routing requests | @app.topic_router | @app.topic_route |
| Broadcast requests | @app.broadcast_router() | Not supported |
| Models | Pydantic | faust.Record |
| Model to dict | to_representation() | model_dump_json() |
| Serializers | JSON, AVRO | JSON, RAW, PICKLE, AVRO |
| Kafka library | confluent | aiokafka |
| Websockets agents | Supported | Not supported |

------------------------------------------------------------------------


# CitizenK Replicator
## Scenarios

### Staging environment
1. I have a staging environment and I want to replicate some production topics to it

2. At some point I want to produce the staging topics in the staging environment using a staging service. So I switch off the replication and populate the same staging topic with real data.

3. When I finish the testing in staging, I want to switch back to production, so that I can save on costs.

4. If the workload is high, I want to replicate most (i.e. 90%) of the messages from production and only produce just a little (i.e. 10%) of the data from staging. This way in the same topic, I will have mixed data and potential schema from the two environments

5. When switching between environments (i.e. on configuration change), I want to change the offset to the latest on the new topic, so that the handover is not too chaotic

6. I also want to delete the consumer group of the service in staging, so that when it come back up again, it won't see a lag.

7. Additionally sometimes, I want to migrate data between production and staging due to schema change or different identities.

![Replicator](docs/replicator.jpg)

### Dev environment + live data
1. When I test a service locally or in a dev environment, possibly with a local Kafka, I want the local Kafka to have real data, so that I can test the service for a long period of time with live data.

2. Theoretically, I can connect the dev service to the staging or production Kafka cluster, however, this presents a stability/security risk to the remote cluster. There is also a risk that the service will join a consumer group and participate accidentally in the remote workload. This approach also prevents parallel testing as there can be a conflict between the consumers.

3. So one solution would be to replicate the topics from staging to the local/dev Kafka, maybe with some filtering to reduce the load, so that the local service is not overwhelmed with too much data

### On premise kafka -- cloud kafka bridge
1. I have a local Kafka and I want to replicate some topics to the remote cloud

2. You can use this tool for this scenario, however Confluent replicator or Kafka MirrorMaker are probably more suitable

### Dev environment + replayed data
1. When I test a service locally or in a dev environment, possibly with a local Kafka, I want the local Kafka to replay historical/simulated messages from a file.

2. this scenario is a bit different from the previous ones, as there is no Kafka consumer, just a producer. And you can say that it is more of a tool than a service.

3. The messages are read from a file with a timestamp (one file for each topic), and injected into the right topic with the correct timing keeping the same gap between now, and the initial timestamp.


### Cluster -- Cluster replication
1. You can use this tool for this scenario, however Confluent replicator or Kafka MirrorMaker are probably more suitable

## Existing tools
1. Confluent replicator: Looks like a good tool, but not open source, expensive
2. Kafka Mirror Maker: Open source but doesn't support filtering
3. kcat: Nice tool, but not for these scenarios


## Implementation details
1. Using containerised python
2. Based on Confluent Kafka API + FastAP
3. Does not create the topics or partitions automatically. It assumes they exists and configured
3. Deployed as a distributed service
4. Filter based on JMESPath for JSON messages
5. Allow two consumer options: with consumer group, without consumer group
6. write code following DDD principles

## Configuration
- LOG_LEVEL: service log level
- JSON_LOGGING: Use json logging
- API_PREFIX: API prefix
- FILE_DATA_PATH: Location of json files when reading and writing topics from file
- KAFKA_SOURCE_SERVER_URL: Source Bootstrap Servers
- KAFKA_SOURCE_USE_TLS: Enable Source SSL: 0,1
- KAFKA_SOURCE_SASL_MECHANISM: Source SASL mechanism: PLAIN, SCRAM-SHA-256, SCRAM-SHA-512
- KAFKA_SOURCE_SASL_USERNAME: Source SASL username
- KAFKA_SOURCE_SASL_PASSWORD: Source SASL password
- KAFKA_SOURCE_GROUP_NAME: Source group name, or leave empty to consume without a consumer group
- KAFKA_SOURCE_EXTRA_CONFIG_<KAFKA_CONFIG_KEY>: Any valid kafka consumer config (uppercase, replace . with _)
- KAFKA_TARGET_SERVER_URL: Target Bootstrap Servers
- KAFKA_TARGET_USE_TLS: Enable Target SSL
- KAFKA_TARGET_SASL_MECHANISM: Target SASL mechanism: PLAIN, SCRAM-SHA-256, SCRAM-SHA-512
- KAFKA_TARGET_SASL_USERNAME: Target SASL username
- KAFKA_TARGET_SASL_PASSWORD: Target SASL password
- KAFKA_TARGET_EXTRA_CONFIG_<KAFKA_CONFIG_KEY>: Any valid kafka producer config (uppercase, replace . with _)
- READ_MAPPINGS_EVERY_SECONDS: How often to check for new mappings in the file system
- CACULATE_STATS_EVERY_SECONDS: How often to calculate stats
- DELETE_GROUPS_EVERY_SECONDS: How often to check for new group deletion

## Current solution limitations
1. Currently only supports JSON schema.

## API
[API Description](docs/replicator_openapi.md)

![Replicator API](docs/replicator_api.jpg)

## User Interface
![Replicator User Interface](docs/replicator_ui.jpg)

The user interface allows you to add a new mapping and edit/delete an existing mapping.

## Usage
Provide a JSON list of topic mappings in this format, either directly, or through templates:
```json
[
    {
        "group": "first",
        "name": "File A to B",
        "source_topic_name": "A",
        "target_topic_name": "{{B}}",
        "source_is_file": true
    },
    {
        "group": "first",
        "name": "Topic B to C",
        "source_topic_name": "{{B}}",
        "target_topic_name": "{{C}}"
    },
    {
        "group": "second",
        "name": "Topic C to D Using filter",
        "source_topic_name": "{{C}}",
        "target_topic_name": "D",
        "valid_jmespath": "key == 'hello' && value.msg == 'world'",
        "enabled": true
    },
    {
        "group": "second",
        "name": "TopicCtoD",
        "topics": [{
            "source":"{{C}}",
            "target": "D"
        }],
        "enabled": true,
        "target_service_consumer_group": "service"
    },
    {
        "group": "second",
        "name": "Topic D to File E",
        "source_topic_name": "D",
        "target_topic_name": "E",
        "target_is_file": true
    }
]
```
- name: A unique mapping name
- group: groups multiple mapping in the same category
- enabled: Enable / disable mapping
- source_topic_name: The topic to read from in the source cluster
- target_topic_name: The topic to write to in the target cluster
- valid_jmespath: filter criteria
- source_is_file: If the source is a json file
- target_is_file: If the target is a json file
- topics: an extension that allows one mapping with several source-target mappings
- target_service_consumer_group: The service consumer group to delete when replication is enabled

The final mapping file is defined this way:
```json
{
    "templates":[
        {
            "template":"name",
            "vars":{
                "A":"A",
                "B":"B",
                "C":"C"
            }
        }
    ],
    "enabled":[],
    "disabled":["TopicCtoD"],
    "mappings":[{
            "group": "third",
            "name": "Disabled Topic U to File V",
            "source_topic_name": "U",
            "target_topic_name": "V",
            "target_is_file": true,
            "enabled": false
    }],
    "comment": "no comment"
}
```

- templates: A list of templates and their corresponding vars to render the template
- enabled / disabled: Overrides the template enabled flag
- mappings: Extra mappings
- comment: A comment that describes the latest change in the mappings

## Topic Level Mapping
Topic level mappings allows mapping of key/values when replicating a topic. This might be useful if for example the schema / enums / keys are different between the environments

To support this, the replicator supports value mappings for each topic that it consumes from the source in the following JSON format:

There are two mapping formats:
- value.payload.product_id : map source product_id to target product_id
- key:partition: map source key to target partition (drop entire msg if partition equals -1000)

```json
{
    "key":{
        "1":10,
        "2":12
    },
    "value.payload.product_id":{
        "1001":1,
        "1002":12,
        "1003":14
    },
    "value.payload.user_name":{
        "A":"A name",
        "B":"B name",
        "C":"C name"
    },
    "key:partition":{
        "1":0,
        "2":0,
        "3":-1000,
        "4":1,
        "5":1,
        "6":1,
    }
}
```

## Stats
Returns a list of JSON stats for each mapping in the following format:
```json
{
    "time": "2023-05-25 18:20:43.875557",
    "started": "2023-05-25 08:08:35.728313",
    "queue": 180,
    "mappings": [
        {
            "name": "Topic B to C",
            "source_topic_name": "B",
            "target_topic_name": "C",
            "valid_jmespath": null,
            "target_service_consumer_group": null,
            "consumer_group_up": false,
            "assignments": [0,1,2],
            "lag": 1258,
            "source_count": 27739,
            "target_count": 27739
        }
    ]
}
```

## Grafana Integration
To view the stats in Grafana, use the Infinity data source with the following settings:

![Replicator Grafana Interface](docs/replicator_grafana.jpg)

## Consumer API
To simplify debug and to support other use cases, the replicator also includes an end point to consume messages from a given topic.


## License
[Apache License v2.0](https://www.apache.org/licenses/LICENSE-2.0)
