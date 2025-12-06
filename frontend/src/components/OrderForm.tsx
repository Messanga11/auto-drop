'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import { Form } from '@/components/molecules/Form/Form'
import { Button } from '@/components/atoms/Button/Button'
import { Card } from '@/components/molecules/Card/Card'

const orderSchema = z.object({
  fullName: z.string().min(2, 'Nom complet requis'),
  phone: z.string().regex(/^[+]?[0-9]{10,15}$/, 'Numéro de téléphone invalide'),
  address: z.string().min(10, 'Adresse complète requise'),
  city: z.string().min(2, 'Ville requise'),
  quantity: z.number().min(1).max(10),
})

type OrderFormData = z.infer<typeof orderSchema>

interface OrderFormProps {
  productId: number
  productName: string
}

export default function OrderForm({ productId, productName }: OrderFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitSuccess, setSubmitSuccess] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<OrderFormData>({
    resolver: zodResolver(orderSchema),
    defaultValues: {
      quantity: 1,
    },
  })

  const onSubmit = async (data: OrderFormData) => {
    setIsSubmitting(true)

    try {
      const response = await fetch('/api/orders', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...data,
          productId,
          productName,
        }),
      })

      if (!response.ok) {
        throw new Error('Erreur lors de la commande')
      }

      const result = await response.json()

      // Tracking Meta Pixel
      if (typeof window !== 'undefined' && (window as any).fbq) {
        (window as any).fbq('track', 'Lead', {
          content_name: productName,
          value: result.estimatedValue || 0,
          currency: 'EUR',
        })
      }

      setSubmitSuccess(true)
      reset()

      // Rediriger vers WhatsApp après 2 secondes
      setTimeout(() => {
        const whatsappUrl = `https://wa.me/${process.env.NEXT_PUBLIC_WHATSAPP_NUMBER}?text=${encodeURIComponent(
          `Bonjour, je viens de commander ${productName}. Référence: ${result.orderId}`
        )}`
        window.open(whatsappUrl, '_blank')
      }, 2000)

    } catch (error) {
      console.error('Erreur commande:', error)
      alert('Une erreur est survenue. Veuillez réessayer.')
    } finally {
      setIsSubmitting(false)
    }
  }

  if (submitSuccess) {
    return (
      <Card variant="glass" className="p-card">
        <div className="text-center space-y-card">
          <h3 className="text-title-md font-regular text-text-primary">
            Commande confirmée !
          </h3>
          <p className="text-body-regular text-text-secondary">
            Vous allez être redirigé vers WhatsApp...
          </p>
        </div>
      </Card>
    )
  }

  return (
    <Card variant="glass" className="p-card">
      <h2 className="text-title-sm font-medium mb-card text-text-primary">
        Passer commande
      </h2>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-card">
        <div>
          <Form.Label required>Nom complet</Form.Label>
          <Form.Input
            {...register('fullName')}
            placeholder="Votre nom complet"
            error={errors.fullName?.message}
          />
        </div>

        <div>
          <Form.Label required>Téléphone</Form.Label>
          <Form.Input
            {...register('phone')}
            type="tel"
            placeholder="+33 6 12 34 56 78"
            error={errors.phone?.message}
          />
        </div>

        <div>
          <Form.Label required>Adresse</Form.Label>
          <Form.Input
            {...register('address')}
            placeholder="Votre adresse complète"
            error={errors.address?.message}
          />
        </div>

        <div>
          <Form.Label required>Ville</Form.Label>
          <Form.Input
            {...register('city')}
            placeholder="Votre ville"
            error={errors.city?.message}
          />
        </div>

        <div>
          <Form.Label required>Quantité</Form.Label>
          <Form.Input
            {...register('quantity', { valueAsNumber: true })}
            type="number"
            min={1}
            max={10}
            error={errors.quantity?.message}
          />
        </div>

        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Traitement...' : 'Commander'}
        </Button>
      </form>
    </Card>
  )
}
