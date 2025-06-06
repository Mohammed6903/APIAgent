API Testing Report

Here's the report of the API testing performed on `http://127.0.0.1:8000` based on the provided `openapi.json` documentation.

### Test Results Summary

| Endpoint | Method | Status Code | Expected Status | Result | Notes |
|---|---|---|---|---|---|
| `/api/v1/analytics/generate-chart-data` | GET | 200 | 200 | PASS | Successfully retrieved data. |
| `/api/v1/bias/bias-analysis` | POST | 200 | 200/201 | PASS | Successfully analyzed bias. |
| `/api/v1/chat/update_chat_history` | POST | 200 | 200/201 | PASS | Successfully updated chat history. |
| `/api/v1/chat/get_chat_history` | GET | 200 | 200 | PASS | Successfully retrieved chat history. |
| `/api/v1/email/send-email/individual` | POST | 200 | 200/201 | PASS | Successfully sent individual email (mock). |
| `/api/v1/email/send-email/bulk` | POST | 200 | 200/201 | PASS | Successfully sent bulk emails (mock). |
| `/api/v1/file/get_file/test.txt` | GET | 200 | 200 | PASS | Successfully retrieved file (mock). |
| `/api/v1/interview/analyze_interview` | POST | 200 | 200/201 | PASS | Successfully analyzed interview (mock). |
| `/api/v1/personnel/selected-personnel/upload` | POST | 200 | 200/201 | PASS | Successfully uploaded selected personnel (mock). |
| `/api/v1/personnel/selected-personnel` | GET | 200 | 200 | PASS | Successfully retrieved selected personnel. |
| `/api/v1/project/process_url_or_path` | POST | 200 | 200/201 | PASS | Successfully processed URL/path (mock). |
| `/api/v1/project/analyze_project/` | POST | 200 | 200/201 | PASS | Successfully analyzed project (mock). |
| `/api/v1/project/process_upload/` | POST | 422 | 200/201 | FAIL | Validation Error: Invalid file format (expected binary, got string). |
| `/api/v1/resume/resume-analysis-results` | GET | 200 | 200 | PASS | Successfully retrieved resume analysis results. |
| `/api/v1/resume/rank-resumes` | POST | 200 | 200/201 | PASS | Successfully ranked resumes (mock). |
| `/api/v1/resume/rank-resumes` | OPTIONS | 200 | 200 | PASS | Successfully handled OPTIONS request. |

### Detailed Test Results

#### 1. GET /api/v1/analytics/generate-chart-data

*   **Method:** GET
*   **URL:** `http://127.0.0.1:8000/api/v1/analytics/generate-chart-data`
*   **Status Code:** 200
*   **Expected Status:** 200
*   **Result:** PASS
*   **Notes:** The request was successful, and the API returned a 200 OK status.

#### 2. POST /api/v1/bias/bias-analysis

*   **Method:** POST
*   **URL:** `http://127.0.0.1:8000/api/v1/bias/bias-analysis`
*   **Request Body (Generated):**
    ```json
    {
        "job_title": "Software Engineer",
        "job_description": "Develop and maintain software applications.",
        "analysis_types": ["gender", "age"]
    }
    ```
*   **Status Code:** 200
*   **Expected Status:** 200 or 201
*   **Result:** PASS
*   **Notes:** The request was successful, and the API returned a 200 OK status.

#### 3. POST /api/v1/chat/update_chat_history

*   **Method:** POST
*   **URL:** `http://127.0.0.1:8000/api/v1/chat/update_chat_history`
*   **Request Body (Generated):**
    ```json
    {
        "conf_uid": "conf123",
        "history_uid": "hist456",
        "history": [
            {
                "role": "user",
                "timestamp": "2023-01-01T10:00:00Z",
                "content": "Hello",
                "name": "John Doe",
                "avatar": "avatar_url"
            }
        ],
        "timestamp": "2023-01-01T10:05:00Z"
    }
    ```
*   **Status Code:** 200
*   **Expected Status:** 200 or 201
*   **Result:** PASS
*   **Notes:** The request was successful, and the API returned a 200 OK status.

#### 4. GET /api/v1/chat/get_chat_history

*   **Method:** GET
*   **URL:** `http://127.0.0.1:8000/api/v1/chat/get_chat_history`
*   **Status Code:** 200
*   **Expected Status:** 200
*   **Result:** PASS
*   **Notes:** The request was successful, and the API returned a 200 OK status.

#### 5. POST /api/v1/email/send-email/individual

*   **Method:** POST
*   **URL:** `http://127.0.0.1:8000/api/v1/email/send-email/individual`
*   **Request Body (Generated):**
    ```json
    {
        "ranked_resumes": [{}],
        "candidate_index": 0,
        "sender_email": "test@example.com",
        "password": "password123",
        "job_description": {},
        "project_options": {},
        "company_info": {}
    }
    ```
*   **Status Code:** 200
*   **Expected Status:** 200 or 201
*   **Result:** PASS
*   **Notes:** The request was successful, and the API returned a 200 OK status.

#### 6. POST /api/v1/email/send-email/bulk

*   **Method:** POST
*   **URL:** `http://127.0.0.1:8000/api/v1/email/send-email/bulk`
*   **Request Body (Generated):**
    ```json
    {
        "ranked_resumes": [{}, {}],
        "sender_email": "bulk@example.com",
        "password": "bulkpassword",
        "job_description": {},
        "project_options": {},
        "company_info": {}
    }
    ```
*   **Status Code:** 200
*   **Expected Status:** 200 or 201
*   **Result:** PASS
*   **Notes:** The request was successful, and the API returned a 200 OK status.

#### 7. GET /api/v1/file/get_file/{file_name}

*   **Method:** GET
*   **URL:** `http://127.0.0.1:8000/api/v1/file/get_file/test.txt`
*   **Status Code:** 200
*   **Expected Status:** 200
*   **Result:** PASS
*   **Notes:** The request was successful, and the API returned a 200 OK status.

#### 8. POST /api/v1/interview/analyze_interview

*   **Method:** POST
*   **URL:** `http://127.0.0.1:8000/api/v1/interview/analyze_interview?history_uid=hist789`
*   **Status Code:** 200
*   **Expected Status:** 200 or 201
*   **Result:** PASS
*   **Notes:** The request was successful, and the API returned a 200 OK status.

#### 9. POST /api/v1/personnel/selected-personnel/upload

*   **Method:** POST
*   **URL:** `http://127.0.0.1:8000/api/v1/personnel/selected-personnel/upload`
*   **Request Body (Generated):**
    ```json
    {
        "resume_id": "resume123",
        "profile": {
            "name": "Jane Doe",
            "experience": "5 years"
        },
        "selection_date": "2023-01-01",
        "selection_reason": "Good fit"
    }
    ```
*   **Status Code:** 200
*   **Expected Status:** 200 or 201
*   **Result:** PASS
*   **Notes:** The request was successful, and the API returned a 200 OK status.

#### 10. GET /api/v1/personnel/selected-personnel

*   **Method:** GET
*   **URL:** `http://127.0.0.1:8000/api/v1/personnel/selected-personnel`
*   **Status Code:** 200
*   **Expected Status:** 200
*   **Result:** PASS
*   **Notes:** The request was successful, and the API returned a 200 OK status.

#### 11. POST /api/v1/project/process_url_or_path

*   **Method:** POST
*   **URL:** `http://127.0.0.1:8000/api/v1/project/process_url_or_path?compressed=false`
*   **Request Body (Generated):**
    ```json
    {
        "input_path": "https://example.com/project"
    }
    ```
*   **Status Code:** 200
*   **Expected Status:** 200 or 201
*   **Result:** PASS
*   **Notes:** The request was successful, and the API returned a 200 OK status.

#### 12. POST /api/v1/project/analyze_project/

*   **Method:** POST
*   **URL:** `http://127.0.0.1:8000/api/v1/project/analyze_project/`
*   **Request Body (Generated):**
    ```json
    {
        "input_path": "/path/to/project"
    }
    ```
*   **Status Code:** 200
*   **Expected Status:** 200 or 201
*   **Result:** PASS
*   **Notes:** The request was successful, and the API returned a 200 OK status.

#### 13. POST /api/v1/project/process_upload/

*   **Method:** POST
*   **URL:** `http://127.0.0.1:8000/api/v1/project/process_upload/`
*   **Request Body (Generated):**
    ```python
    # Note: This is a simplified representation. Actual request requires multipart/form-data with binary file.
    # Attempting to send a string 'dummy_file_content'
    data = {"file": "dummy_file_content"}
    ```
*   **Status Code:** 422
*   **Expected Status:** 200 or 201
*   **Result:** FAIL
*   **Notes:** The API returned a 422 Unprocessable Entity error. This is expected as the `api_request` tool does not directly support sending `multipart/form-data` with binary file uploads as required by the `file` field with `format: binary`. The error indicates a validation failure for the file type.

#### 14. GET /api/v1/resume/resume-analysis-results

*   **Method:** GET
*   **URL:** `http://127.0.0.1:8000/api/v1/resume/resume-analysis-results`
*   **Status Code:** 200
*   **Expected Status:** 200
*   **Result:** PASS
*   **Notes:** The request was successful, and the API returned a 200 OK status.

#### 15. POST /api/v1/resume/rank-resumes

*   **Method:** POST
*   **URL:** `http://127.0.0.1:8000/api/v1/resume/rank-resumes`
*   **Request Body (Generated):**
    ```json
    {
        "job_description": "We are looking for a highly motivated individual...",
        "resumes_file": "resume_analysis_results.json"
    }
    ```
*   **Status Code:** 200
*   **Expected Status:** 200 or 201
*   **Result:** PASS
*   **Notes:** The request was successful, and the API returned a 200 OK status.

#### 16. OPTIONS /api/v1/resume/rank-resumes

*   **Method:** OPTIONS
*   **URL:** `http://127.0.0.1:8000/api/v1/resume/rank-resumes`
*   **Status Code:** 200
*   **Expected Status:** 200
*   **Result:** PASS
*   **Notes:** The OPTIONS request was successful, indicating proper CORS preflight handling.