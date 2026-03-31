import { motion } from 'framer-motion'
import { useNavigate } from 'react-router-dom'

interface NavButtonsProps {
    backTo?: string
    forwardTo?: string
    backLabel?: string
    forwardLabel?: string
}

const btnBase: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: 6,
    fontFamily: 'var(--fm)',
    fontSize: 12,
    fontWeight: 700,
    padding: '9px 16px',
    borderRadius: 8,
    border: '1px solid var(--border2)',
    background: 'rgba(255,255,255,0.04)',
    color: 'var(--txt2)',
    cursor: 'pointer',
    letterSpacing: '.3px',
    textDecoration: 'none',
}

export default function NavButtons({ backTo, forwardTo, backLabel = 'Back', forwardLabel = 'Next' }: NavButtonsProps) {
    const navigate = useNavigate()

    return (
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
            {backTo ? (
                <motion.button
                    style={btnBase}
                    whileHover={{ scale: 1.04, borderColor: 'var(--g)', color: 'var(--g)', boxShadow: '0 0 12px rgba(0,229,176,.18)' }}
                    whileTap={{ scale: 0.97 }}
                    onClick={() => navigate(backTo)}
                >
                    ← {backLabel}
                </motion.button>
            ) : (
                <span />
            )}

            {forwardTo ? (
                <motion.button
                    style={{ ...btnBase, background: 'rgba(0,229,176,.08)', borderColor: 'var(--border)', color: 'var(--g)' }}
                    whileHover={{ scale: 1.04, boxShadow: '0 0 16px rgba(0,229,176,.25)' }}
                    whileTap={{ scale: 0.97 }}
                    onClick={() => navigate(forwardTo)}
                >
                    {forwardLabel} →
                </motion.button>
            ) : (
                <span />
            )}
        </div>
    )
}
