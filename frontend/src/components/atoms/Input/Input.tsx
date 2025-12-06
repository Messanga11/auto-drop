'use client';

import React, { useId } from 'react';
import { tokens } from '@/design-system/tokens';
import { cn } from '@/lib/utils';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  error?: string;
  label?: string;
}

export function Input({
  type = 'text',
  placeholder,
  value,
  onChange,
  error,
  label,
  className,
  id,
  ...props
}: InputProps) {
  const generatedId = useId();
  const inputId = id || generatedId;

  return (
    <div className="w-full">
      {label && (
        <label htmlFor={inputId} className="block text-body-regular text-text-primary mb-2">
          {label}
        </label>
      )}
      <input
        type={type}
        id={inputId}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        className={cn(
          'w-full',
          'rounded-lg', // Using lg radius from design system
          'px-component', // tokens.spacing.padding.component
          'py-component',
          'bg-background-glass',
          'backdrop-blur-card',
          'text-text-primary',
          'placeholder:text-text-secondary',
          'border-0',
          'focus:outline-none',
          'focus:ring-2',
          'focus:ring-primary',
          'transition-all',
          error && 'ring-2 ring-accent-red',
          className
        )}
        {...props}
      />
      {error && (
        <p className="mt-1 text-body-small text-accent-red">{error}</p>
      )}
    </div>
  );
}

