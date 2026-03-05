import { useState } from 'react'
import { CurrencySelector } from '@/components/CurrencySelector'
import { AmountInput } from '@/components/AmountInput'
import { FilterBar } from '@/components/FilterBar'
import { RateList } from '@/components/RateList'
import { LastUpdated } from '@/components/LastUpdated'
import { useRates } from '@/hooks/useRates'
import type { Currency, InstitutionType } from '@/types/rate'

export function Home() {
  const [currency, setCurrency] = useState<Currency>('USD')
  const [amount, setAmount] = useState(1000)
  const [typeFilter, setTypeFilter] = useState<InstitutionType | undefined>(undefined)

  const { data, isLoading, isError, error, isRefetching } = useRates(currency, amount, typeFilter)

  return (
    <div className="min-h-screen bg-slate-100">
      {/* Header */}
      <header className="bg-blue-700 text-white py-6 px-4 shadow-md">
        <div className="max-w-2xl mx-auto">
          <h1 className="text-2xl font-bold tracking-tight">CâmbioFácil</h1>
          <p className="text-blue-200 text-sm mt-0.5">Compare as melhores taxas de câmbio em tempo real</p>
        </div>
      </header>

      <main className="max-w-2xl mx-auto px-4 py-6 space-y-5">
        {/* Controles */}
        <div className="bg-white rounded-2xl shadow-sm p-5 space-y-4">
          <CurrencySelector value={currency} onChange={setCurrency} />
          <AmountInput value={amount} onChange={setAmount} />
        </div>

        {/* Filtro */}
        <FilterBar value={typeFilter} onChange={setTypeFilter} />

        {/* Resultados */}
        {isLoading && (
          <div className="text-center py-12 text-gray-400 animate-pulse">Buscando cotações...</div>
        )}

        {isError && (
          <div className="bg-red-50 border border-red-200 text-red-700 rounded-xl p-4 text-sm">
            {(error as Error).message}
          </div>
        )}

        {data && (
          <>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-500">
                {data.rates.length} resultado{data.rates.length !== 1 ? 's' : ''}
              </span>
              <LastUpdated fetchedAt={data.fetched_at} isRefetching={isRefetching} />
            </div>
            <RateList rates={data.rates} currency={currency} />
          </>
        )}
      </main>
    </div>
  )
}
