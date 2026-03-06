import { RateCard } from './RateCard'
import type { Rate, Currency } from '@/types/rate'

interface Props {
  rates: Rate[]
  currency: Currency
  mode: 'normal' | 'reverse'
  foreignAmount?: number
}

export function RateList({ rates, currency, mode, foreignAmount = 0 }: Props) {
  if (rates.length === 0) {
    return (
      <div className="text-center py-12 text-gray-400 dark:text-gray-500">
        Nenhuma cotação encontrada para este filtro.
      </div>
    )
  }

  const isReverse = mode === 'reverse'
  const worstRate = rates[rates.length - 1]
  const worstBrlCost = foreignAmount * worstRate.buy_rate
  const worstAmountReceived = worstRate.amount_received

  return (
    <div className="space-y-3">
      {rates.map((rate, i) => {
        const brlCost = isReverse ? foreignAmount * rate.buy_rate : undefined
        const savingsVsWorst = i === 0
          ? isReverse
            ? worstBrlCost - (foreignAmount * rate.buy_rate)
            : rate.amount_received - worstAmountReceived
          : undefined

        return (
          <RateCard
            key={rate.institution}
            rate={rate}
            isBest={i === 0}
            currency={currency}
            mode={mode}
            brlCost={brlCost}
            savingsVsWorst={savingsVsWorst}
          />
        )
      })}
    </div>
  )
}
