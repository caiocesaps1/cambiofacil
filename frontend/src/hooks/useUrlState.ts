import { useState, useCallback } from 'react'

function getParams() {
  return new URLSearchParams(window.location.search)
}

function pushParams(params: URLSearchParams) {
  const url = params.toString() ? `?${params}` : window.location.pathname
  window.history.replaceState(null, '', url)
}

export function useUrlState<T extends string>(
  key: string,
  defaultValue: T,
  valid?: T[],
): [T, (v: T) => void] {
  const [value, setValue] = useState<T>(() => {
    const raw = getParams().get(key) as T | null
    if (raw && (!valid || valid.includes(raw))) return raw
    return defaultValue
  })

  const set = useCallback(
    (v: T) => {
      setValue(v)
      const params = getParams()
      if (v === defaultValue) {
        params.delete(key)
      } else {
        params.set(key, v)
      }
      pushParams(params)
    },
    [key, defaultValue],
  )

  return [value, set]
}

export function useUrlNumber(key: string, defaultValue: number): [number, (v: number) => void] {
  const [value, setValue] = useState<number>(() => {
    const raw = getParams().get(key)
    const n = raw ? Number(raw) : NaN
    return isNaN(n) || n <= 0 ? defaultValue : n
  })

  const set = useCallback(
    (v: number) => {
      setValue(v)
      const params = getParams()
      if (v === defaultValue) {
        params.delete(key)
      } else {
        params.set(key, String(v))
      }
      pushParams(params)
    },
    [key, defaultValue],
  )

  return [value, set]
}
