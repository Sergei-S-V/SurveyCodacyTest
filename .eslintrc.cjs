module.exports = {
  root: true,
  extends: [
    "plugin:react/recommended",
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:@typescript-eslint/recommended-type-checked",
  ],
  parser: "@typescript-eslint/parser",
  parserOptions: {
    // project: path.join(__dirname, "tsconfig.json"),
    project: "./frontend/tsconfig.json",
    tsconfigRootDir: __dirname,
    // tsconfigRootDir: path.resolve(__dirname, "."),
  },
  plugins: ["@typescript-eslint"],
  env: {
    browser: true,
    es2021: true,
  },
  rules: {
    "react/react-in-jsx-scope": "off",
    "react/jsx-uses-react": "off",
    "no-unused-vars": "off",
    "@typescript-eslint/no-unused-vars": "error",
  },
  settings: {
    react: {
      version: "detect", // Automatically detect the React version
    },
  },
};
