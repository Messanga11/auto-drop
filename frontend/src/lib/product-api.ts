import { api } from './api-client'

export interface Product {
  id: number
  name: string
  description?: string
  caption?: string
  ad_url?: string
  platform: string
  score: number
  videos?: {
    ugc?: string
    problem_solution?: string
    short_hook?: string
    carousel?: string
  }
  features?: string[]
  beforeAfter?: {
    before?: string
    after?: string
  }
}

export async function getProductBySlug(slug: string): Promise<Product | null> {
  try {
    const productId = parseInt(slug, 10)
    if (isNaN(productId)) {
      return null
    }

    // Récupérer depuis l'API
    const products = await api.get<Product[]>(`/scoring/top-products?limit=100`)
    const product = products.find((p) => p.id === productId)

    if (!product) {
      return null
    }

    return {
      ...product,
      name: product.name || `Produit ${product.id}`,
    }
  } catch (error) {
    console.error('Error fetching product:', error)
    return null
  }
}

