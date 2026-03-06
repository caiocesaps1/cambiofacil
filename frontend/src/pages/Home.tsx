import { useState } from 'react'
import { Moon, Sun, ArrowLeftRight } from 'lucide-react'
import { CurrencySelector } from '@/components/CurrencySelector'
import { AmountInput, foreignPresets } from '@/components/AmountInput'
import { FilterBar } from '@/components/FilterBar'
import { RateList } from '@/components/RateList'
import { RateListSkeleton } from '@/components/RateCardSkeleton'
import { LastUpdated } from '@/components/LastUpdated'
import { useRates } from '@/hooks/useRates'
import { useDarkMode } from '@/hooks/useDarkMode'
import type { Currency, InstitutionType } from '@/types/rate'

type Mode = 'normal' | 'reverse'

export function Home() {
  const [currency, setCurrency] = useState<Currency>('USD')
  const [amount, setAmount] = useState(1000)
  const [foreignAmount, setForeignAmount] = useState(500)
  const [mode, setMode] = useState<Mode>('normal')
  const [typeFilter, setTypeFilter] = useState<InstitutionType | undefined>(undefined)
  const { isDark, toggle } = useDarkMode()

  // Em modo reverso, buscamos com um valor BRL fixo grande para obter as taxas
  const apiAmount = mode === 'normal' ? amount : 10000
  const { data, isLoading, isError, error, isRefetching } = useRates(currency, apiAmount, typeFilter)

  const currencySymbol = currency === 'USDC' ? 'USDC' : currency === 'EUR' ? '€' : '$'

  return (
    <div className="min-h-screen bg-slate-100 dark:bg-slate-900">
      {/* Header */}
      <header className="bg-blue-700 text-white py-6 px-4 shadow-md">
        <div className="max-w-2xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold tracking-tight">CâmbioFácil</h1>
            <p className="text-blue-200 text-sm mt-0.5">Compare as melhores taxas de câmbio em tempo real</p>
          </div>
          <button
            onClick={toggle}
            aria-label={isDark ? 'Ativar modo claro' : 'Ativar modo escuro'}
            className="p-2 rounded-lg text-blue-200 hover:text-white hover:bg-blue-600 transition-colors"
          >
            {isDark ? <Sun size={20} /> : <Moon size={20} />}
          </button>
        </div>
      </header>

      <main className="max-w-2xl mx-auto px-4 py-6 space-y-5">
        {/* Controles */}
        <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-sm p-5 space-y-4">
          <CurrencySelector value={currency} onChange={setCurrency} />

          {/* Toggle de modo */}
          <div className="flex rounded-xl border border-gray-200 dark:border-slate-700 overflow-hidden text-sm font-semibold">
            <button
              onClick={() => setMode('normal')}
              className={`flex-1 py-2 transition-colors ${
                mode === 'normal'
                  ? 'bg-blue-600 text-white'
                  : 'bg-white dark:bg-slate-800 text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-slate-700'
              }`}
            >
              Tenho BRL → recebo {currency}
            </button>
            <button
              onClick={() => setMode('reverse')}
              className={`flex-1 py-2 flex items-center justify-center gap-1.5 transition-colors ${
                mode === 'reverse'
                  ? 'bg-blue-600 text-white'
                  : 'bg-white dark:bg-slate-800 text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-slate-700'
              }`}
            >
              <ArrowLeftRight size={14} />
              Quero {currency} → pago BRL
            </button>
          </div>

          {mode === 'normal' ? (
            <AmountInput value={amount} onChange={setAmount} />
          ) : (
            <AmountInput
              value={foreignAmount}
              onChange={setForeignAmount}
              label={`Quantidade de ${currency} desejada`}
              prefix={currencySymbol}
              presets={foreignPresets}
            />
          )}
        </div>

        {/* Filtro */}
        <FilterBar value={typeFilter} onChange={setTypeFilter} />

        {/* Resultados */}
        {isLoading && <RateListSkeleton />}

        {isError && (
          <div className="bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 rounded-xl p-4 text-sm">
            {(error as Error).message}
          </div>
        )}

        {data && (
          <>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-500 dark:text-gray-400">
                {data.rates.length} resultado{data.rates.length !== 1 ? 's' : ''}
              </span>
              <LastUpdated fetchedAt={data.fetched_at} isRefetching={isRefetching} />
            </div>
            <RateList
              rates={data.rates}
              currency={currency}
              mode={mode}
              foreignAmount={foreignAmount}
            />
          </>
        )}
      </main>
    </div>
  )
}
