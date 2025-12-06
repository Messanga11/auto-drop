# Research: Design System Implementation

**Feature**: 004-design-system  
**Date**: 2024-12-19

## Research Decisions

### Decision 1: Architecture de Tokens Centralisés

**Decision**: Utiliser Tailwind CSS comme système principal de tokens avec extension de la configuration pour inclure tous les tokens de design.json. Exposer également les tokens via variables CSS et un fichier TypeScript pour l'accès programmatique.

**Rationale**: 
- Tailwind CSS est déjà configuré dans le projet et est le standard pour Next.js
- Permet l'utilisation de classes utilitaires (ex: `bg-primary`, `text-xl`, `rounded-lg`)
- Les variables CSS permettent l'utilisation dans les styles inline et les composants dynamiques
- Le fichier TypeScript permet l'accès programmatique et l'autocomplétion

**Alternatives considered**:
- **CSS Variables uniquement**: Rejeté car moins pratique pour Tailwind et nécessite plus de code CSS custom
- **Styled Components ou Emotion**: Rejeté car ajoute une dépendance et n'est pas aligné avec Tailwind déjà présent
- **Système de tokens séparé (Style Dictionary)**: Rejeté car trop complexe pour les besoins actuels

**Implementation approach**:
- Étendre `tailwind.config.ts` avec tous les tokens de design.json (colors, typography, spacing, borderRadius, boxShadow, backdropBlur)
- Créer `design-system/tokens.ts` qui exporte tous les tokens depuis design.json pour l'accès TypeScript
- Créer `design-system/globals.css` avec les variables CSS correspondantes
- Utiliser `@apply` de Tailwind pour créer des classes utilitaires réutilisables si nécessaire

### Decision 2: Architecture Atomique (Atomic Design)

**Decision**: Organiser les composants selon l'architecture atomique (atomes, molécules, organismes) dans des dossiers séparés.

**Rationale**:
- Aligné avec la spécification qui mentionne explicitement "atomes, molécules, organismes"
- Facilite la réutilisabilité et la maintenabilité
- Permet une migration progressive (créer les atomes d'abord, puis les molécules, puis les organismes)
- Structure claire pour les développeurs

**Alternatives considered**:
- **Organisation par feature**: Rejeté car ne correspond pas à la demande explicite de l'utilisateur
- **Organisation plate**: Rejeté car moins scalable et moins claire

**Implementation approach**:
- `components/atoms/`: Button, Input, Badge, Icon, Label
- `components/molecules/`: Card, Form, StatCard, ButtonGroup
- `components/organisms/`: Navbar, DataTable (refactorisé), PageLayout, Section
- Les composants existants dans `admin/` et `common/` seront migrés pour utiliser les nouveaux atomes/molécules/organismes

### Decision 3: Migration Progressive des Composants Existants

**Decision**: Migrer les composants existants un par un en préservant leur fonctionnalité, en commençant par les atomes, puis les molécules, puis les organismes.

**Rationale**:
- Minimise le risque de régression
- Permet de tester chaque composant individuellement
- Permet un déploiement progressif
- Facilite le debugging

**Alternatives considered**:
- **Migration en une seule fois**: Rejeté car trop risqué et difficile à déboguer
- **Créer de nouveaux composants et remplacer**: Rejeté car nécessite de dupliquer la logique fonctionnelle

**Implementation approach**:
1. Créer les tokens centralisés (Phase 1)
2. Créer les atomes conformes au design system (Phase 2)
3. Migrer les composants existants pour utiliser les atomes (Phase 3)
4. Créer les molécules et organismes conformes (Phase 4)
5. Migrer les composants complexes pour utiliser les molécules/organismes (Phase 5)

### Decision 4: Gestion de la Police Inter

**Decision**: Charger la police Inter via Google Fonts avec preload pour optimiser les performances, ou utiliser une version locale si nécessaire.

**Rationale**:
- Google Fonts est simple à intégrer et optimisé
- Preload améliore les performances de chargement
- Permet de charger uniquement les poids nécessaires (200, 300, 400, 500)

**Alternatives considered**:
- **Police système**: Rejeté car ne garantit pas la cohérence visuelle
- **Font local uniquement**: Considéré mais Google Fonts est plus simple pour commencer

**Implementation approach**:
- Ajouter le lien Google Fonts dans `app/layout.tsx` avec preload
- Configurer `font-family: 'Inter', sans-serif` dans `globals.css`
- Optionnel: Télécharger et héberger localement si nécessaire pour l'optimisation

### Decision 5: Effets Visuels (Glass, Blur, Gradients)

**Decision**: Utiliser les propriétés CSS natives (backdrop-filter pour blur, linear-gradient pour gradients) avec fallbacks pour les navigateurs non supportés.

**Rationale**:
- Support moderne des navigateurs (Chrome 76+, Safari 9+, Firefox 103+)
- Performance native CSS meilleure que les solutions JavaScript
- Tailwind CSS supporte backdrop-filter et gradients nativement

**Alternatives considered**:
- **Bibliothèques JavaScript pour effets**: Rejeté car ajoute de la complexité et de la dépendance
- **Images pour gradients**: Rejeté car moins flexible et plus lourd

**Implementation approach**:
- Utiliser `backdrop-blur-{value}` de Tailwind pour les effets glass
- Utiliser `bg-gradient-to-{direction}` de Tailwind pour les gradients
- Créer des classes utilitaires personnalisées si nécessaire pour les effets spécifiques (ex: `glass-card`, `gradient-overlay`)

### Decision 6: Compatibilité avec Composants Tiers

**Decision**: Wrapper ou styliser les composants tiers (ex: DataTable) pour respecter le design system sans modifier leur code source.

**Rationale**:
- Évite de fork les bibliothèques tierces
- Permet de mettre à jour les dépendances facilement
- Respecte le principe de séparation des responsabilités

**Alternatives considered**:
- **Fork et modifier**: Rejeté car difficile à maintenir
- **Créer nos propres composants**: Considéré mais DataTable est déjà implémenté et fonctionne bien

**Implementation approach**:
- Utiliser les classes Tailwind et les tokens pour styliser les composants tiers
- Wrapper les composants tiers dans des composants qui appliquent le design system
- Utiliser `className` prop pour surcharger les styles par défaut

## Technical Patterns

### Pattern 1: Tokens Tailwind

```typescript
// tailwind.config.ts
export default {
  theme: {
    extend: {
      colors: {
        primary: '#FF7335',
        // ... tous les tokens de design.json
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      // ... autres tokens
    },
  },
}
```

### Pattern 2: Variables CSS

```css
/* globals.css */
:root {
  --color-primary: #FF7335;
  --radius-lg: 32px;
  --blur-glass: 40px;
  /* ... tous les tokens */
}
```

### Pattern 3: Tokens TypeScript

```typescript
// design-system/tokens.ts
import designJson from '../../design.json';

export const tokens = {
  colors: designJson.colors,
  typography: designJson.typography,
  // ... export structuré
};
```

## Browser Compatibility

- **backdrop-filter**: Chrome 76+, Safari 9+, Firefox 103+, Edge 79+
- **CSS Variables**: Tous les navigateurs modernes (IE11 non supporté, mais non requis)
- **Gradients**: Support universel
- **Font Inter**: Support universel via Google Fonts

## Performance Considerations

- **Police Inter**: Utiliser `font-display: swap` pour éviter le FOIT (Flash of Invisible Text)
- **CSS Purge**: Tailwind purge automatiquement les classes non utilisées en production
- **Variables CSS**: Performantes, évaluées une fois au chargement
- **Backdrop-filter**: Peut impacter les performances sur les appareils moins puissants, mais acceptable pour l'expérience visuelle

