import { ExternalLink } from 'lucide-react'
import type { Rate } from '@/types/rate'

interface Props {
  rate: Rate
  isBest: boolean
  currency: string
  savingsVsWorst?: number
}

const typeLabel: Record<string, string> = {
  bank: 'Banco',
  fintech: 'Fintech',
  broker: 'Corretora',
  exchange_house: 'Casa de câmbio',
}

export function RateCard({ rate, isBest, currency, savingsVsWorst }: Props) {
  return (
    <div
      className={`relative flex items-center justify-between p-4 rounded-xl border transition-all ${
        isBest
          ? 'border-green-500 bg-green-50 dark:bg-green-900/20 shadow-sm shadow-green-100 dark:shadow-green-900'
          : 'border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:border-blue-200 dark:hover:border-blue-500'
      }`}
    >
      {isBest && (
        <span className="absolute -top-2.5 left-4 bg-green-500 text-white text-xs font-bold px-2 py-0.5 rounded-full">
          Melhor preço
        </span>
      )}

      <div className="flex-1">
        <div className="flex items-center gap-2">
          <span className="font-semibold text-gray-900 dark:text-white">{rate.institution}</span>
          <span className="text-xs text-gray-400 bg-gray-100 dark:bg-slate-700 dark:text-gray-400 px-2 py-0.5 rounded-full">
            {typeLabel[rate.type] ?? rate.type}
          </span>
        </div>
        <div className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Compra R$ {rate.buy_rate.toFixed(4)} · Spread {rate.spread_pct}%
        </div>
        {savingsVsWorst != null && savingsVsWorst > 0 && (
          <div className="mt-1 text-xs font-semibold text-green-600 dark:text-green-400">
            +{savingsVsWorst.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} {currency} a mais que a pior opção
          </div>
        )}
      </div>

      <div className="flex items-center gap-4">
        <div className="text-right">
          <div className={`text-xl font-bold ${isBest ? 'text-green-700 dark:text-green-400' : 'text-gray-900 dark:text-white'}`}>
            {rate.amount_received.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
          </div>
          <div className="text-xs text-gray-400 dark:text-gray-500">{currency} recebidos</div>
        </div>

        <a
          href={rate.url}
          target="_blank"
          rel="noopener noreferrer"
          className={`flex items-center gap-1 text-sm font-semibold px-4 py-2 rounded-lg transition-colors ${
            isBest
              ? 'bg-green-500 text-white hover:bg-green-600'
              : 'bg-blue-600 text-white hover:bg-blue-700'
          }`}
        >
          Comprar
          <ExternalLink size={14} />
        </a>
      </div>
    </div>
  )
}
