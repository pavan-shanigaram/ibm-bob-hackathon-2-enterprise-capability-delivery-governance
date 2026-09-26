import React from 'react'

interface Props {
  loading?: boolean
  onClick?: () => void
  children: React.ReactNode
  variant?: 'primary' | 'danger' | 'ghost'
  size?: 'sm' | 'md'
  type?: 'button' | 'submit'
  disabled?: boolean
  className?: string
}

const VARIANT = {
  primary: 'bg-blue-600 hover:bg-blue-700 text-white border-transparent',
  danger:  'bg-red-600 hover:bg-red-700 text-white border-transparent',
  ghost:   'bg-white hover:bg-gray-50 text-gray-700 border-gray-200',
}
const SIZE = {
  sm: 'px-3 py-1.5 text-xs',
  md: 'px-4 py-2 text-sm',
}

export default function Button({ loading, onClick, children, variant = 'primary', size = 'md', type = 'button', disabled, className = '' }: Props) {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={loading || disabled}
      className={`inline-flex items-center gap-1.5 font-medium rounded-lg border transition-colors disabled:opacity-50 disabled:cursor-not-allowed ${VARIANT[variant]} ${SIZE[size]} ${className}`}
    >
      {loading && (
        <svg className="animate-spin h-3.5 w-3.5" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
        </svg>
      )}
      {children}
    </button>
  )
}
