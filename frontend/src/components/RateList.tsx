import { RateCard } from './RateCard'
import type { Rate, Currency } from '@/types/rate'

interface Props {
  rates: Rate[]
  currency: Currency
}

export function RateList({ rates, currency }: Props) {
  if (rates.length === 0) {
    return (
      <div className="text-center py-12 text-gray-400">
        Nenhuma cotação encontrada para este filtro.
      </div>
    )
  }

  return (
    <div className="space-y-3">
      {rates.map((rate, i) => (
        <RateCard key={rate.institution} rate={rate} isBest={i === 0} currency={currency} />
      ))}
    </div>
  )
}
