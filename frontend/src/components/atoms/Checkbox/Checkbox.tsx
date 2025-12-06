'use client';

import React, { useId } from 'react';
import { cn } from '@/lib/utils';

export interface CheckboxProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label?: string;
  error?: string;
}

export function Checkbox({
  label,
  error,
  className,
  id,
  ...props
}: CheckboxProps) {
  const generatedId = useId();
  const checkboxId = id || generatedId;

  return (
    <div className={cn('flex items-start gap-component', className)}>
      <div className="relative flex items-center">
        <input
          type="checkbox"
          id={checkboxId}
          className={cn(
            'appearance-none',
            'w-5 h-5',
            'rounded-sm',
            'border-2',
            'border-background-glass',
            'bg-background-card',
            'cursor-pointer',
            'transition-all duration-200',
            'checked:bg-primary',
            'checked:border-primary',
            'checked:after:content-["✓"]',
            'checked:after:text-white',
            'checked:after:flex',
            'checked:after:items-center',
            'checked:after:justify-center',
            'checked:after:text-sm',
            'checked:after:font-medium',
            'focus:outline-none',
            'focus:ring-2',
            'focus:ring-primary',
            'focus:ring-offset-2',
            'focus:ring-offset-background-dark',
            'disabled:opacity-50',
            'disabled:cursor-not-allowed',
            error && 'border-accent-red',
            className
          )}
          {...props}
        />
      </div>
      {label && (
        <label
          htmlFor={checkboxId}
          className={cn(
            'text-body-regular',
            'font-regular',
            'text-text-primary',
            'cursor-pointer',
            'select-none',
            error && 'text-accent-red'
          )}
        >
          {label}
        </label>
      )}
      {error && (
        <span className="text-body-small text-accent-red mt-1">
          {error}
        </span>
      )}
    </div>
  );
}

