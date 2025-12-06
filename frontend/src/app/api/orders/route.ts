import { NextRequest, NextResponse } from 'next/server'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()

    // Valider les données
    if (!body.productId || !body.fullName || !body.phone || !body.address) {
      return NextResponse.json(
        { error: 'Données manquantes' },
        { status: 400 }
      )
    }

    // Envoyer à l'API backend
    const response = await fetch(`${API_URL}/api/orders`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    })

    if (!response.ok) {
      const error = await response.json()
      return NextResponse.json(
        { error: error.detail || 'Erreur serveur' },
        { status: response.status }
      )
    }

    const data = await response.json()

    return NextResponse.json({
      orderId: data.id,
      estimatedValue: 0, // À calculer selon le produit
      message: 'Commande enregistrée avec succès',
    })
  } catch (error) {
    console.error('Error processing order:', error)
    return NextResponse.json(
      { error: 'Erreur lors du traitement de la commande' },
      { status: 500 }
    )
  }
}

