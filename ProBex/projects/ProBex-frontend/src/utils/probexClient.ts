import { AlgorandClient } from '@algorandfoundation/algokit-utils'
import algosdk from 'algosdk'
import { getAlgodConfigFromViteEnvironment } from './network/getAlgoClientConfigs'

// The deployed app ID — set via environment variable after deployment
export const APP_ID = Number(import.meta.env.VITE_APP_ID ?? 0)

export interface MarketState {
  totalYesPool: bigint
  totalNoPool: bigint
  marketResolved: boolean
  winningOutcome: number // 0 = unresolved, 1 = yes, 2 = no
  creatorAddress: string
}

export interface UserBet {
  amount: bigint
  outcome: number // 1 = yes, 2 = no
  claimed: boolean
}

export function getAlgorandClient(): AlgorandClient {
  const cfg = getAlgodConfigFromViteEnvironment()
  return AlgorandClient.fromConfig({ algodConfig: cfg })
}

export function getAlgodClient(): algosdk.Algodv2 {
  const cfg = getAlgodConfigFromViteEnvironment()
  return new algosdk.Algodv2(String(cfg.token), cfg.server, cfg.port)
}

export async function fetchMarketState(appId: number): Promise<MarketState> {
  const algod = getAlgodClient()
  const appInfo = await algod.getApplicationByID(appId).do()

  const globalState = appInfo.params?.globalState ?? []

  let totalYesPool = BigInt(0)
  let totalNoPool = BigInt(0)
  let marketResolved = false
  let winningOutcome = 0
  let creatorAddress = String(appInfo.params?.creator ?? '')

  for (const kv of globalState) {
    const key = new TextDecoder().decode(kv.key)
    const val = kv.value

    if (key === 'total_yes_pool') {
      totalYesPool = val.uint ?? 0n
    } else if (key === 'total_no_pool') {
      totalNoPool = val.uint ?? 0n
    } else if (key === 'market_resolved') {
      marketResolved = (val.uint ?? 0n) !== 0n
    } else if (key === 'winning_outcome') {
      winningOutcome = Number(val.uint ?? 0n)
    }
  }

  return { totalYesPool, totalNoPool, marketResolved, winningOutcome, creatorAddress }
}

export async function fetchUserBet(appId: number, address: string): Promise<UserBet | null> {
  const algod = getAlgodClient()
  try {
    const acctInfo = await algod.accountApplicationInformation(address, appId).do()
    const localState =
      acctInfo?.appLocalState?.keyValue ?? []

    if (localState.length === 0) return null

    let amount = BigInt(0)
    let outcome = 0
    let claimed = false

    for (const kv of localState) {
      const key = new TextDecoder().decode(kv.key)
      const val = kv.value

      if (key === 'bet_amount') {
        amount = val.uint ?? 0n
      } else if (key === 'bet_outcome') {
        outcome = Number(val.uint ?? 0n)
      } else if (key === 'claimed') {
        claimed = (val.uint ?? 0n) !== 0n
      }
    }

    return { amount, outcome, claimed }
  } catch {
    return null
  }
}

/** Convert microAlgos to Algos string with 6 decimal places */
export function microAlgosToAlgos(microAlgos: bigint): string {
  const algos = Number(microAlgos) / 1_000_000
  return algos.toFixed(6)
}

/** Convert Algos string to microAlgos bigint */
export function algosToMicroAlgos(algos: number): bigint {
  return BigInt(Math.floor(algos * 1_000_000))
}

/** Get application address from app ID */
export function getAppAddress(appId: number): string {
  return algosdk.getApplicationAddress(appId).toString()
}
