# Testing Suite for Inventory Management System

This directory contains comprehensive tests for the Inventory Management System.

## Test Structure

- `test_models.py` - Tests for database models and CRUD operations
- `test_auth.py` - Tests for authentication and user management
- `test_validators.py` - Tests for input validation functions
- `run_all_tests.py` - Script to run all tests at once

## Running Tests

### Run All Tests
```bash
python tests/run_all_tests.py
```

### Run Individual Test Files
```bash
python -m unittest tests.test_models
python -m unittest tests.test_auth
python -m unittest tests.test_validators
```

### Run Specific Test Methods
```bash
python -m unittest tests.test_models.TestDatabaseModels.test_add_item
python -m unittest tests.test_auth.TestAuthentication.test_create_user
```

## Test Coverage

### Database Models (`test_models.py`)
- ✅ Add, update, delete inventory items
- ✅ Category management
- ✅ Supplier management
- ✅ Transaction logging
- ✅ Foreign key relationships

### Authentication (`test_auth.py`)
- ✅ User creation and validation
- ✅ Password hashing and verification
- ✅ User authentication
- ✅ Duplicate user prevention
- ✅ Role-based access

### Validators (`test_validators.py`)
- ✅ Username validation
- ✅ Password validation
- ✅ Item data validation
- ✅ Quantity and price validation

## Test Features

### Isolated Testing
- Each test runs with a temporary database
- Tests don't affect your production data
- Automatic cleanup after each test

### Comprehensive Coverage
- Happy path scenarios
- Error conditions
- Edge cases
- Invalid inputs

### Mock Data
- Uses temporary SQLite databases
- No external dependencies
- Fast execution

## Adding New Tests

1. Create test methods starting with `test_`
2. Use descriptive test names
3. Test both success and failure cases
4. Follow the AAA pattern (Arrange, Act, Assert)

Example:
```python
def test_feature_name(self):
    """Test description of what this test covers"""
    # Arrange - Set up test data
    # Act - Call the function being tested
    # Assert - Verify the result
```

## Continuous Integration

These tests can be integrated with CI/CD pipelines to ensure code quality:
- GitHub Actions
- GitLab CI/CD
- Jenkins
- Travis CI

## Best Practices

1. **Run tests before committing code**
2. **Write tests for new features**
3. **Keep tests independent**
4. **Use descriptive test names**
5. **Test edge cases and error conditions**
