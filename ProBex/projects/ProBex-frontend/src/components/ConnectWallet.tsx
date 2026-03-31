import { useWallet } from '@txnlab/use-wallet-react'
import { useState } from 'react'

interface ConnectWalletInterface {
  openModal: boolean
  closeModal: () => void
}

const ConnectWallet = ({ openModal, closeModal }: ConnectWalletInterface) => {
  const { wallets, activeAddress } = useWallet()
  const [connecting, setConnecting] = useState(false)

  if (!openModal) return null

  // Pick the first available wallet (KMD on localnet, Pera on testnet/mainnet)
  const wallet = wallets?.[0]

  const handleConnect = async () => {
    if (!wallet) return
    setConnecting(true)
    try {
      await wallet.connect()
      closeModal()
    } catch {
      // user rejected or error
    } finally {
      setConnecting(false)
    }
  }

  return (
    <div className="modal-overlay" onClick={closeModal}>
      <div className="modal-box" onClick={(e) => e.stopPropagation()}>
        <h3>Connect Wallet</h3>

        {activeAddress ? (
          <div className="account-info">
            <p>
              Connected: <strong>{activeAddress.slice(0, 8)}…{activeAddress.slice(-6)}</strong>
            </p>
            <div className="modal-actions" style={{ marginTop: '1rem' }}>
              <button onClick={closeModal}>Close</button>
              <button
                className="btn-red"
                onClick={async () => {
                  if (wallet?.isActive) await wallet.disconnect()
                  closeModal()
                }}
              >
                Disconnect
              </button>
            </div>
          </div>
        ) : (
          <>
            <div className="wallet-list">
              <button className="wallet-list-btn" onClick={handleConnect} disabled={connecting}>
                {wallet?.metadata.icon && (
                  <img alt={wallet.metadata.name} src={wallet.metadata.icon} />
                )}
                <span>{connecting ? 'Connecting…' : `Connect with ${wallet?.metadata.name ?? 'Wallet'}`}</span>
              </button>
            </div>
            <div className="modal-actions">
              <button onClick={closeModal}>Cancel</button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
export default ConnectWallet
