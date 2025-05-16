# Product Requirements Document: BigQuery Text-to-SQL Microservice

## 1. Introduction

This document outlines requirements for a Python-based microservice API that converts natural language to BigQuery SQL queries. The service integrates with a Streamlit interface where queries are routed through a main LLM.

## 2. Goals and Non-Goals

### Goals
- Create a REST API converting natural language to BigQuery SQL
- Communicate with a separate Qwen3 model container
- Prioritize query accuracy over speed
- Allow schema information to be provided and updated
- Generate only SQL query strings without formatting/explanation

### Non-Goals
- SQL query execution
- Query explanation generation
- Result formatting
- UI development
- Main routing LLM implementation

## 3. System Architecture

### 3.1 Component Overview
- **REST API Layer**: FastAPI application exposing endpoints
- **Qwen3 Client**: Component to communicate with the separate Qwen3 container
- **Schema Manager**: Component to store and manage DB schema information
- **Query Validator**: Validates the generated SQL

## 4. API Design

### 4.1 Endpoints

#### `POST /api/v1/generate-sql`
- Converts natural language to SQL
- **Request Body**: Query text and optional context
- **Response**: SQL query string and confidence score

#### `PUT /api/v1/schema/{schema_name}`
- Uploads or updates a DDL schema file.
- **Path Parameter**: `schema_name` (e.g., 'my_database').
- **Request Body**: Plain text DDL content (e.g., `CREATE TABLE ...`).
- **Query Parameter**: `overwrite` (boolean, optional).
- **Response**: Success status message.

#### `GET /api/v1/schema/`
- Lists all available DDL schema files.
- **Response**: List of schema names (e.g., `["my_database.sql", "sales_schema.sql"]`).

#### `GET /api/v1/schema/{schema_name}`
- Retrieves the DDL content of a specific schema file.
- **Path Parameter**: `schema_name`.
- **Response**: Plain text DDL content.

#### `DELETE /api/v1/schema/{schema_name}`
- Deletes a specific DDL schema file.
- **Path Parameter**: `schema_name`.
- **Response**: Success status message.

#### `GET /api/v1/health`
- Health check endpoint
- **Response**: Service status information

## 5. Schema Management

### 5.1 Schema Format
- Store table definitions in BigQuery DDL format
- Include detailed descriptions for tables and columns
- Store sample data for better LLM context

### 5.2 Schema and Relationship Storage
- Store all schema components as Data Definition Language (DDL) statements within `.sql` files.
- These `.sql` files will reside in a dedicated `knowledge/` directory within the project.
- Relationships, if not part of the DDL (e.g., foreign keys), should be documented within the DDL comments or a separate conventions document.

### 5.3 Descriptions and Context
Each table and column should include:
- Purpose explanation
- Data characteristics
- Business meaning
- Usage patterns
- Constraints/limitations

## 6. LLM Integration

### 6.1 Qwen3 Container Communication
- Use Ollama to call Qwen3

### 6.2 Prompt Engineering Best Practices
- Include schema + relationships + descriptions
- Provide few-shot examples of NL-to-SQL conversions
- Use Chain-of-Thought prompting to improve reasoning
- Include BigQuery syntax guidance
- Specify common patterns for complex queries

## 7. Text-to-SQL Best Practices

### 7.1 Current Research Findings
- Schema-guided generation outperforms schema-free approaches
- Sequential processing (parse intent → identify entities → generate SQL) improves accuracy
- Error correction feedback loops enhance performance
- Constrained decoding toward valid SQL syntax reduces errors

### 7.2 Implementation Requirements
- Apply principles from Spider benchmark successful approaches
- Use techniques from recent text-to-SQL papers showing:
  - Explicit schema linking
  - SQL validation feedback loops
  - Pattern-matching for query templates

## 8. Error Handling and Validation

### 8.1 Input Validation
- Validate query text for minimum length and maximum token count
- Check for malicious inputs or SQL injection patterns
- Ensure schema exists before processing queries

### 8.2 SQL Validation
- Verify syntax correctness using BigQuery parser
- Confirm all referenced tables and columns exist in schema
- Validate BigQuery-specific syntax and functions
- Check query complexity and estimate execution cost

### 8.3 Error Response Standards
- Use consistent error codes and messages
- Include suggestions for query reformulation
- Log detailed error traces for debugging
- Return appropriate HTTP status codes (400, 500, etc.)

## 9. Containerization

### 9.1 API Container
- Base image: Python 3.11
- FastAPI and dependencies
- Environment variables for Qwen3 service connection

### 9.2 Qwen3 Container
- Separate container specification
- Communication protocol details
- Resource requirements

## 10. Testing Requirements

### 10.1 Unit Tests
- Test endpoint functionality with mocked LLM responses
- Verify DDL schema file storage (creation, update, deletion) and retrieval from the `knowledge/` directory.
- Test error handling for all expected failure modes
- Validate SQL parsing and verification

### 10.2 Integration Tests
- End-to-end testing with the Qwen3 container
- Test with various natural language query complexities
- Measure conversion accuracy against expected SQL
- Benchmark response times under different loads

### 10.3 Test Data
- Create test dataset covering common query patterns
- Include edge cases and complex queries
- Develop evaluation metrics for SQL accuracy
- Use real-world query examples where possible

## 11. Monitoring and Logging

### 11.1 Logging Requirements
- Log all API requests and responses
- Record processing time for each step
- Track LLM interaction details and token usage
- Store query patterns for future improvement

### 11.2 Monitoring Metrics
- Response time per query
- SQL generation success rate
- Error frequency by type
- Container resource utilization
- Inter-container communication latency

### 11.3 Alerting
- Set up alerts for service unavailability
- Monitor for degraded LLM performance
- Track unusual error patterns
- Alert on resource constraints

## 12. Development Milestones

### 12.1 Phase 1: Foundation (Week 1-2)
- Set up FastAPI framework with Python 3.11
- Implement basic endpoint structure
- Design schema storage using DDL `.sql` files in the `knowledge/` directory.
- Create communication protocol with Qwen3 container

### 12.2 Phase 2: Core Functionality (Week 3-4)
- Implement schema management
- Develop prompt engineering approach
- Create SQL validation components
- Build Qwen3 client interface

### 12.3 Phase 3: Testing and Refinement (Week 5-6)
- Develop comprehensive test suite
- Optimize prompt templates
- Implement performance improvements
- Add monitoring and logging

### 12.4 Phase 4: Deployment and Documentation (Week 7-8)
- Containerize the application
- Create deployment documentation
- Conduct performance testing
- Prepare handover documentation

## 13. Acceptance Criteria
- Accurately converts natural language to valid BigQuery SQL
- Properly stores and utilizes schema with descriptions and relationships
- Successfully communicates with separate Qwen3 container
- Handles errors gracefully
- Meets performance requirements under load

## 14. Future Considerations

### 14.1 Functionality Enhancements
- Support for additional database types beyond BigQuery
- Implementation of SQL execution capabilities
- Query explanation generation
- Historical query caching for performance

### 14.2 Technical Improvements
- Streaming response capability for long-running queries
- Advanced schema inference from sample data
- Feedback loop for improving conversion accuracy over time
- Fine-tuned custom model specific to the organization's query patterns

### 14.3 Integration Opportunities
- Direct integration with BI tools
- Extension to other data sources beyond SQL
- Automated schema updates from database changes
- User feedback collection for continuous improvement