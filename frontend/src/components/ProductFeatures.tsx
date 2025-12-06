'use client'

import { Section } from '@/components/organisms/Section/Section'
import { Card } from '@/components/molecules/Card/Card'

interface ProductFeaturesProps {
  features?: string[]
  beforeAfterImages?: { before?: string; after?: string }
}

export default function ProductFeatures({
  features,
  beforeAfterImages,
}: ProductFeaturesProps) {
  return (
    <Section className="mb-section">
      <h2 className="text-title-md font-regular text-center mb-section text-text-primary">
        Caractéristiques du produit
      </h2>

      {features && features.length > 0 && (
        <div className="grid md:grid-cols-2 gap-gridGap mb-section">
          {features.map((feature, index) => (
            <Card key={index} variant="glass" className="p-card">
              <p className="text-body-regular text-text-primary">{feature}</p>
            </Card>
          ))}
        </div>
      )}

      {beforeAfterImages &&
        (beforeAfterImages.before || beforeAfterImages.after) && (
          <div className="grid md:grid-cols-2 gap-gridGap">
            {beforeAfterImages.before && (
              <div>
                <h3 className="text-title-sm font-medium mb-card text-text-primary">
                  Avant
                </h3>
                <img
                  src={beforeAfterImages.before}
                  alt="Avant"
                  className="rounded-lg w-full"
                />
              </div>
            )}
            {beforeAfterImages.after && (
              <div>
                <h3 className="text-title-sm font-medium mb-card text-text-primary">
                  Après
                </h3>
                <img
                  src={beforeAfterImages.after}
                  alt="Après"
                  className="rounded-lg w-full"
                />
              </div>
            )}
          </div>
        )}
    </Section>
  )
}
