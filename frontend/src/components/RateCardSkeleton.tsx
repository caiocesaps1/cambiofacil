export function RateCardSkeleton() {
  return (
    <div className="flex items-center justify-between p-4 rounded-xl border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800 animate-pulse">
      <div className="flex-1 space-y-2">
        <div className="flex items-center gap-2">
          <div className="h-4 w-28 bg-gray-200 dark:bg-slate-700 rounded-full" />
          <div className="h-4 w-16 bg-gray-100 dark:bg-slate-600 rounded-full" />
        </div>
        <div className="h-3 w-44 bg-gray-100 dark:bg-slate-700 rounded-full" />
      </div>

      <div className="flex items-center gap-4">
        <div className="text-right space-y-1">
          <div className="h-6 w-16 bg-gray-200 dark:bg-slate-700 rounded-md ml-auto" />
          <div className="h-3 w-20 bg-gray-100 dark:bg-slate-600 rounded-full ml-auto" />
        </div>
        <div className="h-9 w-24 bg-gray-200 dark:bg-slate-700 rounded-lg" />
      </div>
    </div>
  )
}

interface Props {
  count?: number
}

export function RateListSkeleton({ count = 4 }: Props) {
  return (
    <div className="space-y-3">
      {Array.from({ length: count }).map((_, i) => (
        <RateCardSkeleton key={i} />
      ))}
    </div>
  )
}
