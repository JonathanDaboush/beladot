module.exports = {
  testEnvironment: 'jsdom',
  collectCoverage: true,
  coverageDirectory: '<rootDir>/build/coverage',
  coverageReporters: ['text', 'lcov'],
  collectCoverageFrom: [
    '<rootDir>/src/**/*.{js,jsx}',
    '!<rootDir>/src/index.js',
    '!<rootDir>/src/reportWebVitals.js',
    '!<rootDir>/src/pages/**',
  ],
  coveragePathIgnorePatterns: ['<rootDir>/src/pages/'],
  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    '\\.(gif|ttf|eot|svg|png)$': '<rootDir>/__mocks__/fileMock.js',
  },
};
