// /** @type {import('tailwindcss').Config} */
// module.exports = {
//   content: ["./src/**/*.{html,js}"],
//   theme: {
//     extend: {},
//   },
//   plugins: [],
// }


/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./templates/**/*.html",
        "./**/templates/**/*.html",
        "./static/**/*.js",
        "./**/static/**/*.js",
    ],
    theme: {
        extend: {},
    },
    plugins: [],
};

