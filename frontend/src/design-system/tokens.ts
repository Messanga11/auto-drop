/**
 * Design System Tokens
 * 
 * Centralized design tokens exported from design.json
 * These tokens are the single source of truth for all design values.
 */

// Import design.json using require for Node.js compatibility
// This works in both Node.js (for Tailwind config) and browser contexts
let designJson: any;
if (typeof window === 'undefined') {
  // Node.js environment (Tailwind config, build time)
  const fs = require('fs');
  const path = require('path');
  // Resolve from process.cwd() (project root) to find design.json
  const designJsonPath = path.resolve(process.cwd(), 'design.json');
  designJson = JSON.parse(fs.readFileSync(designJsonPath, 'utf8'));
} else {
  // Browser environment - tokens should be available via CSS variables
  // For now, we'll use a fallback or fetch if needed
  designJson = {} as any;
}

// Type definitions for design tokens
export interface TypographyTokens {
  family: string;
  weights: {
    extraLight: number;
    light: number;
    regular: number;
    medium: number;
  };
  titles: {
    xl: { size: number; weight: string; tracking?: number };
    lg: { size: number; weight: string };
    md: { size: number; weight: string };
    sm: { size: number; weight: string };
  };
  body: {
    regular: { size: number; weight: string };
    small: { size: number; weight: string };
  };
}

export interface ColorTokens {
  primary: string;
  primaryGradient: {
    from: string;
    to: string;
    direction: string;
  };
  background: {
    light: string;
    dark: string;
    card: string;
    glass: string;
    glassDark: string;
  };
  text: {
    primary: string;
    secondary: string;
    dark: string;
    muted: string;
  };
  accent: {
    blue: string;
    green: string;
    red: string;
    beige: string;
    grey: string;
    black: string;
  };
}

export interface SpacingTokens {
  padding: {
    screen: number;
    section: number;
    card: number;
    component: number;
  };
  gridGap: number;
  maxWidth: number;
}

export interface RadiusTokens {
  xs: number;
  sm: number;
  md: number;
  lg: number;
  xl: number;
  xxl: number;
  full: number;
}

export interface ShadowTokens {
  soft: string;
  strong: string;
  innerGlow: string;
}

export interface BlurTokens {
  glassStrong: number;
  card: number;
  backgroundFog: number;
}

export interface ButtonTokens {
  default: {
    radius: number;
    paddingX: number;
    paddingY: number;
    fontWeight: number;
    background: string;
    hoverBackground: string;
  };
  tag: {
    radius: number;
    paddingX: number;
    paddingY: number;
    inactiveBg: string;
    activeBg: string;
    activeText: string;
  };
}

export interface CardTokens {
  glass: {
    background: string;
    blur: number;
    radius: number;
    shadow: string;
  };
  stat: {
    radius: number;
    padding: number;
    background: string;
  };
}

export interface NavbarTokens {
  height: number;
  blur: number;
  background: string;
  avatarSize: number;
  iconStyle: {
    stroke: number;
    color: string;
  };
}

// Export all tokens
export const typography: TypographyTokens = designJson.typography || {
  family: 'Inter',
  weights: { extraLight: 200, light: 300, regular: 400, medium: 500 },
  titles: { xl: { size: 88, weight: 'extraLight', tracking: -2 }, lg: { size: 54, weight: 'light' }, md: { size: 32, weight: 'regular' }, sm: { size: 20, weight: 'medium' } },
  body: { regular: { size: 18, weight: 'light' }, small: { size: 14, weight: 'regular' } },
};

export const colors: ColorTokens = designJson.colors || {
  primary: '#FF7335',
  primaryGradient: { from: '#FF6A00', to: '#FF3B2E', direction: 'diagonal' },
  background: { light: '#F5F6F7', dark: '#0C0C0C', card: 'rgba(255,255,255,0.15)', glass: 'rgba(255,255,255,0.20)', glassDark: 'rgba(0,0,0,0.25)' },
  text: { primary: '#FFFFFF', secondary: 'rgba(255,255,255,0.75)', dark: '#111111', muted: 'rgba(0,0,0,0.5)' },
  accent: { blue: '#9DB5C8', green: '#7FE0B3', red: '#FF6E5E', beige: '#C7A488', grey: '#8F9AA3', black: '#000000' },
};

export const spacing: SpacingTokens = designJson.layout ? {
  padding: {
    screen: designJson.layout.padding.screen,
    section: designJson.layout.padding.section,
    card: designJson.layout.padding.card,
    component: designJson.layout.padding.component,
  },
  gridGap: designJson.layout.gridGap,
  maxWidth: designJson.layout.maxWidth,
} : {
  padding: { screen: 48, section: 32, card: 24, component: 16 },
  gridGap: 32,
  maxWidth: 1600,
};

export const radii: RadiusTokens = designJson.radii || {
  xs: 8, sm: 14, md: 22, lg: 32, xl: 48, xxl: 60, full: 999,
};

export const shadows: ShadowTokens = designJson.shadows || {
  soft: '0 4px 32px rgba(0,0,0,0.25)',
  strong: '0 8px 48px rgba(0,0,0,0.35)',
  innerGlow: 'inset 0 0 32px rgba(255,255,255,0.1)',
};

export const blur: BlurTokens = designJson.blur || {
  glassStrong: 45,
  card: 25,
  backgroundFog: 80,
};

export const buttons: ButtonTokens = designJson.buttons || {
  default: { radius: 30, paddingX: 22, paddingY: 12, fontWeight: 400, background: 'rgba(255,255,255,0.15)', hoverBackground: 'rgba(255,255,255,0.25)' },
  tag: { radius: 20, paddingX: 16, paddingY: 6, inactiveBg: 'rgba(255,255,255,0.12)', activeBg: '#000000', activeText: '#FFFFFF' },
};

export const cards: CardTokens = designJson.cards || {
  glass: { background: 'rgba(255,255,255,0.20)', blur: 40, radius: 32, shadow: '0 8px 48px rgba(0,0,0,0.3)' },
  stat: { radius: 28, padding: 20, background: 'rgba(0,0,0,0.35)' },
};

export const navbar: NavbarTokens = designJson.navbar || {
  height: 68,
  blur: 25,
  background: 'rgba(0,0,0,0.30)',
  avatarSize: 42,
  iconStyle: { stroke: 1.6, color: '#FFFFFF' },
};

// Convenience exports
export const tokens = {
  typography,
  colors,
  spacing,
  radii,
  shadows,
  blur,
  buttons,
  cards,
  navbar,
};

export default tokens;
