"""Generate Fern x-fern-examples overrides from OpenAPI spec.

Reads openapi.json, builds realistic response examples for every endpoint
by walking the schema and pulling `examples` from each field definition.

Usage:
    python scripts/generate_overrides.py [--spec fern/openapi/openapi.json]
"""

import argparse
import json
from pathlib import Path

import yaml


def resolve_ref(spec: dict, ref: str) -> dict:
    """Resolve a $ref pointer like #/components/schemas/Foo."""
    parts = ref.lstrip("#/").split("/")
    node = spec
    for part in parts:
        node = node[part]
    return node


def is_nullable(schema: dict) -> bool:
    """Check if a schema allows null."""
    if "anyOf" in schema:
        return any(opt.get("type") == "null" for opt in schema["anyOf"])
    return False


def build_example(spec: dict, schema: dict, *, nullable_as_null: bool = False) -> object:
    """Recursively build an example value from a schema definition."""
    # Handle $ref
    if "$ref" in schema:
        resolved = resolve_ref(spec, schema["$ref"])
        # Check for examples on the ref wrapper first
        if "examples" in schema and schema["examples"]:
            return schema["examples"][0]
        return build_example(spec, resolved, nullable_as_null=nullable_as_null)

    # Use first example if available (check BEFORE anyOf/allOf)
    if "examples" in schema and schema["examples"]:
        return schema["examples"][0]
    if "example" in schema:
        return schema["example"]

    # Handle anyOf (nullable types, unions)
    if "anyOf" in schema:
        nullable = any(opt.get("type") == "null" for opt in schema["anyOf"])
        non_null = [opt for opt in schema["anyOf"] if opt.get("type") != "null"]
        if non_null:
            result = build_example(spec, non_null[0])
            return result
        return None

    # Handle allOf
    if "allOf" in schema:
        result = {}
        for sub in schema["allOf"]:
            val = build_example(spec, sub)
            if isinstance(val, dict):
                result.update(val)
        return result

    # Handle by type
    schema_type = schema.get("type")

    if schema_type == "object" or "properties" in schema:
        result = {}
        required = set(schema.get("required", []))
        for prop_name, prop_schema in schema.get("properties", {}).items():
            result[prop_name] = build_example(spec, prop_schema)
        return result

    if schema_type == "array":
        items = schema.get("items", {})
        item_example = build_example(spec, items)
        return [item_example] if item_example is not None else []

    # Enum
    if "enum" in schema:
        return schema["enum"][0]

    # Scalar defaults
    defaults = {
        "string": "string",
        "integer": 0,
        "number": 0.0,
        "boolean": True,
    }
    return defaults.get(schema_type)


def get_success_response_schema(spec: dict, operation: dict) -> dict | None:
    """Find the success response schema (200 or 201)."""
    for code in ("200", "201"):
        resp = operation.get("responses", {}).get(code, {})
        content = resp.get("content", {})
        json_content = content.get("application/json", {})
        if "schema" in json_content:
            return json_content["schema"]
    return None


def get_request_schema(spec: dict, operation: dict) -> dict | None:
    """Find the request body schema."""
    body = operation.get("requestBody", {})
    content = body.get("content", {})
    json_content = content.get("application/json", {})
    if "schema" in json_content:
        return json_content["schema"]
    return None


def build_path_params(path: str) -> dict | None:
    """Extract path parameters and give them example values."""
    import re
    params = re.findall(r"\{(\w+)\}", path)
    if not params:
        return None
    return {p: p for p in params}


def generate_overrides(spec: dict) -> dict:
    """Generate x-fern-examples overrides for all endpoints."""
    paths = {}

    for path, methods in sorted(spec.get("paths", {}).items()):
        path_overrides = {}

        for method in ("get", "post", "put", "patch", "delete"):
            if method not in methods:
                continue

            operation = methods[method]

            # Skip endpoints with no response body (like DELETE 204)
            response_schema = get_success_response_schema(spec, operation)
            if response_schema is None:
                continue

            example_entry = {}

            # Path parameters
            path_params = build_path_params(path)
            if path_params:
                example_entry["path-parameters"] = path_params

            # Request body example
            request_schema = get_request_schema(spec, operation)
            if request_schema:
                request_example = build_example(spec, request_schema)
                if request_example and isinstance(request_example, dict):
                    example_entry["request"] = request_example

            # Response body example
            response_example = build_example(spec, response_schema)
            if response_example is not None:
                example_entry["response"] = {"body": response_example}

            if example_entry.get("response"):
                path_overrides[method] = {
                    "x-fern-examples": [example_entry]
                }

        if path_overrides:
            paths[path] = path_overrides

    return {"paths": paths}


class CleanDumper(yaml.SafeDumper):
    """YAML dumper that produces clean output."""
    pass


def str_representer(dumper, data):
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


CleanDumper.add_representer(str, str_representer)


def main():
    parser = argparse.ArgumentParser(description="Generate Fern overrides from OpenAPI spec")
    parser.add_argument("--spec", default="fern/openapi/openapi.json", help="Path to OpenAPI spec")
    parser.add_argument("--output", default="fern/openapi/ai_examples_override.yml", help="Output path")
    args = parser.parse_args()

    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"Spec not found: {spec_path}")
        return

    with open(spec_path) as f:
        spec = json.load(f)

    overrides = generate_overrides(spec)

    with open(args.output, "w") as f:
        yaml.dump(overrides, f, Dumper=CleanDumper, default_flow_style=False, sort_keys=False, allow_unicode=True)

    # Count endpoints
    count = sum(len(methods) for methods in overrides["paths"].values())
    print(f"Generated overrides for {count} endpoints → {args.output}")


if __name__ == "__main__":
    main()
