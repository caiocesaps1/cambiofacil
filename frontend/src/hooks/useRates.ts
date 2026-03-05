import { useQuery } from '@tanstack/react-query'
import { api } from '@/services/api'
import type { Currency } from '@/types/rate'

export function useRates(currency: Currency, amount: number, type?: string) {
  return useQuery({
    queryKey: ['rates', currency, amount, type],
    queryFn: () => api.getRates(currency, amount, type),
    staleTime: 5 * 60 * 1000,
    refetchInterval: 15 * 60 * 1000,
    retry: 1,
  })
}
