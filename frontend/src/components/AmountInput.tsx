interface Props {
  value: number
  onChange: (v: number) => void
}

const presets = [1000, 2000, 5000, 10000]

export function AmountInput({ value, onChange }: Props) {
  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-gray-700">Valor em BRL</label>
      <div className="relative">
        <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 font-medium">R$</span>
        <input
          type="number"
          min={1}
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
          className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-lg font-semibold"
        />
      </div>
      <div className="flex gap-2 flex-wrap">
        {presets.map((p) => (
          <button
            key={p}
            onClick={() => onChange(p)}
            className={`text-sm px-3 py-1 rounded-full border transition-all ${
              value === p
                ? 'border-blue-600 bg-blue-50 text-blue-700 font-semibold'
                : 'border-gray-200 text-gray-500 hover:border-blue-300'
            }`}
          >
            R$ {p.toLocaleString('pt-BR')}
          </button>
        ))}
      </div>
    </div>
  )
}
