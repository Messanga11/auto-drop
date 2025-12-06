# Design Tokens Contract

**Feature**: 004-design-system  
**Date**: 2024-12-19

## Contract Definition

Ce document définit le contrat pour l'accès et l'utilisation des tokens de design dans l'application.

## Token Categories

### 1. Typography Tokens

**Access Pattern**: 
- Tailwind: `text-{size}`, `font-{weight}`, `tracking-{value}`
- CSS Variable: `var(--font-size-{name})`, `var(--font-weight-{name})`
- TypeScript: `tokens.typography.{category}.{name}`

**Required Tokens**:
- Family: Inter
- Weights: 200 (extraLight), 300 (light), 400 (regular), 500 (medium)
- Title sizes: xl (88px), lg (54px), md (32px), sm (20px)
- Body sizes: regular (18px), small (14px)
- Tracking: -2px pour title.xl

### 2. Color Tokens

**Access Pattern**:
- Tailwind: `bg-{color}`, `text-{color}`, `border-{color}`
- CSS Variable: `var(--color-{name})`
- TypeScript: `tokens.colors.{category}.{name}`

**Required Tokens**:
- Primary: #FF7335
- Primary Gradient: from #FF6A00, to #FF3B2E
- Background: light, dark, card, glass, glassDark
- Text: primary, secondary, dark, muted
- Accent: blue, green, red, beige, grey, black

### 3. Spacing Tokens

**Access Pattern**:
- Tailwind: `p-{size}`, `px-{size}`, `py-{size}`, `gap-{size}`
- CSS Variable: `var(--spacing-{name})`
- TypeScript: `tokens.spacing.{name}`

**Required Tokens**:
- Padding: screen (48px), section (32px), card (24px), component (16px)
- Gap: gridGap (32px)
- MaxWidth: 1600px

### 4. Border Radius Tokens

**Access Pattern**:
- Tailwind: `rounded-{size}`
- CSS Variable: `var(--radius-{name})`
- TypeScript: `tokens.radii.{name}`

**Required Tokens**:
- xs (8px), sm (14px), md (22px), lg (32px), xl (48px), xxl (60px), full (999px)

### 5. Shadow Tokens

**Access Pattern**:
- Tailwind: `shadow-{name}` (custom)
- CSS Variable: `var(--shadow-{name})`
- TypeScript: `tokens.shadows.{name}`

**Required Tokens**:
- soft, strong, innerGlow

### 6. Blur Tokens

**Access Pattern**:
- Tailwind: `backdrop-blur-{name}` (custom)
- CSS Variable: `var(--blur-{name})`
- TypeScript: `tokens.blur.{name}`

**Required Tokens**:
- glassStrong (45px), card (25px), backgroundFog (80px)

## Component-Specific Contracts

### Button Contract

**Required Properties**:
- Default variant: radius 30px, paddingX 22px, paddingY 12px, background glass, hoverBackground
- Tag variant: radius 20px, paddingX 16px, paddingY 6px, states (active/inactive)

### Card Contract

**Required Properties**:
- Glass variant: background rgba(255,255,255,0.20), blur 40px, radius 32px, shadow
- Stat variant: radius 28px, padding 20px, background rgba(0,0,0,0.35)

### Navbar Contract

**Required Properties**:
- Height: 68px
- Blur: 25px
- Background: rgba(0,0,0,0.30)
- Avatar size: 42px
- Icon style: stroke 1.6px, color #FFFFFF

## Validation Contract

Tous les tokens DOIVENT:
1. Correspondre exactement aux valeurs de design.json (tolérance 0px/0%)
2. Être accessibles via au moins 2 méthodes (Tailwind + CSS Variables ou TypeScript)
3. Être documentés avec leur valeur exacte
4. Être testables visuellement pour vérifier la conformité

## Extension Contract

Pour ajouter de nouveaux tokens:
1. Ajouter la valeur dans design.json (source de vérité)
2. Exposer via Tailwind config
3. Exposer via CSS Variables
4. Exposer via TypeScript tokens
5. Documenter dans ce contrat

