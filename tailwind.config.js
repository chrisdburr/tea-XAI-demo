/** @type {import('tailwindcss').Config} */
module.exports = {
	darkMode: "class",
	content: [
		"./templates/**/*.html",
		"./api/templates/**/*.html",
		"./api/views/**/*.py",
		// Add other paths where Tailwind classes are used
	],
	theme: {
		extend: {
			colors: {
				primary: "#1E40AF", // Example custom color
				secondary: "#64748B",
			},
			fontFamily: {
				sans: ["Inter", "sans-serif"], // Example custom font
			},
		},
	},
	plugins: [
		require("@tailwindcss/forms"),
		require("@tailwindcss/typography"),
	],
};

