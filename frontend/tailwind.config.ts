import type { Config } from "tailwindcss";
import { tokens } from "./src/design-system/tokens";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/design-system/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      // Color tokens
      colors: {
        primary: tokens.colors.primary,
        "primary-gradient": {
          from: tokens.colors.primaryGradient.from,
          to: tokens.colors.primaryGradient.to,
        },
        background: {
          DEFAULT: "var(--background)",
          light: tokens.colors.background.light,
          dark: tokens.colors.background.dark,
          card: tokens.colors.background.card,
          glass: tokens.colors.background.glass,
          glassDark: tokens.colors.background.glassDark,
        },
        text: {
          primary: tokens.colors.text.primary,
          secondary: tokens.colors.text.secondary,
          dark: tokens.colors.text.dark,
          muted: tokens.colors.text.muted,
        },
        accent: {
          blue: tokens.colors.accent.blue,
          green: tokens.colors.accent.green,
          red: tokens.colors.accent.red,
          beige: tokens.colors.accent.beige,
          grey: tokens.colors.accent.grey,
          black: tokens.colors.accent.black,
        },
        // Keep existing for backward compatibility
        foreground: "var(--foreground)",
      },
      // Typography tokens
      fontFamily: {
        sans: [tokens.typography.family, "sans-serif"],
      },
      fontSize: {
        "title-xl": [`${tokens.typography.titles.xl.size}px`, { lineHeight: "1.2" }],
        "title-lg": [`${tokens.typography.titles.lg.size}px`, { lineHeight: "1.2" }],
        "title-md": [`${tokens.typography.titles.md.size}px`, { lineHeight: "1.2" }],
        "title-sm": [`${tokens.typography.titles.sm.size}px`, { lineHeight: "1.2" }],
        "body-regular": [`${tokens.typography.body.regular.size}px`, { lineHeight: "1.5" }],
        "body-small": [`${tokens.typography.body.small.size}px`, { lineHeight: "1.5" }],
      },
      fontWeight: {
        extraLight: tokens.typography.weights.extraLight.toString(),
        light: tokens.typography.weights.light.toString(),
        regular: tokens.typography.weights.regular.toString(),
        medium: tokens.typography.weights.medium.toString(),
      },
      letterSpacing: {
        "title-xl": `${tokens.typography.titles.xl.tracking}px`,
      },
      // Spacing tokens
      spacing: {
        screen: `${tokens.spacing.padding.screen}px`,
        section: `${tokens.spacing.padding.section}px`,
        card: `${tokens.spacing.padding.card}px`,
        component: `${tokens.spacing.padding.component}px`,
        gridGap: `${tokens.spacing.gridGap}px`,
      },
      maxWidth: {
        container: `${tokens.spacing.maxWidth}px`,
      },
      // Border radius tokens
      borderRadius: {
        xs: `${tokens.radii.xs}px`,
        sm: `${tokens.radii.sm}px`,
        md: `${tokens.radii.md}px`,
        lg: `${tokens.radii.lg}px`,
        xl: `${tokens.radii.xl}px`,
        xxl: `${tokens.radii.xxl}px`,
        full: `${tokens.radii.full}px`,
      },
      // Shadow tokens
      boxShadow: {
        soft: tokens.shadows.soft,
        strong: tokens.shadows.strong,
        "inner-glow": tokens.shadows.innerGlow,
      },
      // Blur tokens (backdrop-filter)
      backdropBlur: {
        "glass-strong": `${tokens.blur.glassStrong}px`,
        card: `${tokens.blur.card}px`,
        "background-fog": `${tokens.blur.backgroundFog}px`,
      },
    },
  },
  plugins: [
    // Custom plugin for glass effects
    function ({ addUtilities }: any) {
      addUtilities({
        ".glass-card": {
          background: tokens.cards.glass.background,
          "backdrop-filter": `blur(${tokens.cards.glass.blur}px)`,
          "border-radius": `${tokens.cards.glass.radius}px`,
          "box-shadow": tokens.cards.glass.shadow,
        },
        ".glass-strong": {
          "backdrop-filter": `blur(${tokens.blur.glassStrong}px)`,
        },
        ".gradient-overlay": {
          background: `linear-gradient(135deg, #FF6A00, #FF3E3E, #000000)`,
          opacity: 0.55,
          "mix-blend-mode": "overlay",
        },
      });
    },
  ],
};
export default config;
