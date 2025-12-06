import { Metadata } from 'next'
import { notFound } from 'next/navigation'
import ProductHero from '@/components/ProductHero'
import ProductFeatures from '@/components/ProductFeatures'
import OrderForm from '@/components/OrderForm'
import { getProductBySlug } from '@/lib/product-api'

interface ProductPageProps {
  params: {
    slug: string
  }
}

// Génération statique des pages au build
export async function generateStaticParams() {
  // Récupérer la liste des produits depuis l'API
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/scoring/top-products?limit=10`)
    const products = await response.json()
    return products.map((product: any) => ({
      slug: product.product_id.toString(),
    }))
  } catch {
    return []
  }
}

// Métadonnées dynamiques pour SEO
export async function generateMetadata(
  { params }: ProductPageProps
): Promise<Metadata> {
  const product = await getProductBySlug(params.slug)

  if (!product) {
    return {
      title: 'Produit introuvable',
    }
  }

  return {
    title: `${product.name} - Commandez maintenant`,
    description: product.description || product.caption,
    openGraph: {
      title: product.name,
      description: product.description || product.caption,
      images: product.ad_url ? [product.ad_url] : [],
    },
  }
}

export default async function ProductPage({ params }: ProductPageProps) {
  const product = await getProductBySlug(params.slug)

  if (!product) {
    notFound()
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      {/* Hero avec vidéo */}
      <ProductHero
        videoUrl={product.videos?.ugc}
        productName={product.name}
        tagline={product.caption}
      />

      {/* Caractéristiques */}
      <ProductFeatures
        features={product.features || []}
        beforeAfterImages={product.beforeAfter}
      />

      {/* Formulaire de commande */}
      <section className="py-16 px-4">
        <div className="max-w-2xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-8">
            Commander maintenant
          </h2>
          <OrderForm
            productId={product.id}
            productName={product.name}
          />
        </div>
      </section>

      {/* Pixel tracking Meta & TikTok */}
      <script
        dangerouslySetInnerHTML={{
          __html: `
            !function(f,b,e,v,n,t,s)
            {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
            n.callMethod.apply(n,arguments):n.queue.push(arguments)};
            if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
            n.queue=[];t=b.createElement(e);t.async=!0;
            t.src=v;s=b.getElementsByTagName(e)[0];
            s.parentNode.insertBefore(t,s)}(window, document,'script',
            'https://connect.facebook.net/en_US/fbevents.js');
            fbq('init', '${process.env.NEXT_PUBLIC_META_PIXEL_ID}');
            fbq('track', 'PageView');
            fbq('track', 'ViewContent', {
              content_name: '${product.name}',
              content_ids: ['${product.id}'],
              content_type: 'product',
            });
          `,
        }}
      />
    </main>
  )
}

// ISR: revalider la page toutes les heures
export const revalidate = 3600

