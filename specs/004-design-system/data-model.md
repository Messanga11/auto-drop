# Data Model: Design System Implementation

**Feature**: 004-design-system  
**Date**: 2024-12-19

## Overview

Cette feature n'introduit pas de nouvelles entités de données dans la base de données. Elle se concentre sur la création d'un système de tokens de design et la migration des composants UI existants. Ce document décrit les structures de tokens et les interfaces des composants.

## Design Tokens Structure

### Typography Tokens

**Source**: `design.json.typography`

```typescript
interface TypographyTokens {
  family: 'Inter';
  weights: {
    extraLight: 200;
    light: 300;
    regular: 400;
    medium: 500;
  };
  titles: {
    xl: { size: 88; weight: 'extraLight'; tracking: -2 };
    lg: { size: 54; weight: 'light' };
    md: { size: 32; weight: 'regular' };
    sm: { size: 20; weight: 'medium' };
  };
  body: {
    regular: { size: 18; weight: 'light' };
    small: { size: 14; weight: 'regular' };
  };
}
```

**Mapping Tailwind**:
- `fontFamily.sans`: 'Inter'
- `fontWeight`: 200, 300, 400, 500
- `fontSize`: 88px, 54px, 32px, 20px, 18px, 14px
- `letterSpacing`: -2px pour title.xl

### Color Tokens

**Source**: `design.json.colors`

```typescript
interface ColorTokens {
  primary: '#FF7335';
  primaryGradient: {
    from: '#FF6A00';
    to: '#FF3B2E';
    direction: 'diagonal';
  };
  background: {
    light: '#F5F6F7';
    dark: '#0C0C0C';
    card: 'rgba(255,255,255,0.15)';
    glass: 'rgba(255,255,255,0.20)';
    glassDark: 'rgba(0,0,0,0.25)';
  };
  text: {
    primary: '#FFFFFF';
    secondary: 'rgba(255,255,255,0.75)';
    dark: '#111111';
    muted: 'rgba(0,0,0,0.5)';
  };
  accent: {
    blue: '#9DB5C8';
    green: '#7FE0B3';
    red: '#FF6E5E';
    beige: '#C7A488';
    grey: '#8F9AA3';
    black: '#000000';
  };
}
```

**Mapping Tailwind**:
- `colors.primary`: '#FF7335'
- `colors.background.*`: Toutes les variantes
- `colors.text.*`: Toutes les variantes
- `colors.accent.*`: Toutes les variantes

### Spacing Tokens

**Source**: `design.json.layout.padding` et `design.json.layout.gridGap`

```typescript
interface SpacingTokens {
  padding: {
    screen: 48;
    section: 32;
    card: 24;
    component: 16;
  };
  gridGap: 32;
  maxWidth: 1600;
}
```

**Mapping Tailwind**:
- `spacing`: 16px, 24px, 32px, 48px
- `maxWidth`: 1600px

### Border Radius Tokens

**Source**: `design.json.radii`

```typescript
interface RadiusTokens {
  xs: 8;
  sm: 14;
  md: 22;
  lg: 32;
  xl: 48;
  xxl: 60;
  full: 999;
}
```

**Mapping Tailwind**:
- `borderRadius`: 8px, 14px, 22px, 32px, 48px, 60px, 999px

### Shadow Tokens

**Source**: `design.json.shadows`

```typescript
interface ShadowTokens {
  soft: '0 4px 32px rgba(0,0,0,0.25)';
  strong: '0 8px 48px rgba(0,0,0,0.35)';
  innerGlow: 'inset 0 0 32px rgba(255,255,255,0.1)';
}
```

**Mapping Tailwind**:
- `boxShadow`: soft, strong, innerGlow (custom)

### Blur Tokens

**Source**: `design.json.blur`

```typescript
interface BlurTokens {
  glassStrong: 45;
  card: 25;
  backgroundFog: 80;
}
```

**Mapping Tailwind**:
- `backdropBlur`: 25px, 45px, 80px (custom)

### Component-Specific Tokens

#### Button Tokens

**Source**: `design.json.buttons`

```typescript
interface ButtonTokens {
  default: {
    radius: 30;
    paddingX: 22;
    paddingY: 12;
    fontWeight: 400;
    background: 'rgba(255,255,255,0.15)';
    hoverBackground: 'rgba(255,255,255,0.25)';
  };
  tag: {
    radius: 20;
    paddingX: 16;
    paddingY: 6;
    inactiveBg: 'rgba(255,255,255,0.12)';
    activeBg: '#000000';
    activeText: '#FFFFFF';
  };
}
```

#### Card Tokens

**Source**: `design.json.cards`

```typescript
interface CardTokens {
  glass: {
    background: 'rgba(255,255,255,0.20)';
    blur: 40;
    radius: 32;
    shadow: '0 8px 48px rgba(0,0,0,0.3)';
  };
  stat: {
    radius: 28;
    padding: 20;
    background: 'rgba(0,0,0,0.35)';
  };
}
```

#### Navbar Tokens

**Source**: `design.json.navbar`

```typescript
interface NavbarTokens {
  height: 68;
  blur: 25;
  background: 'rgba(0,0,0,0.30)';
  avatarSize: 42;
  iconStyle: {
    stroke: 1.6;
    color: '#FFFFFF';
  };
}
```

## Component Interfaces

### Atom Components

#### Button Component

```typescript
interface ButtonProps {
  variant?: 'default' | 'tag';
  size?: 'sm' | 'md' | 'lg';
  state?: 'active' | 'inactive';
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  className?: string;
}
```

#### Input Component

```typescript
interface InputProps {
  type?: 'text' | 'email' | 'number' | 'date';
  placeholder?: string;
  value?: string;
  onChange?: (value: string) => void;
  error?: string;
  className?: string;
}
```

#### Badge Component

```typescript
interface BadgeProps {
  variant?: 'default' | 'tag';
  state?: 'active' | 'inactive';
  children: React.ReactNode;
  className?: string;
}
```

### Molecule Components

#### Card Component

```typescript
interface CardProps {
  variant?: 'glass' | 'stat';
  children: React.ReactNode;
  className?: string;
}
```

#### Form Component

```typescript
interface FormProps {
  onSubmit: (data: Record<string, any>) => void;
  children: React.ReactNode;
  className?: string;
}
```

### Organism Components

#### Navbar Component

```typescript
interface NavbarProps {
  user?: User;
  onLogout?: () => void;
  items: NavItem[];
  className?: string;
}
```

## Token Access Patterns

### Via Tailwind Classes

```tsx
<button className="bg-primary text-white rounded-[30px] px-[22px] py-[12px]">
  Click me
</button>
```

### Via CSS Variables

```css
.custom-element {
  background-color: var(--color-primary);
  border-radius: var(--radius-lg);
}
```

### Via TypeScript Tokens

```typescript
import { tokens } from '@/design-system/tokens';

const primaryColor = tokens.colors.primary; // '#FF7335'
const cardRadius = tokens.radii.lg; // 32
```

## Validation Rules

- **Couleurs**: Doivent correspondre exactement aux valeurs hexadécimales/rgba (tolérance 0%)
- **Espacements**: Doivent correspondre exactement aux valeurs en pixels (tolérance 0px)
- **Radius**: Doivent correspondre exactement aux valeurs en pixels (tolérance 0px)
- **Typography**: Doivent utiliser la police Inter avec les poids et tailles exacts
- **Shadows**: Doivent correspondre exactement aux valeurs définies (tolérance 0px pour offsets et blur)
- **Blur**: Doivent correspondre exactement aux valeurs en pixels (tolérance 0px)

