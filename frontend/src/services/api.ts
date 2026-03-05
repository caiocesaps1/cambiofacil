import type { Currency, RatesResponse } from '@/types/rate'

const BASE_URL = import.meta.env.VITE_API_URL ?? '/api'

export const api = {
  getRates: async (currency: Currency, amount: number, type?: string): Promise<RatesResponse> => {
    const params = new URLSearchParams({ currency, amount: String(amount) })
    if (type) params.set('type', type)
    const res = await fetch(`${BASE_URL}/rates?${params}`)
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Erro ao buscar cotações' }))
      throw new Error(error.detail ?? 'Erro desconhecido')
    }
    return res.json()
  },
}
