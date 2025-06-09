from agno.agent import Agent
from agno.models.google import Gemini
from agno.team import Team
from agno.tools.file import FileTools
from Tools.file import get_dir_tree
from textwrap import dedent
from Tools.api import APIRequest
from Tools.endpoints import APIEndpointTracker
from Documentor import PostProcessingAgent
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
# from agno.storage.sqlite import SqliteStorage

memory_db = SqliteMemoryDb(table_name="memory", db_file="tmp/memory.db")
memory = Memory(db=memory_db)

session_id = "session_1"
john_doe_id = "john_doe@example.com"

tester = Agent(
    name="API Tester",
    role="Tests API endpoints",
    model=Gemini(id="gemini-2.5-flash-preview-04-17"),
    tools=[
        FileTools(),
        APIEndpointTracker("api_test_progress.json"),
        APIRequest,
    ],
    memory=memory,
    description="You are an API testing tool. You test the APIs and return the results.",
    instructions="""
        You are an advanced API testing agent with systematic endpoint tracking capabilities.

        ## INITIALIZATION PHASE
        1. **Endpoint Tracker Setup**:
            - Use APIEndpointTracker to manage endpoint testing state
            - This tracker will maintain state across testing sessions and prevent duplicate testing
            - Load any existing progress from previous runs

        2. **Documentation Processing**:
            - If documentation URL provided: Use APIRequest to fetch OpenAPI/Swagger spec
            - If documentation file provided: Read using FileTools
            - Parse documentation and populate tracker using `load_openapi_spec()` or manual `add_endpoint()` calls
            - Verify all endpoints are registered before starting tests

        ## SYSTEMATIC TESTING WORKFLOW
        3. **Pre-Test Validation**:
            - Use `tracker.get_testing_progress()` to show initial status
            - Validate that all endpoints from documentation are registered
            - Check for any previously tested endpoints to avoid duplication

        4. **Intelligent Endpoint Selection**:
            - Use `tracker.get_next_endpoint_to_test(method_priority=["GET", "POST", "PUT", "DELETE"])` 
            - Prioritize GET requests first (safer), then POST, PUT, DELETE
            - Process endpoints systematically rather than randomly

        5. **Enhanced Request Preparation**:
            - For GET requests: Extract query parameters from endpoint metadata
            - For POST/PUT requests: Generate sample payloads based on request body schemas
            - Use realistic test data (not just "string"/"123") based on field names and types
            - Handle required vs optional parameters intelligently
            - Implement authentication headers if specified in documentation

        6. **Comprehensive Testing Execution**:
            - Test each endpoint exactly once using APIRequest tool
            - Capture detailed metrics: response time, status code, headers, body structure
            - **STRICT DATA TYPE VALIDATION**: Verify response matches documented schema exactly
            - Check for proper HTTP status codes (200/201 for success, 4xx/5xx for errors)
            - Validate response content-type headers
            - Record actual vs expected response structure mismatches

        7. **Progress Tracking & State Management**:
            - After each test: `tracker.mark_endpoint_tested(path, method, status, test_details)`
            - Use TestStatus.TESTED for successful tests, TestStatus.FAILED for failures
            - Store detailed test results including validation errors in test_details
            - Automatically save progress after each endpoint

        8. **Error Handling & Resilience**:
            - Handle network timeouts, connection errors gracefully
            - Distinguish between endpoint failures vs network issues
            - Continue testing remaining endpoints even if some fail
            - Rate limit handling: pause if receiving 429 responses

        ## VALIDATION & REPORTING
        9. **Data Type Strict Checking**:
            - Compare actual response data types against documented schemas
            - Flag mismatches: string vs number, array vs object, missing required fields
            - Validate enum values, format constraints (email, date, UUID)
            - Check for unexpected additional fields not in documentation

        10. **Comprehensive Reporting**:
            - Generate detailed markdown report with:
                * Executive summary with pass/fail statistics
                * Per-endpoint results table: Method | Path | Status | Response Time | Validation Issues
                * Data type validation failures section
                * Schema compliance summary
                * Recommendations for API improvements
            - Use `tracker.get_testing_progress()` for overall statistics
            - Save report as `api_testing_report.md` using FileTools

        11. **Final Validation**:
            - Ensure `tracker.get_pending_endpoints()` returns empty list
            - Verify 100% endpoint coverage from documentation
            - Provide summary of untested endpoints if any remain

        ## EFFICIENCY OPTIMIZATIONS
        - Batch similar requests where possible
        - Reuse authentication tokens across requests
        - Parallel processing of independent GET requests (if tool supports)
        - Skip redundant validation for identical response schemas
        - Cache successful authentication for subsequent requests

        ## ERROR RECOVERY
        - Resume testing from last successful endpoint if interrupted
        - Handle partial responses and malformed JSON gracefully
        - Provide clear error messages for debugging
        - Log all HTTP request/response details for troubleshooting

        Remember: 
        - Always use the endpoint tracker for state management
        - Focus on data type accuracy over response content
        - Test thoroughly but efficiently
        - Maintain detailed logs for debugging
    """,
    show_tool_calls=True,
    markdown=True,
    enable_user_memories=True,
)

documentor = PostProcessingAgent(
    name="API Documentor",
    role="Generates API documentation",
    model=Gemini(id="gemini-2.5-flash-preview-04-17"),
    tools=[FileTools(), get_dir_tree],
    description=dedent("""
        You are an API analysis tool. You generate and save their proper documentations in JSON format in the working directory.
    """),
    instructions=dedent("""
        You are an advanced API documentation generator with systematic analysis capabilities.

        ## ANALYSIS WORKFLOW
        1. **Project Structure Analysis**:
            - Use `get_dir_tree()` to map complete project structure
            - Identify framework type: FastAPI, Flask, Django, Express.js, Spring Boot, etc.
            - Locate configuration files, route definitions, model definitions
            - Identify database models/schemas that inform API responses

        2. **Deep Code Analysis**:
            - Read all relevant API files using FileTools
            - Extract endpoints with HTTP methods, paths, parameters
            - Analyze request/response models, validation rules, decorators
            - Identify authentication/authorization requirements
            - Extract business logic to understand expected behaviors

        3. **Comprehensive Endpoint Documentation**:
            - Generate full OpenAPI 3.0 compliant JSON specification
            - Include detailed parameter schemas with types, formats, constraints
            - Document request body schemas with examples
            - Provide comprehensive response schemas for all status codes
            - Add realistic example values based on field names and business context

        4. **Enhanced Metadata Extraction**:
            - Extract endpoint descriptions from code comments/docstrings
            - Identify parameter validation rules (min/max, regex patterns)
            - Document error responses and their conditions
            - Include rate limiting, authentication requirements
            - Add operation IDs and tags for organization

        5. **Quality Validation**:
            - Ensure all endpoints have complete request/response schemas
            - Validate JSON schema compliance
            - Check for missing required fields, inconsistent naming
            - Verify data type accuracy (string, integer, array, object)

        6. **Integration with Endpoint Tracker**:
            - After generating documentation, create endpoint tracker instance
            - Use `load_openapi_spec(tracker, openapi_spec)` to populate tracker
            - This enables systematic testing of all documented endpoints
            - Save tracker state for handoff to testing agent

        ## OUTPUT REQUIREMENTS
        7. **Documentation Structure**:
            ```json
            {
                "openapi": "3.0.0",
                "info": {
                    "title": "Generated API Documentation",
                    "version": "1.0.0",
                    "description": "Comprehensive API documentation extracted from source code"
                },
                "servers": [{"url": "http://localhost:8000", "description": "Development server"}],
                "paths": {
                    "/endpoint": {
                        "get": {
                            "summary": "Clear endpoint description",
                            "parameters": [...],
                            "responses": {
                                "200": {
                                    "description": "Success response",
                                    "content": {
                                        "application/json": {
                                            "schema": {...},
                                            "example": {...}
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "components": {
                    "schemas": {...},
                    "securitySchemes": {...}
                }
            }
            ```

        8. **File Operations**:
            - Save primary documentation as `api_documentation.json`
            - Create summary markdown as `api_endpoints_summary.md`
            - Generate endpoint tracking initialization file

        ## FRAMEWORK-SPECIFIC ANALYSIS
        - **FastAPI**: Extract from route decorators, Pydantic models, response_model parameters
        - **Flask**: Analyze route functions, request parsing, jsonify responses
        - **Django**: Extract from URLs, views, serializers, model definitions
        - **Express.js**: Parse route definitions, middleware, response patterns
        - **Spring Boot**: Analyze controllers, request/response entities, validation annotations

        ## QUALITY ASSURANCE
        - Ensure every endpoint has complete documentation
        - Validate realistic example data
        - Check for consistent naming conventions
        - Verify proper HTTP status code usage
        - Include edge cases and error scenarios
    """),
    show_tool_calls=True,
    markdown=True,
    memory=memory,
    enable_user_memories=True,
)

organizer = Team(
    name="API Testing Team",
    mode="coordinate",
    model=Gemini(id="gemini-2.5-flash-preview-04-17"),
    tools=[FileTools(), APIRequest],
    description="You are a testing team coordinator. Your goal is to test a given api and if there is no documentation present or given for an api, document it.",
    instructions=[
        # INITIALIZATION AND DISCOVERY PHASE
        "1. **Project Assessment**: Begin by determining available documentation sources:",
        "   - If client provides documentation URL (OpenAPI/Swagger), validate accessibility using APIRequest",
        "   - If no URL provided, analyze project structure to identify framework and auto-generated docs",
        "   - Common endpoints to check: /docs, /swagger, /openapi.json, /api-docs, /swagger-ui",
        "2. **Framework Detection and Documentation Strategy**:",
        "   - FastAPI: Check /docs and /openapi.json endpoints",
        "   - Django REST: Look for /swagger/ or /redoc/ endpoints",
        "   - Flask: Check for flask-restx or flasgger documentation",
        "   - Spring Boot: Look for /swagger-ui.html or /v3/api-docs",
        "   - Express.js: Check for swagger-jsdoc or similar implementations",
        # DOCUMENTATION PHASE
        "3. **Documentation Acquisition Strategy**:",
        "   - **If live documentation exists**: Use tester to fetch and validate documentation completeness",
        "   - **If no live docs**: Deploy documentor to generate comprehensive API documentation",
        "   - **Hybrid approach**: Use live docs as primary, generate supplementary docs for gaps",
        "4. **Documentation Quality Validation**:",
        "   - Verify documentation completeness: all endpoints, parameters, responses",
        "   - Check for realistic example data and proper data types",
        "   - Ensure authentication/authorization requirements are documented",
        "   - Validate OpenAPI 3.0 compliance if applicable",
        # ENDPOINT TRACKING SETUP
        "5. **Endpoint Tracking Initialization**:",
        "   - Instruct tester to initialize APIEndpointTracker with persistent storage",
        "   - Load all endpoints from documentation into tracker system",
        "   - Verify tracker shows complete endpoint inventory before testing begins",
        "   - Establish baseline metrics: total endpoints, methods distribution, complexity assessment",
        # SYSTEMATIC TESTING PHASE
        "6. **Comprehensive Testing Execution**:",
        "   - Direct tester to use systematic endpoint selection via tracker.get_next_endpoint_to_test()",
        "   - Prioritize testing order: GET → POST → PUT → DELETE for safety",
        "   - Require strict data type validation against documented schemas",
        "   - Monitor progress using tracker.get_testing_progress() at regular intervals",
        "7. **Quality Assurance Requirements**:",
        "   - **Strict Data Type Checking**: Every response field type must match documentation exactly",
        "   - **Status Code Validation**: 200/201 for success, proper 4xx/5xx for errors",
        "   - **Schema Compliance**: Response structure must match documented format",
        "   - **Authentication Testing**: Verify secured endpoints require proper authentication",
        # PROGRESS MONITORING
        "8. **Continuous Progress Monitoring**:",
        "   - Request progress updates after every 10 endpoints tested",
        "   - Monitor for stuck/failed endpoints and provide resolution guidance",
        "   - Ensure no endpoints are skipped or tested multiple times",
        "   - Validate that tracker state persists correctly between sessions",
        "9. **Error Handling and Recovery**:",
        "   - If tester encounters failures, analyze root cause: network, server, or documentation issues",
        "   - Distinguish between temporary failures (retry) vs permanent issues (document and continue)",
        "   - For authentication failures, verify credentials and endpoint security requirements",
        "   - Handle rate limiting gracefully with appropriate delays",
        # COMPLETION AND REPORTING
        "10. **Testing Completion Validation**:",
        "    - Verify tracker.get_pending_endpoints() returns empty list",
        "    - Confirm 100% endpoint coverage from original documentation",
        "    - Validate no endpoints were missed or inadequately tested",
        "    - Ensure all test results are properly recorded in tracker",
        "11. **Comprehensive Reporting Requirements**:",
        "    - Generate executive summary with overall API health assessment",
        "    - Provide detailed endpoint results: method, path, status, response time, validation issues",
        "    - Include data type validation failures with specific field-level details",
        "    - Document schema compliance issues and recommendations",
        "    - Save final report as `api_testing_report.md` with timestamp",
        # EFFICIENCY OPTIMIZATIONS
        "12. **Performance and Efficiency Measures**:",
        "    - Batch similar requests where possible to reduce overhead",
        "    - Implement intelligent retry logic for transient failures",
        "    - Use endpoint metadata to prepare better test data",
        "    - Cache authentication tokens to avoid repeated login requests",
        "13. **Final Deliverables Checklist**:",
        "    - ✅ Complete endpoint inventory in tracker",
        "    - ✅ 100% endpoint testing coverage",
        "    - ✅ Detailed test results with data type validation",
        "    - ✅ Comprehensive markdown report",
        "    - ✅ Persistent tracker state for future runs",
        "    - ✅ Recommendations for API improvements",
        # COMMUNICATION PROTOCOLS
        "14. **Team Communication Standards**:",
        "    - Provide clear, specific instructions when delegating tasks",
        "    - Include endpoint URLs, expected methods, and validation requirements",
        "    - Request confirmation of task completion before proceeding",
        "    - Share tracker progress data between team members",
        "    - Escalate critical issues immediately rather than continuing with incomplete data",
    ],
    members=[
        documentor,
        tester,
    ],
    add_datetime_to_instructions=True,
    add_member_tools_to_system_message=False,
    enable_agentic_context=True,
    enable_team_history=True,
    num_of_interactions_from_history=5,
    share_member_interactions=True,
    show_members_responses=True,
    show_tool_calls=True,
    markdown=True,
    memory=memory,
    enable_user_memories=True,
)

organizer.print_response(
    """
        Test API at http://127.0.0.1:8000 with documentation at http://127.0.0.1:8000/openapi.json.
        
        Requirements:
        - Strict data type validation - every field must match documented schema exactly
        - Status code validation - 200/201 for success operations
        - Complete endpoint coverage - test every documented endpoint
        - Comprehensive error reporting with specific validation failures
        - Use endpoint tracker for systematic testing and progress monitoring
        
        Generate detailed report with:
        - Executive summary of API health
        - Per-endpoint validation results
        - Data type compliance issues
        - Performance metrics
        - Recommendations for improvements
    """,
    # stream=True,
)
