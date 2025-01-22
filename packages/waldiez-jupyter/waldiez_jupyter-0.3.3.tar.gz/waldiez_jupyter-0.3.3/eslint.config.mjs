import eslint from "@eslint/js";
import stylistic from "@stylistic/eslint-plugin";
import eslintPluginPrettierRecommended from "eslint-plugin-prettier/recommended";
import eslintTs from "typescript-eslint";

// export default eslintTs.config({
const defaultConfig = eslintTs.config({
    extends: [eslint.configs.recommended, ...eslintTs.configs.recommended, eslintPluginPrettierRecommended],
    ignores: ["node_modules", "dist", "public", ".local", "**/assets/**"],
    plugins: {
        "@stylistic": stylistic,
    },
    // no overrides in flat config
    // overrides: [
    //     {
    //         files: ['*spec.ts', '*spec.tsx'],
    //         plugins: ['jest'],
    //         extends: ['plugin:jest/recommended'],
    //         rules: {
    //             'jest/expect-expect': 'off'
    //         }
    //     }
    // ],
    rules: {
        "prettier/prettier": [
            "error",
            {
                tabWidth: 4,
                printWidth: 110,
                arrowParens: "avoid",
                bracketSpacing: true,
                singleQuote: false,
                trailingComma: "all",
                endOfLine: "lf",
            },
        ],
        "@typescript-eslint/naming-convention": [
            "error",
            {
                selector: "interface",
                format: ["PascalCase"],
                custom: {
                    regex: "^I[A-Z]",
                    match: true,
                },
            },
        ],
        "no-unused-vars": "off",
        "@typescript-eslint/no-unused-vars": [
            "error",
            {
                args: "all",
                argsIgnorePattern: "^_",
                varsIgnorePattern: "^_",
                caughtErrorsIgnorePattern: "^_",
            },
        ],
        "@typescript-eslint/no-explicit-any": "off",
        "@typescript-eslint/no-namespace": "off",
        "@typescript-eslint/no-unused-expressions": "off",
        "@typescript-eslint/no-use-before-define": "off",
        "@stylistic/no-explicit-any": "off",
        "@stylistic/no-trailing-spaces": "off",
        "@stylistic/padded-blocks": "off",
        "@stylistic/function-paren-newline": "off",
        "@stylistic/no-use-before-define": "off",
        "@stylistic/quotes": [
            "error",
            "double",
            {
                avoidEscape: true,
                allowTemplateLiterals: false,
            },
        ],
        curly: ["error", "all"],
        eqeqeq: "error",
        "prefer-arrow-callback": "error",
    },
});

export default [
    ...defaultConfig,
    // overrides
    ...defaultConfig.map(config => ({
        ...config,
        files: ["*spec.ts", "*spec.tsx"],
        plugins: ["jest"],
        extends: ["plugin:jest/recommended"],
        rules: {
            ...config.rules,
            "jest/expect-expect": "off",
        },
    })),
];
