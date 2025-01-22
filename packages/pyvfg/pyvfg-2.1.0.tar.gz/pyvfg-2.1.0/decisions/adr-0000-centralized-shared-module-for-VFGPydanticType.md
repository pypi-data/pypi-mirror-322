# **ADR: Centralized Shared Module for `VFGPydanticType`**

## **Status**
Proposed

---

## **Context**

The `VFGPydanticType` is a core structure used across multiple python repositories and components:

1. **`genius-agent-factor-graph (current repo)`**:
   - Defined in `python/pyvfg/pydantic.py` and used across files under `src/types/`.
2. **`gpil-pipeline (external repo)`**:
   - Specifically used in **FastAPI endpoints** within `packages/gpil-server/src/gpil_server/app.py` for APIs like:
     - `/graph` (GET and POST endpoints)
     - `/validate`
     - `/import`

This type integrates [Pydantic](https://docs.pydantic.dev/) validation with custom logic to handle **Verses Factor Graphs (VFG)**. The current state has a duplicated implementation of `VFGPydanticType` across the repositories. 

### **Current Challenges**
1. **Code Duplication**:
   - The `VFGPydanticType` logic exists in multiple places, requiring manual updates.
   - Changes (e.g., bug fixes, schema updates) need to be applied individually, increasing maintenance overhead.

2. **Inconsistency Risks**:
   - Any missed updates across repos can lead to inconsistencies in API behavior or validation rules.

3. **Testing Overhead**:
   - Each repo requires redundant unit tests for the same logic, increasing effort and slowing down development.

4. **Dependency Management**:
   - Both repositories depend on the same type and logic, but managing updates to shared code manually is inefficient.

5. **Scalability**:
   - As more projects or components require VFG integration, duplication will grow, exacerbating the issues above.

---

## **Decision**
We will extract `VFGPydanticType` and its supporting logic into a **centralized shared module** and distribute it as a **Python package**. The package will provide a single source of truth for `VFGPydanticType`, ensuring consistency and maintainability.

---

## **Details**

### **Implementation Steps**

1. **New Repository**:
   - Create a new GitHub repository: **`vfg-pydantic`**.
   - This repository will house the shared implementation of `VFGPydanticType` and related utilities.

   **Proposed File Structure**:
   ```
   vfg-pydantic/
   ├── vfg_pydantic/
   │   ├── __init__.py         # Expose package exports
   │   └── types.py            # Contains VFGPydanticType and supporting logic
   ├── tests/
   │   └── test_types.py       # Unit tests for validation and serialization
   ├── pyproject.toml          # Package metadata and dependencies
   ├── README.md               # Documentation
   └── .github/
       └── workflows/
           └── ci.yml          # CI for testing, building, and publishing
   ```

2. **Shared Module Content**:
   - Extract the following components from `genius-agent-factor-graph`:
     - `VFGPydanticType` (Pydantic annotation).
     - `_VFGPydanticAnnotation` (custom validation logic).
     - Supporting functions: `vfg_from_json`, `vfg_to_json`.
     - URLs for external schemas and examples:
       ```python
       VFG_SCHEMA_REF_URL = "https://<schema-url>"
       VFG_EXAMPLE_REF_URL = "https://<example-url>"
       ```
   **Proposed code for new `vfg_pydantic/types.py`**:
   ```python
    import json
    from typing import Annotated, Any

    from pydantic import Field, GetCoreSchemaHandler, GetJsonSchemaHandler
    from pydantic.json_schema import JsonSchemaValue
    from pydantic_core import core_schema

    # Import the VFG class and utility functions from pyvfg
    from pyvfg import VFG, vfg_from_json, vfg_to_json

    # External schema and example URLs
    VFG_SCHEMA_REF_URL = (
        "https://verses-json-schema-registry-gitops-usw1.s3.us-west-1.amazonaws.com/vfg/0_3_0/vfg_0_3_0.json"
    )
    VFG_EXAMPLE_REF_URL = (
        "https://verses-json-schema-registry-gitops-usw1.s3.us-west-1.amazonaws.com/vfg/examples/small/sprinkler_factor_graph_vfg.json"
    )

    # Fetch example JSON (used in the Field examples)
    try:
        import requests

        VFG_EXAMPLE_JSON = requests.get(VFG_EXAMPLE_REF_URL).json()
    except Exception as e:
        # Fallback to a placeholder if fetching the example fails
        VFG_EXAMPLE_JSON = {"error": f"Could not fetch example JSON: {e}"}


    class _VFGPydanticAnnotation:
        """
        Pydantic annotation class for the VFG type.
        This class customizes validation, serialization, and JSON schema generation for the VFG type.
        """

        @classmethod
        def __get_pydantic_core_schema__(
            cls, _source_type: Any, _handler: GetCoreSchemaHandler
        ) -> core_schema.CoreSchema:
            """
            Define validation and serialization behavior for the VFG type.
            """

            def validate_from_str(value: str) -> VFG:
                # Ensure the string is valid JSON, then parse it into a VFG instance
                json.loads(value)  # Raises ValueError if the string is not valid JSON
                return vfg_from_json(value)

            def validate_from_dict(value: dict[str, Any]) -> VFG:
                # Convert a Python dictionary to JSON, then parse it into a VFG instance
                return vfg_from_json(json.dumps(value))

            def serialize(instance: VFG) -> str:
                # Serialize a VFG instance into a JSON string
                return json.loads(vfg_to_json(instance))

            from_str_schema = core_schema.chain_schema(
                [
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(validate_from_str),
                ]
            )

            from_dict_schema = core_schema.chain_schema(
                [
                    core_schema.dict_schema(),
                    core_schema.no_info_plain_validator_function(validate_from_dict),
                ]
            )

            return core_schema.json_or_python_schema(
                json_schema=from_dict_schema,
                python_schema=core_schema.union_schema(
                    [
                        core_schema.is_instance_schema(VFG),  # Accept existing VFG instances
                        from_str_schema,  # Accept JSON strings
                        from_dict_schema,  # Accept Python dictionaries
                    ]
                ),
                serialization=core_schema.plain_serializer_function_ser_schema(serialize),
            )

        @classmethod
        def __get_pydantic_json_schema__(
            cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
        ) -> JsonSchemaValue:
            """
            Return an external reference to the VFG schema URL.
            This is used to link the JSON schema for OpenAPI documentation and validation.
            """
            return {"$ref": VFG_SCHEMA_REF_URL}


    # Define the reusable Pydantic-compatible type for VFG
    VFGPydanticType = Annotated[
        VFG,
        _VFGPydanticAnnotation,
        Field(
            ...,
            examples=[VFG_EXAMPLE_JSON],  # Example usage of the type
        ),
    ]
   ```

   - Include clear **unit tests** for:
     - Validation of JSON strings and dictionaries.
     - Serialization into JSON strings.
     - Example payload validation.

3. **Package Publishing**:
   - Publish the shared module to **PyPI** or **GitHub Packages** using semantic versioning (`v1.0.0`, `v1.1.0`, etc.).
   - Use GitHub Actions for automated CI/CD workflows:
     - Run tests on pull requests and pushes.
     - Publish the package on versioned tags.

4. **Integration into Dependent Repositories**:
   - Replace local implementations of `VFGPydanticType` in:
     - `genius-agent-factor-graph`.
     - `gpil-pipeline` (FastAPI `app.py` and related files).

   **Updated Imports**:
   ```python
   from vfg_pydantic.types import VFGPydanticType
   ```

   - Add the shared module as a dependency:
     - `requirements.txt` or `pyproject.toml`:
       ```
       vfg-pydantic==1.0.0
       ```

5. **Testing and Validation**:
   - Run end-to-end tests in both repositories after integration.
   - Ensure the FastAPI endpoints in `gpil-pipeline` correctly validate and serialize `VFG` data using the shared module.

---

### **Benefits**

1. **Single Source of Truth**:
   - A centralized implementation ensures consistency across all repositories.

2. **Simplified Maintenance**:
   - Bug fixes and updates are applied in one place and propagate automatically through version updates.

3. **Improved Developer Productivity**:
   - Reduces duplication of effort for testing, documentation, and validation logic.

4. **Scalability**:
   - New repositories or projects can easily integrate `VFGPydanticType` by adding the shared module as a dependency.

5. **Controlled Updates**:
   - Semantic versioning allows dependent projects to control when they upgrade to newer versions.

---

### **Trade-offs**

1. **Initial Overhead**:
   - Creating and publishing the new package requires effort.
   - **Mitigation**: Use GitHub Actions to automate CI/CD.

2. **Dependency Management**:
   - Projects must update their dependencies to adopt the shared module.
   - **Mitigation**: Provide clear upgrade instructions and ensure backward compatibility.

---

### **Consequences**

1. **Positive Outcomes**:
   - Consistent `VFGPydanticType` usage across `genius-agent-factor-graph` and `gpil-pipeline`.
   - Easier onboarding for new developers or projects.

2. **Negative Outcomes**:
   - If the shared module introduces bugs, all dependent repositories may be affected.
   - **Mitigation**: Implement comprehensive unit tests and versioning.

---

## **Work Items and Timeline**

| **Task**                          | **Owner**           | **Deadline**   |
|-----------------------------------|---------------------|----------------|
| Create `vfg-pydantic` repository  | DevOps         | TBD   |
| Extract and refactor code         | Python Dev   | TBD   |
| Add CI/CD pipelines               | DevOps         | TBD   |
| Publish version `v1.0.0`          | DevOps         | TBD    |
| Integrate shared module in `gpil` | Python Dev   | TBD   |
| Integrate shared module in `genius-agent-factor-graph` | Python Dev | TBD |
