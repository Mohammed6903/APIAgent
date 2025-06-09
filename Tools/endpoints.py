import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, asdict
from enum import Enum
import threading
from agno.tools import Toolkit, tool


class TestStatus(Enum):
    PENDING = "pending"
    TESTED = "tested"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class EndpointInfo:
    """Data class to store endpoint information"""

    path: str
    method: str
    summary: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    request_body: Optional[Dict[str, Any]] = None
    responses: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    status: TestStatus = TestStatus.PENDING
    test_timestamp: Optional[str] = None
    test_details: Optional[Dict[str, Any]] = None
    endpoint_id: str = uuid.uuid4().hex

    def __post_init__(self):
        if self.endpoint_id is None:
            self.endpoint_id = str(uuid.uuid4())


class APIEndpointTracker(Toolkit):
    """
    A comprehensive tool to track API endpoints for testing.
    Manages endpoint registration, testing status, and provides various query methods.
    """

    def __init__(self, storage_file: Optional[str] = None, **kwargs):
        super().__init__(name="file_tools", **kwargs)
        self.endpoints: Dict[str, EndpointInfo] = {}
        self.storage_file = storage_file
        self._lock = threading.Lock()

        if storage_file:
            self.load_from_file()

    def add_endpoint(
        self,
        path: str,
        method: str,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        request_body: Optional[Dict[str, Any]] = None,
        responses: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
    ) -> str:
        """
        Add a new endpoint to track.

        Args:
            path: API endpoint path (e.g., '/users/{id}')
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            summary: Brief description of the endpoint
            description: Detailed description
            parameters: Parameter definitions
            request_body: Request body schema
            responses: Response definitions
            tags: List of tags for categorization

        Returns:
            str: Unique endpoint ID
        """
        with self._lock:
            endpoint = EndpointInfo(
                path=path,
                method=method.upper(),
                summary=summary,
                description=description,
                parameters=parameters or {},
                request_body=request_body,
                responses=responses or {},
                tags=tags or [],
            )

            # Use combination of method and path as key for quick lookup
            key = f"{method.upper()}:{path}"
            self.endpoints[key] = endpoint

            if self.storage_file:
                self.save_to_file()

            return endpoint.endpoint_id

    def add_endpoints_bulk(self, endpoints: List[Dict[str, Any]]) -> List[str]:
        """
        Add multiple endpoints at once.

        Args:
            endpoints: List of endpoint dictionaries

        Returns:
            List[str]: List of endpoint IDs
        """
        endpoint_ids = []
        for ep in endpoints:
            endpoint_id = self.add_endpoint(**ep)
            endpoint_ids.append(endpoint_id)
        return endpoint_ids

    def mark_endpoint_tested(
        self,
        path: str,
        method: str,
        status: TestStatus = TestStatus.TESTED,
        test_details: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Mark an endpoint as tested and optionally remove it from tracking.

        Args:
            path: API endpoint path
            method: HTTP method
            status: Test status (TESTED, FAILED, SKIPPED)
            test_details: Additional test information

        Returns:
            bool: True if endpoint was found and updated, False otherwise
        """
        with self._lock:
            key = f"{method.upper()}:{path}"
            if key in self.endpoints:
                self.endpoints[key].status = status
                self.endpoints[key].test_timestamp = datetime.now().isoformat()
                self.endpoints[key].test_details = test_details or {}

                if self.storage_file:
                    self.save_to_file()

                return True
            return False

    def remove_endpoint(self, path: str, method: str) -> bool:
        """
        Remove an endpoint from tracking.

        Args:
            path: API endpoint path
            method: HTTP method

        Returns:
            bool: True if endpoint was found and removed, False otherwise
        """
        with self._lock:
            key = f"{method.upper()}:{path}"
            if key in self.endpoints:
                del self.endpoints[key]

                if self.storage_file:
                    self.save_to_file()

                return True
            return False

    def get_pending_endpoints(self) -> List[EndpointInfo]:
        """Get all endpoints that haven't been tested yet."""
        return [ep for ep in self.endpoints.values() if ep.status == TestStatus.PENDING]

    def get_tested_endpoints(self) -> List[EndpointInfo]:
        """Get all endpoints that have been tested."""
        return [ep for ep in self.endpoints.values() if ep.status == TestStatus.TESTED]

    def get_failed_endpoints(self) -> List[EndpointInfo]:
        """Get all endpoints that failed testing."""
        return [ep for ep in self.endpoints.values() if ep.status == TestStatus.FAILED]

    def get_endpoints_by_tag(self, tag: str) -> List[EndpointInfo]:
        """Get endpoints filtered by tag."""
        return [ep for ep in self.endpoints.values() if tag in (ep.tags or [])]

    def get_endpoints_by_method(self, method: str) -> List[EndpointInfo]:
        """Get endpoints filtered by HTTP method."""
        return [ep for ep in self.endpoints.values() if ep.method == method.upper()]

    def get_endpoint(self, path: str, method: str) -> Optional[EndpointInfo]:
        """Get a specific endpoint by path and method."""
        key = f"{method.upper()}:{path}"
        return self.endpoints.get(key)

    def get_testing_progress(self) -> Dict[str, Any]:
        """Get testing progress statistics."""
        total = len(self.endpoints)
        if total == 0:
            return {
                "total": 0,
                "tested": 0,
                "pending": 0,
                "failed": 0,
                "skipped": 0,
                "progress_percent": 0,
            }

        tested = len(
            [ep for ep in self.endpoints.values() if ep.status == TestStatus.TESTED]
        )
        pending = len(
            [ep for ep in self.endpoints.values() if ep.status == TestStatus.PENDING]
        )
        failed = len(
            [ep for ep in self.endpoints.values() if ep.status == TestStatus.FAILED]
        )
        skipped = len(
            [ep for ep in self.endpoints.values() if ep.status == TestStatus.SKIPPED]
        )

        progress_percent = ((tested + failed + skipped) / total) * 100

        return {
            "total": total,
            "tested": tested,
            "pending": pending,
            "failed": failed,
            "skipped": skipped,
            "progress_percent": round(progress_percent, 2),
        }

    def get_all_endpoints(self) -> List[EndpointInfo]:
        """Get all endpoints regardless of status."""
        return list(self.endpoints.values())

    def clear_all_endpoints(self) -> None:
        """Remove all endpoints from tracking."""
        with self._lock:
            self.endpoints.clear()

            if self.storage_file:
                self.save_to_file()

    def reset_endpoint_status(self, path: str, method: str) -> bool:
        """Reset an endpoint's status back to PENDING."""
        with self._lock:
            key = f"{method.upper()}:{path}"
            if key in self.endpoints:
                self.endpoints[key].status = TestStatus.PENDING
                self.endpoints[key].test_timestamp = None
                self.endpoints[key].test_details = None

                if self.storage_file:
                    self.save_to_file()

                return True
            return False

    def reset_all_endpoints(self) -> None:
        """Reset all endpoints status back to PENDING."""
        with self._lock:
            for endpoint in self.endpoints.values():
                endpoint.status = TestStatus.PENDING
                endpoint.test_timestamp = None
                endpoint.test_details = None

            if self.storage_file:
                self.save_to_file()

    def export_to_dict(self) -> Dict[str, Any]:
        """Export all endpoints to a dictionary."""
        return {
            "endpoints": [asdict(ep) for ep in self.endpoints.values()],
            "metadata": {
                "total_endpoints": len(self.endpoints),
                "export_timestamp": datetime.now().isoformat(),
            },
        }

    def import_from_dict(self, data: Dict[str, Any]) -> None:
        """Import endpoints from a dictionary."""
        with self._lock:
            self.endpoints.clear()

            for ep_data in data.get("endpoints", []):
                # Convert status string back to enum
                if isinstance(ep_data.get("status"), str):
                    ep_data["status"] = TestStatus(ep_data["status"])

                endpoint = EndpointInfo(**ep_data)
                key = f"{endpoint.method}:{endpoint.path}"
                self.endpoints[key] = endpoint

            if self.storage_file:
                self.save_to_file()

    def save_to_file(self) -> None:
        """Save endpoints to file."""
        if not self.storage_file:
            return

        try:
            data = self.export_to_dict()
            # Convert enum values to strings for JSON serialization
            for ep in data["endpoints"]:
                if isinstance(ep.get("status"), TestStatus):
                    ep["status"] = ep["status"].value

            with open(self.storage_file, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving to file: {e}")

    def load_from_file(self) -> None:
        """Load endpoints from file."""
        if not self.storage_file:
            return

        try:
            with open(self.storage_file, "r") as f:
                data = json.load(f)
            self.import_from_dict(data)
        except FileNotFoundError:
            # File doesn't exist yet, start with empty tracker
            pass
        except Exception as e:
            print(f"Error loading from file: {e}")

    def get_next_endpoint_to_test(
        self,
        method_priority: Optional[List[str]] = None,
        tag_filter: Optional[str] = None,
    ) -> Optional[EndpointInfo]:
        """
        Get the next endpoint that should be tested based on priority.

        Args:
            method_priority: List of HTTP methods in order of priority
            tag_filter: Only consider endpoints with this tag

        Returns:
            EndpointInfo or None: Next endpoint to test
        """
        pending_endpoints = self.get_pending_endpoints()

        if tag_filter:
            pending_endpoints = [
                ep for ep in pending_endpoints if tag_filter in (ep.tags or [])
            ]

        if not pending_endpoints:
            return None

        if method_priority:
            # Sort by method priority
            method_order = {method: i for i, method in enumerate(method_priority)}
            pending_endpoints.sort(key=lambda ep: method_order.get(ep.method, 999))

        return pending_endpoints[0]

    def load_openapi_spec(self, openapi_spec: Dict[str, Any]) -> List[str]:
        """
        Load endpoints from OpenAPI specification.

        Args:
            tracker: APIEndpointTracker instance
            openapi_spec: OpenAPI specification dictionary

        Returns:
            List[str]: List of endpoint IDs that were added
        """
        endpoint_ids = []
        paths = openapi_spec.get("paths", {})

        for path, path_item in paths.items():
            for method, operation in path_item.items():
                if method.lower() in [
                    "get",
                    "post",
                    "put",
                    "delete",
                    "patch",
                    "head",
                    "options",
                ]:
                    endpoint_id = self.add_endpoint(
                        path=path,
                        method=method,
                        summary=operation.get("summary"),
                        description=operation.get("description"),
                        parameters=operation.get("parameters"),
                        request_body=operation.get("requestBody"),
                        responses=operation.get("responses"),
                        tags=operation.get("tags"),
                    )
                    endpoint_ids.append(endpoint_id)

        return endpoint_ids


# Convenience functions for common operations
def create_tracker(storage_file: Optional[str] = None) -> APIEndpointTracker:
    """Create a new API endpoint tracker instance."""
    return APIEndpointTracker(storage_file)
