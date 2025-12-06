# Design System

Ce design system est basé sur `design.json` et garantit une cohérence visuelle à 100% à travers l'application.

## Architecture

Le design system suit l'architecture atomique :

- **Atomes** : Composants de base (Button, Input, Label, Badge, Icon)
- **Molécules** : Composants composés d'atomes (Card, Form, StatCard, ButtonGroup)
- **Organismes** : Composants complexes (Navbar, PageLayout, Section, DataTable)

## Accès aux Tokens

### Via Tailwind CSS

```tsx
<div className="bg-primary text-text-primary rounded-lg p-card">
  Contenu
</div>
```

### Via CSS Variables

```css
.custom-element {
  background-color: var(--color-primary);
  border-radius: var(--radius-lg);
  padding: var(--spacing-card);
}
```

### Via TypeScript

```typescript
import { tokens } from '@/design-system/tokens';

const primaryColor = tokens.colors.primary; // '#FF7335'
const cardRadius = tokens.radii.lg; // 32
```

## Composants Disponibles

### Atomes

- **Button** : `@/components/atoms/Button/Button`
  - Variants: `default`, `tag`
  - States: `active`, `inactive` (pour tag)

- **Input** : `@/components/atoms/Input/Input`
  - Supporte les erreurs et labels

- **Label** : `@/components/atoms/Label/Label`
  - Supporte le marqueur `required`

- **Badge** : `@/components/atoms/Badge/Badge`
  - Variants: `default`, `tag`
  - States: `active`, `inactive`

- **Icon** : `@/components/atoms/Icon/Icon`
  - Enforce strokeWidth 1.7px et couleur #FFFFFF

### Molécules

- **Card** : `@/components/molecules/Card/Card`
  - Variants: `glass`, `stat`

- **StatCard** : `@/components/molecules/StatCard/StatCard`
  - Affiche titre, valeur, et sous-titre optionnel

- **Form** : `@/components/molecules/Form/Form`
  - Utilise Input, Label, Button
  - Exports: `Form.Input`, `Form.Label`, `Form.Button`

- **ButtonGroup** : `@/components/molecules/ButtonGroup/ButtonGroup`
  - Groupe de boutons avec espacement cohérent

### Organismes

- **Navbar** : `@/components/organisms/Navbar/Navbar`
  - Height: 68px, blur: 25px, background: rgba(0,0,0,0.30)

- **PageLayout** : `@/components/organisms/PageLayout/PageLayout`
  - Padding: 48px, maxWidth: 1600px

- **Section** : `@/components/organisms/Section/Section`
  - Padding: 32px, option glass effect

## Tokens Disponibles

### Couleurs

- `primary`: #FF7335
- `background.light`, `background.dark`, `background.card`, `background.glass`, `background.glassDark`
- `text.primary`, `text.secondary`, `text.dark`, `text.muted`
- `accent.blue`, `accent.green`, `accent.red`, `accent.beige`, `accent.grey`, `accent.black`

### Typographie

- Police: Inter
- Poids: 200 (extraLight), 300 (light), 400 (regular), 500 (medium)
- Tailles: title-xl (88px), title-lg (54px), title-md (32px), title-sm (20px), body-regular (18px), body-small (14px)

### Espacements

- `screen`: 48px
- `section`: 32px
- `card`: 24px
- `component`: 16px
- `gridGap`: 32px

### Border Radius

- `xs`: 8px, `sm`: 14px, `md`: 22px, `lg`: 32px, `xl`: 48px, `xxl`: 60px, `full`: 999px

### Shadows

- `soft`: 0 4px 32px rgba(0,0,0,0.25)
- `strong`: 0 8px 48px rgba(0,0,0,0.35)
- `inner-glow`: inset 0 0 32px rgba(255,255,255,0.1)

### Blur

- `glass-strong`: 45px
- `card`: 25px
- `background-fog`: 80px

## Utilitaires Tailwind Personnalisés

- `.glass-card`: Effet glass complet (background, blur, radius, shadow)
- `.glass-strong`: Blur fort (45px)
- `.gradient-overlay`: Gradient overlay avec overlay blend mode

## Exemples d'Utilisation

### Créer un bouton

```tsx
import { Button } from '@/components/atoms/Button/Button';

<Button variant="default">Cliquer</Button>
<Button variant="tag" state="active">Tag actif</Button>
```

### Créer une carte

```tsx
import { Card } from '@/components/molecules/Card/Card';

<Card variant="glass">
  <div className="p-card">
    Contenu de la carte
  </div>
</Card>
```

### Créer un formulaire

```tsx
import { Form } from '@/components/molecules/Form/Form';

<Form onSubmit={(data) => console.log(data)}>
  <Form.Label required>Email</Form.Label>
  <Form.Input type="email" name="email" />
  <Form.Button type="submit">Envoyer</Form.Button>
</Form>
```

## Validation

Tous les composants doivent respecter scrupuleusement les valeurs de `design.json` :
- Couleurs : tolérance 0%
- Espacements : tolérance 0px
- Radius : tolérance 0px
- Typographie : police Inter avec poids/tailles exacts

## Pages Showcase

- `/design-system/atoms` : Affiche tous les atomes
- `/design-system/molecules` : Affiche toutes les molécules
- `/design-system/organisms` : Affiche tous les organismes

Utilisez ces pages pour vérifier visuellement la conformité avec `design.json`.

