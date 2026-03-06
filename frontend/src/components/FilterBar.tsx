import type { InstitutionType } from '@/types/rate'

interface Props {
  value: InstitutionType | undefined
  onChange: (v: InstitutionType | undefined) => void
}

const filters: { value: InstitutionType | undefined; label: string }[] = [
  { value: undefined, label: 'Todos' },
  { value: 'fintech', label: 'Fintechs' },
  { value: 'bank', label: 'Bancos' },
  { value: 'broker', label: 'Corretoras' },
  { value: 'exchange_house', label: 'Casas de câmbio' },
]

export function FilterBar({ value, onChange }: Props) {
  return (
    <div className="flex gap-2 flex-wrap">
      {filters.map((f) => (
        <button
          key={String(f.value)}
          onClick={() => onChange(f.value)}
          className={`text-sm px-4 py-1.5 rounded-full border transition-all ${
            value === f.value
              ? 'border-blue-600 bg-blue-600 text-white font-semibold'
              : 'border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-gray-600 dark:text-gray-300 hover:border-blue-400'
          }`}
        >
          {f.label}
        </button>
      ))}
    </div>
  )
}
