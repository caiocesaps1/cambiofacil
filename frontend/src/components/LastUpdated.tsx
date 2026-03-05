import { RefreshCw } from 'lucide-react'

interface Props {
  fetchedAt: string
  isRefetching: boolean
}

export function LastUpdated({ fetchedAt, isRefetching }: Props) {
  const date = new Date(fetchedAt)
  const formatted = date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })

  return (
    <div className="flex items-center gap-1.5 text-xs text-gray-400">
      <RefreshCw size={12} className={isRefetching ? 'animate-spin' : ''} />
      <span>Atualizado às {formatted}</span>
    </div>
  )
}
