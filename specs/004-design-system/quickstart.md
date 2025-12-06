# Quickstart: Design System Implementation

**Feature**: 004-design-system  
**Date**: 2024-12-19

## Setup

### 1. Installer la police Inter

```bash
# Option 1: Google Fonts (recommandé pour débuter)
# Ajouter dans frontend/src/app/layout.tsx:
# <link rel="preconnect" href="https://fonts.googleapis.com">
# <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin>
# <link href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500&display=swap" rel="stylesheet">

# Option 2: Police locale (pour optimisation)
# Télécharger Inter depuis Google Fonts et placer dans frontend/public/fonts/
```

### 2. Créer la structure de dossiers

```bash
cd frontend/src
mkdir -p design-system components/atoms components/molecules components/organisms
```

### 3. Configurer les tokens Tailwind

```bash
# Modifier frontend/tailwind.config.ts pour inclure tous les tokens de design.json
```

## Validation

### Étape 1: Vérifier les tokens centralisés

```bash
# 1. Vérifier que tailwind.config.ts contient tous les tokens
# 2. Vérifier que design-system/tokens.ts exporte tous les tokens
# 3. Vérifier que globals.css contient les variables CSS
```

**Critère de succès**: Tous les tokens de design.json sont accessibles via Tailwind, CSS Variables et TypeScript.

### Étape 2: Créer un composant atome (Button)

```bash
# Créer frontend/src/components/atoms/Button/Button.tsx
# Utiliser les tokens pour styliser
# Vérifier visuellement la conformité avec design.json
```

**Critère de succès**: Le Button respecte exactement les propriétés définies dans design.json.buttons.default.

### Étape 3: Créer un composant molécule (Card)

```bash
# Créer frontend/src/components/molecules/Card/Card.tsx
# Utiliser les tokens et le Button atom
# Vérifier visuellement la conformité avec design.json
```

**Critère de succès**: La Card respecte exactement les propriétés définies dans design.json.cards.glass.

### Étape 4: Migrer un composant existant (LoginForm)

```bash
# Modifier frontend/src/components/admin/LoginForm.tsx
# Remplacer les styles hardcodés par les tokens
# Vérifier que la fonctionnalité est préservée
```

**Critère de succès**: LoginForm utilise les tokens du design system et fonctionne identiquement à avant.

### Étape 5: Vérifier la navbar

```bash
# Modifier frontend/src/app/admin/layout.tsx (AdminNav)
# Appliquer les tokens de design.json.navbar
# Vérifier visuellement la conformité
```

**Critère de succès**: La navbar respecte exactement les propriétés définies dans design.json.navbar.

## Tests Visuels

### Checklist de Conformité

Pour chaque composant migré, vérifier:

- [ ] Couleurs correspondent exactement à design.json (utiliser un color picker)
- [ ] Typographie utilise Inter avec les poids/tailles corrects
- [ ] Espacements (padding, gap) correspondent exactement
- [ ] Border radius correspondent exactement
- [ ] Shadows correspondent exactement
- [ ] Blur effects correspondent exactement (si applicable)
- [ ] Fonctionnalité préservée (pas de régression)

### Outils de Vérification

- **Color Picker**: Utiliser l'outil de développement du navigateur pour vérifier les couleurs
- **Ruler**: Utiliser l'outil de mesure du navigateur pour vérifier les espacements
- **Font Inspector**: Vérifier la police, poids et taille dans les DevTools
- **Screenshot Comparison**: Comparer visuellement avec design.json

## Exemples d'Utilisation

### Utiliser un token de couleur

```tsx
// Via Tailwind
<div className="bg-primary text-white">Content</div>

// Via CSS Variable
<div style={{ backgroundColor: 'var(--color-primary)' }}>Content</div>

// Via TypeScript
import { tokens } from '@/design-system/tokens';
<div style={{ backgroundColor: tokens.colors.primary }}>Content</div>
```

### Utiliser un token d'espacement

```tsx
// Via Tailwind
<div className="p-screen">Content</div> // 48px

// Via CSS Variable
<div style={{ padding: 'var(--spacing-screen)' }}>Content</div>
```

### Utiliser un effet glass

```tsx
// Via Tailwind (classe custom)
<div className="glass-card">Content</div>

// Via classes Tailwind
<div className="bg-glass backdrop-blur-[40px] rounded-lg shadow-strong">
  Content
</div>
```

## Troubleshooting

### Les tokens ne sont pas appliqués

1. Vérifier que `tailwind.config.ts` est correctement configuré
2. Vérifier que les classes Tailwind sont dans le `content` array
3. Redémarrer le serveur de développement
4. Vérifier que les variables CSS sont définies dans `globals.css`

### La police Inter ne charge pas

1. Vérifier que le lien Google Fonts est dans `layout.tsx`
2. Vérifier la connexion internet (pour Google Fonts)
3. Vérifier que `font-family: 'Inter'` est dans `globals.css`

### Les effets blur ne fonctionnent pas

1. Vérifier la compatibilité du navigateur (Chrome 76+, Safari 9+, Firefox 103+)
2. Vérifier que `backdrop-filter` est supporté
3. Vérifier que les valeurs blur sont correctes dans la config Tailwind

