module.exports = {
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  testEnvironment: 'jsdom',
  transform: {
    '^.+\\.(js|jsx)$': 'babel-jest',
  },
  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    '\\.(gif|ttf|eot|svg|png)$': '<rootDir>/__mocks__/fileMock.js',
    '^\.\./context/AuthContext$': '<rootDir>/src/context/AuthContext.js',
    '^\.\./context/AuthContext.js$': '<rootDir>/src/context/AuthContext.js',
    '^\.\./context/AuthContext$': '<rootDir>/src/context/AuthContext.js',
    '^\.\./context/AuthContext.js$': '<rootDir>/src/context/AuthContext.js',
    '^../context/AuthContext$': '<rootDir>/src/context/AuthContext.js',
    '^../context/AuthContext.js$': '<rootDir>/src/context/AuthContext.js',
    '^\.\./context/AuthContext$': '<rootDir>/src/context/AuthContext.js',
    '^\.\./context/AuthContext.js$': '<rootDir>/src/context/AuthContext.js',
  },
};
