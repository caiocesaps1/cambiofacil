export type Currency = 'USD' | 'EUR'
export type InstitutionType = 'bank' | 'fintech' | 'broker' | 'exchange_house'

export interface Rate {
  institution: string
  type: InstitutionType
  currency: Currency
  buy_rate: number
  sell_rate: number
  spread_pct: number
  amount_received: number
  url: string
  updated_at: string
}

export interface RatesResponse {
  currency: Currency
  amount_brl: number
  rates: Rate[]
  fetched_at: string
}
