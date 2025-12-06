export function getWhatsAppUrl(phone: string, message: string): string {
  const phoneNumber = process.env.NEXT_PUBLIC_WHATSAPP_NUMBER || phone
  const encodedMessage = encodeURIComponent(message)
  return `https://wa.me/${phoneNumber}?text=${encodedMessage}`
}

export function openWhatsApp(phone: string, message: string): void {
  const url = getWhatsAppUrl(phone, message)
  window.open(url, '_blank')
}

