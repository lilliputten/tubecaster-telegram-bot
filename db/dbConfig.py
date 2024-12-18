TEST_DATABASE_URL = 'file:.data-test.db'

testEnv = {
    'DATABASE_URL': TEST_DATABASE_URL,
}

__all__ = [
    'TEST_DATABASE_URL',
    'testEnv',
]
