interface Props {
  value: number
  onChange: (v: number) => void
  label?: string
  prefix?: string
  presets?: { value: number; label: string }[]
}

const brlPresets = [
  { value: 1000, label: 'R$ 1.000' },
  { value: 2000, label: 'R$ 2.000' },
  { value: 5000, label: 'R$ 5.000' },
  { value: 10000, label: 'R$ 10.000' },
]

const foreignPresets = [
  { value: 100, label: '100' },
  { value: 500, label: '500' },
  { value: 1000, label: '1.000' },
  { value: 5000, label: '5.000' },
]

export { brlPresets, foreignPresets }

export function AmountInput({ value, onChange, label = 'Valor em BRL', prefix = 'R$', presets = brlPresets }: Props) {
  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">{label}</label>
      <div className="relative">
        <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 dark:text-gray-400 font-medium">{prefix}</span>
        <input
          type="number"
          min={1}
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
          className="w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-slate-600 bg-white dark:bg-slate-700 text-gray-900 dark:text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-lg font-semibold"
        />
      </div>
      <div className="flex gap-2 flex-wrap">
        {presets.map((p) => (
          <button
            key={p.value}
            onClick={() => onChange(p.value)}
            className={`text-sm px-3 py-1 rounded-full border transition-all ${
              value === p.value
                ? 'border-blue-600 bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 font-semibold'
                : 'border-gray-200 dark:border-slate-700 text-gray-500 dark:text-gray-400 hover:border-blue-300'
            }`}
          >
            {p.label}
          </button>
        ))}
      </div>
    </div>
  )
}
