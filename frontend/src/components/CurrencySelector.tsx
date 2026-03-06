import type { Currency } from '@/types/rate'

interface Props {
  value: Currency
  onChange: (v: Currency) => void
}

const options: { value: Currency; label: string; flag: string }[] = [
  { value: 'USD', label: 'Dólar Americano', flag: '🇺🇸' },
  { value: 'EUR', label: 'Euro', flag: '🇪🇺' },
  { value: 'USDC', label: 'USD Coin', flag: '💵' },
]

export function CurrencySelector({ value, onChange }: Props) {
  return (
    <div className="flex gap-3">
      {options.map((opt) => (
        <button
          key={opt.value}
          onClick={() => onChange(opt.value)}
          className={`flex-1 flex items-center justify-center gap-2 py-3 px-4 rounded-xl border-2 font-semibold transition-all ${
            value === opt.value
              ? 'border-blue-600 bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300'
              : 'border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-gray-600 dark:text-gray-300 hover:border-blue-300'
          }`}
        >
          <span className="text-2xl">{opt.flag}</span>
          <span>{opt.value}</span>
          <span className="hidden sm:inline text-sm font-normal opacity-70">— {opt.label}</span>
        </button>
      ))}
    </div>
  )
}
