'use client'

import { Section } from '@/components/organisms/Section/Section'

interface ProductHeroProps {
  videoUrl?: string
  productName: string
  tagline?: string
}

export default function ProductHero({
  videoUrl,
  productName,
  tagline,
}: ProductHeroProps) {
  return (
    <Section withGlass className="mb-section">
      <div className="text-center space-y-card">
        <h1 className="text-title-xl font-extraLight text-text-primary">
          {productName}
        </h1>
        {tagline && (
          <p className="text-title-md font-regular text-text-secondary">
            {tagline}
          </p>
        )}
        {videoUrl && (
          <div className="mt-section">
            <video
              src={videoUrl}
              autoPlay
              loop
              muted
              className="w-full max-w-4xl mx-auto rounded-lg shadow-strong"
            />
          </div>
        )}
      </div>
    </Section>
  )
}
