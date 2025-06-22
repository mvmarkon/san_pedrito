module.exports = {
  root: true,
  env: {
    browser: true,
    es2020: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
    'plugin:react/recommended',
    'plugin:react/jsx-runtime',
    'plugin:prettier/recommended',
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs', 'postcss.config.js', 'tailwind.config.js', 'vite.config.ts'],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    project: ['./tsconfig.json', './tsconfig.node.json'],
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
  plugins: [
    'react-refresh',
    '@typescript-eslint',
    'simple-import-sort',
    'react',
    'prettier',
  ],
  rules: {
    'react-refresh/only-export-components': 'off',
    '@typescript-eslint/no-unused-vars': [
      'warn',
      { argsIgnorePattern: '^_', varsIgnorePattern: '^(React|Outlet)$' },
    ],
    'simple-import-sort/imports': [
      'error',
      {
        groups: [
          ['^react$', '^react-dom$', '^react-router-dom$'],
          ['^@?\w'],
          ['^(@|components)(/.*|$)', '^(@|lib)(/.*|$)', '^(@|pages)(/.*|$)', '^(@|hooks)(/.*|$)', '^(@|utils)(/.*|$)', '^(@|types)(/.*|$)', '^(@|constants)(/.*|$)', '^(@|context)(/.*|$)', '^(@|services)(/.*|$)', '^(@|store)(/.*|$)', '^(@|styles)(/.*|$)', '^(@|assets)(/.*|$)', '^(@|config)(/.*|$)', '^(@|data)(/.*|$)', '^(@|helpers)(/.*|$)', '^(@|mocks)(/.*|$)', '^(@|routes)(/.*|$)', '^(@|theme)(/.*|$)', '^(@|validation)(/.*|$)', '^(@|views)(/.*|$)', '^(@|workers)(/.*|$)', '^(@|api)(/.*|$)', '^(@|auth)(/.*|$)', '^(@|forms)(/.*|$)', '^(@|i18n)(/.*|$)', '^(@|layouts)(/.*|$)', '^(@|navigation)(/.*|$)', '^(@|providers)(/.*|$)', '^(@|schemas)(/.*|$)', '^(@|tests)(/.*|$)', '^(@|ui)(/.*|$)', '^(@|widgets)(/.*|$)', '^(@|models)(/.*|$)', '^(@|enums)(/.*|$)', '^(@|interfaces)(/.*|$)', '^(@|decorators)(/.*|$)', '^(@|mixins)(/.*|$)', '^(@|modules)(/.*|$)', '^(@|plugins)(/.*|$)', '^(@|templates)(/.*|$)', '^(@|themes)(/.*|$)', '^(@|validators)(/.*|$)', '^(@|vendor)(/.*|$)', '^(@|web)(/.*|$)', '^(@|workers)(/.*|$)', '^(@|zod)(/.*|$)',
          ],
          ['^\.'],
          ['^\u0000'],
          ['^.+\u0000$'],
        ],
      },
    ],
    'simple-import-sort/exports': 'error',
    'indent': 'off',
    'linebreak-style': ['error', 'unix'],
    'quotes': ['error', 'single'],
    'semi': ['error', 'always'],
    'react/react-in-jsx-scope': 'off',
    'react/prop-types': 'off',
    'prettier/prettier': 'error',
  },
};