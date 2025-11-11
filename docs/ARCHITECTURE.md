# PyMLB StatsAPI Architecture

## Schema-Driven Design

```mermaid
graph TB
    subgraph "JSON Schemas"
        S1[schedule.json]
        S2[game.json]
        S3[person.json]
        S4[team.json]
        S5[stats.json]
        S6[...]
    end

    subgraph "Schema Loader"
        SL[SchemaLoader]
        SL -->|loads| S1
        SL -->|loads| S2
        SL -->|loads| S3
        SL -->|loads| S4
        SL -->|loads| S5
        SL -->|loads| S6
    end

    subgraph "Registry & Factory"
        REG[StatsAPI Registry]
        SL -->|provides schemas| REG

        REG -->|creates| E1[Schedule Endpoint]
        REG -->|creates| E2[Game Endpoint]
        REG -->|creates| E3[Person Endpoint]
        REG -->|creates| E4[Team Endpoint]
        REG -->|creates| E5[Stats Endpoint]

        E1 -->|generates| M1[schedule method]
        E2 -->|generates| M2[boxscore method]
        E2 -->|generates| M3[liveGameV1 method]
        E3 -->|generates| M4[person method]
        E4 -->|generates| M5[teams method]
    end

    subgraph "Runtime"
        USER[User Code]
        USER -->|calls| API[api.Schedule.schedule]
        API -->|validates params| EM[EndpointMethod]
        EM -->|builds URL| HTTP[HTTP Request]
        HTTP -->|gets| MLB[MLB Stats API]
        MLB -->|returns| RESP[APIResponse]
        RESP -->|wraps data| META[Metadata + Timestamp]
        RESP -->|can save| FILE[Gzipped JSON]
    end

    style S1 fill:#e1f5ff
    style S2 fill:#e1f5ff
    style S3 fill:#e1f5ff
    style S4 fill:#e1f5ff
    style S5 fill:#e1f5ff
    style S6 fill:#e1f5ff
    style REG fill:#fff4e6
    style API fill:#e8f5e9
    style RESP fill:#f3e5f5
```

## Component Breakdown

### 1. Schema Layer (`pymlb_statsapi/resources/schemas/`)

```
schemas/
└── statsapi/
    └── stats_api_1_0/
        ├── schedule.json      # Schedule endpoints
        ├── game.json          # Game data endpoints
        ├── person.json        # Player/person endpoints
        ├── team.json          # Team endpoints
        ├── stats.json         # Statistics endpoints
        └── ...
```

**Schema Structure:**
```json
{
  "apiVersion": "1.0",
  "swaggerVersion": "1.2",
  "apis": [
    {
      "path": "/v1/schedule",
      "description": "schedule",
      "operations": [
        {
          "method": "GET",
          "nickname": "schedule",
          "summary": "View schedule info",
          "parameters": [
            {
              "name": "sportId",
              "paramType": "query",
              "type": "integer",
              "required": false
            }
          ]
        }
      ]
    }
  ]
}
```

### 2. Schema Loader (`pymlb_statsapi/utils/schema_loader.py`)

```mermaid
graph LR
    A[SchemaLoader] -->|discover| B[Get Available Schemas]
    B -->|list .json files| C[schedule.json, game.json, ...]
    A -->|load| D[Read JSON Schema]
    D -->|parse| E[Validate Structure]
    E -->|return| F[Python Dict]

    style A fill:#fff4e6
    style F fill:#e8f5e9
```

**Key Methods:**
- `get_available_schemas()` - List all schema files
- `load_stats_schema(name)` - Load a specific schema
- `load_endpoint_model(name)` - Load endpoint configuration

### 3. Registry & Factory (`pymlb_statsapi/model/`)

#### StatsAPI Registry

```mermaid
graph TB
    R[StatsAPI Registry] -->|singleton| API[api instance]
    R -->|discovers| S[Available Schemas]
    S -->|for each schema| E[Create Endpoint]
    E -->|stores in| CACHE[_endpoints dict]

    USER[user code] -->|accesses| API
    API -->|api.Schedule| ATTR[__getattr__]
    ATTR -->|returns cached| ENDPOINT[Schedule Endpoint]

    style R fill:#fff4e6
    style API fill:#e8f5e9
    style ENDPOINT fill:#e1f5ff
```

**Lazy Loading:**
- Endpoints created on first access
- Cached for subsequent calls
- Attribute access: `api.Schedule` → `Endpoint("schedule")`

#### Endpoint Factory

```mermaid
graph TB
    SCHEMA[JSON Schema] -->|parsed by| EP[Endpoint.__init__]
    EP -->|for each operation| METHOD[Create Method]
    METHOD -->|wraps in| EM[EndpointMethod]
    EM -->|generates| FUNC[Dynamic Function]
    FUNC -->|attached to| ENDPOINT[Endpoint Instance]

    USER[user.schedule] -->|calls| FUNC
    FUNC -->|validates| PARAMS[Parameters]
    PARAMS -->|builds| URL[Request URL]
    URL -->|executes| HTTP[HTTP GET]
    HTTP -->|wraps| RESP[APIResponse]

    style SCHEMA fill:#e1f5ff
    style ENDPOINT fill:#fff4e6
    style RESP fill:#f3e5f5
```

**Dynamic Method Generation:**
```python
# Schema operation becomes a callable method
operation = {
    "method": "GET",
    "nickname": "schedule",
    "parameters": [...]
}

# Generates:
endpoint.schedule(sportId=1, date="2024-10-27")
```

### 4. Request Execution Flow

```mermaid
sequenceDiagram
    participant U as User Code
    participant E as Endpoint
    participant EM as EndpointMethod
    participant V as Validator
    participant H as HTTP Client
    participant M as MLB API
    participant R as APIResponse

    U->>E: schedule(sportId=1)
    E->>EM: _execute_request()
    EM->>V: validate_and_resolve_params()
    V->>V: Check required params
    V->>V: Validate enums
    V->>V: Handle multiple values
    V-->>EM: validated params + resolved URL

    EM->>H: requests.get(url, params)
    H->>M: GET /api/v1/schedule?sportId=1

    alt Success (200)
        M-->>H: JSON response
        H-->>EM: Response object
        EM->>R: APIResponse(response, metadata)
        R-->>U: response
    else Error (4xx/5xx)
        M-->>H: Error response
        H-->>EM: Error
        EM->>EM: Retry with backoff
        EM->>H: requests.get() [retry]
    end
```

### 5. Response Handling

```mermaid
graph TB
    RESP[APIResponse] -->|contains| META[Metadata]
    RESP -->|contains| DATA[JSON Data]
    RESP -->|has| TIME[Timestamp]

    META -->|request info| REQ[URL, params, method]
    META -->|response info| RES[status, elapsed_ms]

    USER[User] -->|calls| JSON[response.json]
    USER -->|calls| SAVE[response.gzip]
    USER -->|calls| URI[response.get_uri]

    JSON -->|returns| DATA
    SAVE -->|creates| FILE[.json.gz file]
    FILE -->|contains| WRAP[metadata + data]

    style RESP fill:#f3e5f5
    style META fill:#e1f5ff
    style FILE fill:#fff4e6
```

**Storage Format:**
```json
{
  "metadata": {
    "request": {
      "endpoint_name": "schedule",
      "method_name": "schedule",
      "path_params": {},
      "query_params": {"sportId": "1"},
      "url": "https://statsapi.mlb.com/api/v1/schedule?sportId=1",
      "timestamp": "2025-01-15T10:30:00.123456+00:00"
    },
    "response": {
      "status_code": 200,
      "elapsed_ms": 245.3
    }
  },
  "data": {
    "dates": [...]
  }
}
```

### 6. Parameter Validation Flow

```mermaid
graph TB
    CALL[Method Call] -->|with params| VAL[validate_and_resolve_params]

    VAL -->|check| PATH[Path Parameters]
    PATH -->|required?| PREQ{Required?}
    PREQ -->|yes & missing| ERR1[AssertionError]
    PREQ -->|yes & present| PENUM{Has enum?}
    PENUM -->|yes| VALENUM[Validate enum]
    VALENUM -->|invalid| ERR2[AssertionError]
    VALENUM -->|valid| PATHOK[Add to validated]
    PENUM -->|no| PATHOK

    VAL -->|check| QUERY[Query Parameters]
    QUERY -->|required?| QREQ{Required?}
    QREQ -->|yes & missing| ERR3[AssertionError]
    QREQ -->|yes & present| QMULTI{Allow multiple?}
    QMULTI -->|yes| QJOIN[Join with comma]
    QMULTI -->|no & multiple| ERR4[AssertionError]
    QJOIN -->|add to| QUERYOK[Add to validated]
    QMULTI -->|no & single| QUERYOK

    PATHOK -->|resolve| TEMPLATE[Path template]
    TEMPLATE -->|replace| URL[Final URL]
    QUERYOK -->|append| URL

    URL -->|return| DONE[Ready for HTTP]

    style ERR1 fill:#ffebee
    style ERR2 fill:#ffebee
    style ERR3 fill:#ffebee
    style ERR4 fill:#ffebee
    style DONE fill:#e8f5e9
```

### 7. HTTP Retry Logic

```mermaid
graph TB
    REQ[HTTP Request] -->|execute| TRY[Try Request]
    TRY -->|check| STATUS{Status?}

    STATUS -->|200 OK| SUCCESS[Return Response]
    STATUS -->|4xx/5xx| CHECK{Retries left?}
    STATUS -->|Network Error| CHECK

    CHECK -->|yes| SLEEP[sleep attempt]
    SLEEP -->|exponential backoff| RETRY[Retry Request]
    RETRY --> TRY

    CHECK -->|no| FAIL[Raise Error]

    style SUCCESS fill:#e8f5e9
    style FAIL fill:#ffebee
    style SLEEP fill:#fff4e6
```

**Retry Parameters:**
- `MAX_RETRIES` = 3
- Backoff: `sleep(attempt)` → 0s, 1s, 2s
- Retries on: 5xx errors, connection errors, timeouts
- No retry on: 4xx errors (but currently retries due to AssertionError)

## Data Flow Summary

```mermaid
graph LR
    A[JSON Schemas] -->|loaded by| B[SchemaLoader]
    B -->|provides to| C[StatsAPI Registry]
    C -->|creates| D[Endpoints]
    D -->|generates| E[Dynamic Methods]
    E -->|called by| F[User Code]
    F -->|validates| G[Parameters]
    G -->|builds| H[HTTP Request]
    H -->|calls| I[MLB API]
    I -->|returns| J[APIResponse]
    J -->|saves to| K[Gzipped JSON]

    style A fill:#e1f5ff
    style C fill:#fff4e6
    style E fill:#e8f5e9
    style J fill:#f3e5f5
    style K fill:#fff9c4
```

## Key Design Principles

1. **100% Schema-Driven**
   - No hardcoded endpoint classes
   - Everything generated from JSON schemas
   - Add new endpoints by adding schemas

2. **Zero Manual Maintenance**
   - Methods auto-generated at runtime
   - Parameter validation from schema
   - Documentation from schema metadata

3. **Type-Safe Without Types**
   - Runtime parameter validation
   - Enum checking
   - Required/optional enforcement

4. **Efficient Storage**
   - Gzip compression (80-95% reduction)
   - Metadata wrapping with timestamps
   - Reproducible data snapshots

5. **Robust Error Handling**
   - Automatic retry with backoff
   - Clear validation errors
   - Helpful error messages

6. **Developer Experience**
   - IDE autocomplete (via `__getattr__`)
   - Introspection methods (`.get_schema()`, `.list_parameters()`)
   - Helpful method docstrings generated from schemas
